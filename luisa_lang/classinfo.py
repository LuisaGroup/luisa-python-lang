import inspect
from types import GenericAlias, NoneType
import types
import typing
from typing import (
    Any,
    Callable,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    TypeAliasType,
    TypeVar,
    Generic,
    Dict,
    Type,
    Union,
    cast,
)
import functools
from dataclasses import dataclass


class GenericInstance:
    origin: 'VarType'
    args: List["VarType"]

    def __init__(self, origin: 'VarType', args: List["VarType"]):
        self.origin = origin
        self.args = args

    def __repr__(self):
        return f"{self.origin}[{', '.join(map(repr, self.args))}]"


class UnionType:
    types: List["VarType"]

    def __init__(self, types: List["VarType"]):
        self.types = types

    def __repr__(self):
        return f"Union[{', '.join(map(repr, self.types))}]"

    def substitute(self, env: Dict[TypeVar, 'VarType']) -> "UnionType":
        return UnionType([subst_type(ty, env) for ty in self.types])


class AnyType:
    def __repr__(self):
        return "Any"

    def __eq__(self, other):
        return isinstance(other, AnyType)


class SelfType:
    def __repr__(self):
        return "Self"

    def __eq__(self, other):
        return isinstance(other, SelfType)


class LiteralType:
    value: Any

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f"Literal[{self.value}]"

    def __eq__(self, other):
        return isinstance(other, LiteralType) and self.value == other.value


class AnnotatedType:
    origin: 'VarType'
    annotations: List[Any]

    def __init__(self, origin: 'VarType', annotations: List[Any]):
        self.origin = origin
        self.annotations = annotations

    def __repr__(self):
        return f"Annotated[{self.origin}, {self.annotations}]"

    def substitute(self, env: Dict[TypeVar, 'VarType']) -> "AnnotatedType":
        return AnnotatedType(subst_type(self.origin, env), self.annotations)


type VarType = Union[TypeVar, Type, GenericInstance,
                     UnionType, SelfType, AnyType, LiteralType, AnnotatedType]


def subst_type(ty: VarType, env: Dict[TypeVar, VarType]) -> VarType:
    match ty:
        case TypeVar():
            return env.get(ty, ty)
        case GenericInstance(origin=origin, args=args):
            return GenericInstance(origin, [subst_type(arg, env) for arg in args])
        case MethodType() | UnionType() | AnnotatedType():
            return ty.substitute(env)
        case _:
            return ty


class MethodType:
    type_vars: List[TypeVar]
    args: List[Tuple[str, VarType]]
    return_type: VarType
    env: Dict[TypeVar, VarType]
    is_static: bool

    def __init__(
        self, type_vars: List[TypeVar], args: List[Tuple[str, VarType]], return_type: VarType, env: Optional[Dict[TypeVar, VarType]] = None, is_static: bool = False
    ):
        self.type_vars = type_vars
        self.args = args
        self.return_type = return_type
        self.env = env or {}
        self.is_static = is_static

    def __repr__(self):
        # [a, b, c](x: T, y: U) -> V
        return f"[{', '.join(map(repr, self.type_vars))}]({', '.join(map(repr, self.args))}) -> {self.return_type}"

    def substitute(self, env: Dict[TypeVar, VarType]) -> "MethodType":
        return MethodType([], [(arg[0], subst_type(arg[1], env)) for arg in self.args], subst_type(self.return_type, env), env)


class ClassType:
    type_vars: List[TypeVar]
    fields: Dict[str, VarType]
    methods: Dict[str, MethodType]

    def __init__(
        self,
        type_vars: List[TypeVar],
        fields: Dict[str, VarType],
        methods: Dict[str, MethodType],
    ):
        self.type_vars = type_vars
        self.fields = fields
        self.methods = methods

    def __repr__(self):
        # class[T, U]:
        #     a: T
        #     b: U
        #     def foo(x: T, y: U) -> V
        return (
            f"class[{', '.join(map(repr, self.type_vars))}]:\n"
            + "\n".join(f"    {name}: {type}" for name,
                        type in self.fields.items())
            + "\n"
            + "\n".join(
                f"    def {name}{method}" for name, method in self.methods.items()
            )
        )

    def instantiate(self, type_args: List[VarType]) -> "ClassType":
        if len(type_args) != len(self.type_vars):
            raise RuntimeError(
                f"Expected {len(self.type_vars)}" +
                f"type arguments but got {len(type_args)}"
            )
        env = dict(zip(self.type_vars, type_args))
        return ClassType(
            [], {name: subst_type(ty, env) for name, ty in self.fields.items()}, {
                name: method.substitute(env) for name, method in self.methods.items()}
        )


