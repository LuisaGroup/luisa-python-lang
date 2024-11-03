from luisa_lang.classinfo import VarType, GenericInstance, UnionType,  _get_cls_globalns, register_class, class_typeinfo
from enum import Enum, auto
from typing_extensions import TypeAliasType
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
    Generic,
    Literal,
    cast,
    overload,
    Any,
)
from luisa_lang.utils import get_full_name, unique_hash
from luisa_lang.math_types import *
from luisa_lang._builtin_decor import _builtin_type, _builtin, _intrinsic_impl
from luisa_lang.lang_builtins import *
import luisa_lang.hir as hir
import luisa_lang.classinfo as classinfo
import luisa_lang.parse as parse
from luisa_lang.parse import FuncParser
import ast
import inspect

_T = TypeVar("_T")
_N = TypeVar("_N", int, u32, u64)
_F = TypeVar("_F", bound=Callable[..., Any])
_KernelType = TypeVar("_KernelType", bound=Callable[..., None])


class _ObjKind(Enum):
    BUILTIN_TYPE = auto()
    STRUCT = auto()
    FUNC = auto()
    KERNEL = auto()


def _make_func_template(f: Callable[..., Any], func_name: str, func_globals: Dict[str, Any], self_type: Optional[hir.Type] = None):
    # parsing_ctx = _parse.ParsingContext(func_name, func_globals)
    # func_sig_parser = _parse.FuncParser(func_name, f, parsing_ctx, self_type)
    # func_sig = func_sig_parser.parsed_func
    # params = [v.name for v in func_sig_parser.params]
    # is_generic = func_sig_parser.p_ctx.type_vars != {}

    func_sig = classinfo.parse_func_signature(f, func_globals, [])
    func_sig_converted, sig_parser = parse.convert_func_signature(
        func_sig, func_name, func_globals, {}, [], self_type)

    def parsing_func(args: hir.FunctionTemplateResolvingArgs) -> hir.FunctionLike:
        type_var_ns: Dict[TypeVar, hir.Type | hir.ComptimeValue] = {}
        any_param_types: List[hir.Type] = []
        if is_generic:
            mapping = hir.match_func_template_args(func_sig_converted, args)
            if isinstance(mapping, hir.TypeInferenceError):
                raise mapping
            if len(mapping) != len(func_sig_converted.generic_params):
                # print(mapping, func_sig_converted.generic_params)
                raise hir.TypeInferenceError(
                    None, "not all type parameters are resolved")
            for p in func_sig_converted.generic_params:
                if p not in mapping:
                    raise hir.TypeInferenceError(
                        None, f"type parameter {p} is not resolved")
                type_var_ns[sig_parser.generic_param_to_type_var[p]
                            ] = mapping[p]
                # print(f'binding {p.name} = {mapping[p]}, tv: {sig_parser.generic_param_to_type_var[p]} @{id(sig_parser.generic_param_to_type_var[p])}')
        # print('parsing  instantiated signature')
        func_sig_instantiated, _ = parse.convert_func_signature(
            func_sig, func_name, func_globals, type_var_ns, any_param_types, self_type)
        func_parser = FuncParser(
            func_name, f, func_sig_instantiated, func_globals, type_var_ns, self_type)
        return func_parser.parse_body()
    params = [v[0] for v in func_sig.args]
    is_generic = len(func_sig.type_vars) > 0
    return hir.FunctionTemplate(func_name, params, parsing_func, is_generic)


def _dsl_func_impl(f: _T, kind: _ObjKind, attrs: Dict[str, Any]) -> _T:
    import sourceinspect
    assert inspect.isfunction(f), f"{f} is not a function"
    # print(hir.GlobalContext.get)

    ctx = hir.GlobalContext.get()
    func_name = get_full_name(f)
    func_globals: Any = getattr(f, "__globals__", {})

    if kind == _ObjKind.FUNC:
        template = _make_func_template(f, func_name, func_globals)
        ctx.functions[f] = template
        setattr(f, "__luisa_func__", template)
        return cast(_T, f)
    else:
        raise NotImplementedError()
        # return cast(_T, f)


def _dsl_struct_impl(cls: type[_T], attrs: Dict[str, Any]) -> type[_T]:
    ctx = hir.GlobalContext.get()

    register_class(cls)
    cls_info = class_typeinfo(cls)
    globalns = _get_cls_globalns(cls)
    globalns[cls.__name__] = cls

    def get_ir_type(var_ty: VarType) -> hir.Type:
        if isinstance(var_ty, (UnionType, classinfo.AnyType, classinfo.SelfType)):
            raise RuntimeError("Struct fields cannot be UnionType")
        if isinstance(var_ty, TypeVar):
            raise NotImplementedError()
        if isinstance(var_ty, GenericInstance):
            raise NotImplementedError()
        return ctx.types[var_ty]

    fields: List[Tuple[str, hir.Type]] = []
    for name, field in cls_info.fields.items():
        fields.append((name, get_ir_type(field)))
    ir_ty = hir.StructType(
        f'{cls.__name__}_{unique_hash(cls.__qualname__)}', cls.__qualname__, fields)
    ctx.types[cls] = ir_ty

    for name, method in cls_info.methods.items():
        method_object = getattr(cls, name)
        template = _make_func_template(
            method_object, get_full_name(method_object), globalns, self_type=ir_ty)
        ir_ty.methods[name] = template
    return cls


def _dsl_decorator_impl(obj: _T, kind: _ObjKind, attrs: Dict[str, Any]) -> _T:
    if kind == _ObjKind.STRUCT:
        assert isinstance(obj, type), f"{obj} is not a type"
        return cast(_T, _dsl_struct_impl(obj, attrs))
    elif kind == _ObjKind.FUNC or kind == _ObjKind.KERNEL:
        return _dsl_func_impl(obj, kind, attrs)
    raise NotImplementedError()


def struct(cls: type[_T]) -> type[_T]:
    """
    Mark a class as a DSL struct.

    Example:
    ```python
    @luisa.struct
    class Sphere:
        center: luisa.float3
        radius: luisa.float

        def volume(self) -> float:
            return 4.0 / 3.0 * math.pi * self.radius ** 3
    ```
    """
    return _dsl_decorator_impl(cls, _ObjKind.STRUCT, {})


@overload
def kernel(f: _KernelType) -> _KernelType: ...


@overload
def kernel(export: bool = False, **kwargs) -> Callable[[
    _KernelType], _KernelType]: ...


def kernel(*args, **kwargs) -> _KernelType | Callable[[_KernelType], _KernelType]:
    if len(args) == 1 and len(kwargs) == 0:
        f = args[0]
        return f

    def decorator(f):
        return f

    return decorator


class InoutMarker:
    value: str

    def __init__(self, value: str):
        self.value = value


inout = InoutMarker("inout")
out = InoutMarker("out")


@overload
def func(f: _F) -> _F: ...


@overload
def func(inline: bool | Literal["always"]
         = False, **kwargs) -> Callable[[_F], _F]: ...


def func(*args, **kwargs) -> _F | Callable[[_F], _F]:
    """
    Mark a function as a DSL function.
    To mark an argument as inout/out, use the `var=inout` syntax in decorator arguments.

    Example:
    ```python
    @luisa.func(a=inout, b=inout)
    def swap(a: int, b: int):
        a, b = b, a
    ```
    """

    def impl(f: _F) -> _F:
        return _dsl_decorator_impl(f, _ObjKind.FUNC, kwargs)

    if len(args) == 1 and len(kwargs) == 0:
        f = args[0]
        return impl(f)

    def decorator(f):
        return impl(f)

    return decorator


