import inspect
from types import NoneType
import typing
from typing import (
    Any,
    Callable,
    List,
    Literal,
    Optional,
    Set,
    TypeVar,
    Generic,
    Dict,
    Type,
    Union,
)
import functools
from dataclasses import dataclass


class GenericInstance:
    origin: type
    args: List["VarType"]

    def __init__(self, origin: type, args: List["VarType"]):
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

VarType = Union[TypeVar, Type, GenericInstance, UnionType]

def subst_type(ty: VarType, env: Dict[TypeVar, VarType]) -> VarType:
    match ty:
        case TypeVar():
            return env.get(ty, ty)
        case GenericInstance(origin=origin, args=args):
            return GenericInstance(origin, [subst_type(arg, env) for arg in args])
        case _:
            return ty

class MethodType:
    type_vars: List[TypeVar]
    args: List[VarType]
    return_type: VarType
    env: Dict[TypeVar, VarType]

    def __init__(
        self, type_vars: List[TypeVar], args: List[VarType], return_type: VarType, env: Optional[Dict[TypeVar, VarType]] = None
    ):
        self.type_vars = type_vars
        self.args = args
        self.return_type = return_type
        self.env = env or {}

    def __repr__(self):
        # [a, b, c](x: T, y: U) -> V
        return f"[{', '.join(map(repr, self.type_vars))}]({', '.join(map(repr, self.args))}) -> {self.return_type}"
    
    def substitute(self, env: Dict[TypeVar, VarType]) -> "MethodType":
        return MethodType([], [subst_type(arg, env) for arg in self.args], subst_type(self.return_type, env), env)


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
                f"Expected {len(self.type_vars)} type arguments but got {len(type_args)}"
            )
        env = dict(zip(self.type_vars, type_args))
        return ClassType(
            [], {name: subst_type(ty, env) for name, ty in self.fields.items()}, {name: method.substitute(env) for name, method in self.methods.items()}
        )

_CLS_TYPE_INFO: Dict[type, ClassType] = {}


def _class_typeinfo(cls: type) -> ClassType:
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
            base_orig = base.__origin__
            if not _is_class_registered(base_orig) and base_orig not in _BUILTIN_ANNOTATION_BASES:
                raise RuntimeError(
                    f"Base class {base_orig} of {cls} is not registered."
                )
            for arg in base.__args__:
                if isinstance(arg, typing.ForwardRef):
                    arg: type = typing._eval_type(arg, globalns, globalns) #type: ignore
                base_params.append(arg)
            if base_orig in _BUILTIN_ANNOTATION_BASES:
                pass
            else:
                base_info = _class_typeinfo(base_orig)
                info.append((base.__name__, base_info.instantiate(base_params)))
        else:
            if _is_class_registered(base):
                info.append((base.__name__, _class_typeinfo(base)))
    return info

def _get_cls_globalns(cls: type) -> Dict[str, Any]:
    module = inspect.getmodule(cls)
    assert module is not None
    return module.__dict__

def _register_class(cls: type) -> None:
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

    def parse_type_hint(hint: Any) -> VarType:

        if hint is None:
            return NoneType
        if isinstance(hint, TypeVar):
            return hint
        origin = typing.get_origin(hint)
        if origin:
            if isinstance(origin, type):
            # assert isinstance(origin, type), f"origin must be a type but got {origin}"
                args = list(typing.get_args(hint))
                return GenericInstance(origin, [parse_type_hint(arg) for arg in args])
            elif origin is Union:
                return UnionType([parse_type_hint(arg) for arg in typing.get_args(hint)])
            else:
                raise RuntimeError(f"Unsupported origin type: {origin}")
        if isinstance(hint, type):
            return hint
        raise RuntimeError(f"Unsupported type hint: {hint}")

    cls_ty = ClassType([], {}, {})
    for _base_name, base_info in base_infos:
        cls_ty.fields.update(base_info.fields)
        cls_ty.methods.update(base_info.methods)
    if type_vars:
        for tv in type_vars:
            cls_ty.type_vars.append(tv)
    for name, member in inspect.getmembers(cls):
        if name in local_methods:
            assert inspect.isfunction(member)
            signature = inspect.signature(member)
            method_type_hints = typing.get_type_hints(member)
            param_types: List[VarType] = []
            for param in signature.parameters.values():
                if param.name == "self":
                    param_types.append(cls)
                else:
                    param_types.append(parse_type_hint(
                        method_type_hints[param.name]))
            return_type = parse_type_hint(method_type_hints.get("return"))
            cls_ty.methods[name] = MethodType([], param_types, return_type)
    for name in local_fields:
        cls_ty.fields[name] = parse_type_hint(type_hints[name])
    _CLS_TYPE_INFO[cls] = cls_ty