_CLS_TYPE_INFO: Dict[type, ClassType] = {}


def class_typeinfo(cls: type) -> ClassType:
    if cls in _CLS_TYPE_INFO:
        return _CLS_TYPE_INFO[cls]
    raise RuntimeError(f"Class {cls} is not registered.")


def _is_class_registered(cls: type) -> bool:
    return cls in _CLS_TYPE_INFO


_BUILTIN_ANNOTATION_BASES = set([typing.Generic, typing.Protocol, object])


def _get_base_classinfo(cls: type, globalns) -> List[tuple[str, ClassType]]:
    if not hasattr(cls, "__orig_bases__"):
        return []
    info = []
    for base in cls.__orig_bases__:
        if hasattr(base, "__origin__"):
            base_params = []
            base_orig: Any = base.__origin__

            if not _is_class_registered(base_orig) and base_orig not in _BUILTIN_ANNOTATION_BASES:
                raise RuntimeError(
                    f"Base class {base_orig} of {cls} is not registered."
                )
            for arg in base.__args__:
                if isinstance(arg, typing.ForwardRef):
                    arg: type = typing._eval_type(  # type: ignore
                        arg, globalns, globalns)  # type: ignore
                base_params.append(arg)
            if base_orig in _BUILTIN_ANNOTATION_BASES:
                pass
            else:
                assert isinstance(base_orig, type)
                base_info = class_typeinfo(cast(type, base_orig))
                info.append(
                    (base.__name__, base_info.instantiate(base_params)))
        else:
            if _is_class_registered(base):
                info.append((base.__name__, class_typeinfo(base)))
    return info


def _get_cls_globalns(cls: type) -> Dict[str, Any]:
    module = inspect.getmodule(cls)
    assert module is not None
    return module.__dict__


def parse_type_hint(hint: Any) -> VarType:
    # print(hint, type(hint))
    if hint is None:
        return NoneType
    if isinstance(hint, TypeVar):
        return hint
    if isinstance(hint, types.UnionType):
        return UnionType([parse_type_hint(arg) for arg in hint.__args__])
    if hint is typing.Any:
        return AnyType()
    if isinstance(hint, TypeAliasType):
        return parse_type_hint(hint.__value__)

    origin = typing.get_origin(hint)
    if origin:
        if origin is typing.Annotated:
            annotate_args = typing.get_args(hint)
            return AnnotatedType(parse_type_hint(annotate_args[0]), list(annotate_args[1:]))
        elif origin is Union:
            return UnionType([parse_type_hint(arg) for arg in typing.get_args(hint)])
        elif origin is Literal:
            return LiteralType(typing.get_args(hint)[0])
        elif isinstance(origin, TypeAliasType):
            def do() -> VarType:
                assert isinstance(hint, GenericAlias)
                args = list(typing.get_args(hint))
                assert len(args) == len(origin.__parameters__), f"Expected {
                    len(origin.__parameters__)} type arguments but got {len(args)}"
                true_origin = origin.__value__
                parametric_args = origin.__parameters__
                parsed_args = [parse_type_hint(arg) for arg in args]
                env = dict(zip(parametric_args, parsed_args))
                parsed_origin = parse_type_hint(true_origin)
                return subst_type(parsed_origin, env)
            return do()
        elif isinstance(origin, type):
            # assert isinstance(origin, type), f"origin must be a type but got {origin}"
            args = list(typing.get_args(hint))
            return GenericInstance(origin, [parse_type_hint(arg) for arg in args])

        else:
            raise RuntimeError(f"Unsupported origin type: {
                               origin}, {type(origin), type(hint)}")

    if isinstance(hint, type):
        return hint
    if hint == typing.Self:
        return SelfType()
    raise RuntimeError(f"Unsupported type hint: {hint}")


def extract_type_vars_from_hint(hint: typing.Any) -> List[TypeVar]:
    if isinstance(hint, TypeVar):
        return [hint]
    if hasattr(hint, "__args__"):  # Handle custom generic types like Foo[T]
        type_vars = []
        for arg in hint.__args__:
            type_vars.extend(extract_type_vars_from_hint(arg))
        return type_vars
    return []


def get_type_vars(func: typing.Callable) -> List[TypeVar]:
    type_hints = typing.get_type_hints(func, include_extras=True)
    type_vars = []
    for hint in type_hints.values():
        type_vars.extend(extract_type_vars_from_hint(hint))
    return list(set(type_vars))  # Return unique type vars


def parse_func_signature(func: object, globalns: Dict[str, Any], foreign_type_vars: List[TypeVar], is_static: bool = False) -> MethodType:
    assert inspect.isfunction(func)
    signature = inspect.signature(func)
    method_type_hints = typing.get_type_hints(func, globalns)
    param_types: List[Tuple[str, VarType]] = []
    type_vars = get_type_vars(func)
    for param in signature.parameters.values():
        if param.name == "self":
            param_types.append((param.name, SelfType()))
        elif param.name in method_type_hints:
            param_types.append((param.name, parse_type_hint(
                method_type_hints[param.name])))
        else:
            param_types.append((param.name, AnyType()))
    if "return" in method_type_hints:
        return_type = parse_type_hint(method_type_hints.get("return"))
    else:
        return_type = AnyType()
    # remove foreign type vars from type_vars
    type_vars = [tv for tv in type_vars if tv not in foreign_type_vars]
    return MethodType(type_vars, param_types, return_type, is_static=is_static)


def is_static(cls: type, method_name: str) -> bool:
    method = getattr(cls, method_name, None)
    if method is None:
        return False
    # Using inspect to retrieve the method directly from the class
    method = cls.__dict__.get(method_name, None)
    return isinstance(method, staticmethod)


def register_class(cls: type) -> None:
    cls_qualname = cls.__qualname__
    globalns = _get_cls_globalns(cls)
    globalns[cls.__name__] = cls
    assert (
        "<locals>" not in cls_qualname
    ), f"Cannot use local class {cls_qualname} as a DSL type. Must be a top-level class!"

    origin = typing.get_origin(cls)
    type_args: List[Type]
    type_vars: Any
    if origin:
        type_hints = typing.get_type_hints(origin, globalns)
        type_args = list(typing.get_args(cls))
        type_vars = getattr(origin, "__parameters__", None)
    else:
        type_hints = typing.get_type_hints(cls, globalns)
        type_args = []
        type_vars = getattr(cls, "__parameters__", None)
    assert type_args == []
    assert not type_vars or isinstance(type_vars, tuple), type_vars
    # print(type_hints)
    # if hasattr(cls, "__orig_bases__"):
    #     print(cls.__base__)
    #     print(cls.__orig_bases__)
    base_infos = _get_base_classinfo(cls, globalns)

    base_fields: Set[str] = set()
    base_methods: Set[str] = set()

    for _base_name, base_info in base_infos:
        base_fields.update(base_info.fields.keys())
        base_methods.update(base_info.methods.keys())

    local_fields: Set[str] = set()
    local_methods: Set[str] = set()
    for name, hint in type_hints.items():
        if name in base_fields:
            continue
        local_fields.add(name)
    for name, member in inspect.getmembers(cls, inspect.isfunction):
        if name in base_methods:
            continue
        local_methods.add(name)

    cls_ty = ClassType([], {}, {})
    for _base_name, base_info in base_infos:
        cls_ty.fields.update(base_info.fields)
        cls_ty.methods.update(base_info.methods)

    if type_vars:
        for tv in type_vars:
            cls_ty.type_vars.append(tv)
    for name, member in inspect.getmembers(cls):
        if name in local_methods:
            # print(f'Found local method: {name} in {cls}')
            cls_ty.methods[name] = parse_func_signature(
                member, globalns, cls_ty.type_vars, is_static=is_static(cls, name))
    for name in local_fields:
        cls_ty.fields[name] = parse_type_hint(type_hints[name])
    _CLS_TYPE_INFO[cls] = cls_ty
