from enum import Enum, auto
from typing_extensions import TypeAliasType
from typing import (
    Callable,
    Dict,
    Optional,
    Sequence,
    TypeAlias,
    TypeVar,
    Union,
    Generic,
    Literal,
    cast,
    overload,
    Any,
)
from luisa_lang._utils import _get_full_name
from luisa_lang.math_types import *
from luisa_lang._builtin_decor import _builtin_type, _builtin, _intrinsic_impl
import luisa_lang.hir as hir
import luisa_lang.parse as parse
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


def _dsl_func_impl(f: _T, kind: _ObjKind, attrs: Dict[str, Any]) -> _T:
    import sourceinspect
    from luisa_lang._utils import retrieve_ast_and_filename

    assert inspect.isfunction(f), f"{f} is not a function"
    print(hir.GlobalContext.get)
    obj_ast, obj_file = retrieve_ast_and_filename(f)
    assert isinstance(obj_ast, ast.Module), f"{obj_ast} is not a module"

    ctx = hir.GlobalContext.get()
    func_globals: Any = getattr(f, "__globals__", {})
    parsing_ctx = parse.ParsingContext(func_globals)
    print(ast.dump(obj_ast))
    func_def = obj_ast.body[0]
    if not isinstance(func_def, ast.FunctionDef):
        raise RuntimeError("Function definition expected.")
    func_parser = parse.FuncParser(_get_full_name(f), func_def, parsing_ctx)
    func_ir = func_parser.parse_body()
    ctx.functions[f] = func_ir
    if kind == _ObjKind.FUNC:

        def dummy(*args, **kwargs):
            raise RuntimeError("DSL function should only be called in DSL context.")

        setattr(dummy, "__luisa_func__", f)
        return cast(_T, dummy)
    else:
        return cast(_T, f)


def _dsl_decorator_impl(obj: _T, kind: _ObjKind, attrs: Dict[str, Any]) -> _T:

    if kind == _ObjKind.STRUCT:
        return obj
    elif kind == _ObjKind.FUNC or kind == _ObjKind.KERNEL:
        return _dsl_func_impl(obj, kind, attrs)
    raise NotImplementedError()


def struct(cls: type) -> type:
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
    return cls


@overload
def kernel(f: _KernelType) -> _KernelType: ...
@overload
def kernel(export: bool = False, **kwargs) -> Callable[[_KernelType], _KernelType]: ...
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
def func(inline: bool | Literal["always"] = False, **kwargs) -> Callable[[_F], _F]: ...
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


def typeof(value: Any) -> hir.Type:
    if isinstance(value, hir.Type):
        return value
    if isinstance(value, type):
        return hir.GlobalContext.get().types[value]
    return hir.GlobalContext.get().types[type(value)]


_t = hir.SymbolicType("T")
_n = hir.SymbolicConstant("N", typeof(u32))


# @_builtin_type(
#     hir.ParametricType(
#         "Array", [hir.TypeParameter(_t, bound=[])], hir.ArrayType(_t, _n)
#     )
# )
class Array(Generic[_T, _N]):
    def __init__(self) -> None:
        return _intrinsic_impl()

    def __getitem__(self, index: int | u32 | u64) -> _T:
        return _intrinsic_impl()

    def __setitem__(self, index: int | u32 | u64, value: _T) -> None:
        return _intrinsic_impl()

    def __len__(self) -> u32 | u64:
        return _intrinsic_impl()


# @_builtin_type(
#     hir.ParametricType(
#         "Buffer", [hir.TypeParameter(_t, bound=[])], hir.OpaqueType("Buffer")
#     )
# )
class Buffer(Generic[_T]):
    def __getitem__(self, index: int | u32 | u64) -> _T:
        return _intrinsic_impl()

    def __setitem__(self, index: int | u32 | u64, value: _T) -> None:
        return _intrinsic_impl()

    def __len__(self) -> u32 | u64:
        return _intrinsic_impl()


# @_builtin_type(
#     hir.ParametricType(
#         "Pointer", [hir.TypeParameter(_t, bound=[])], hir.PointerType(_t)
#     )
# )
class Pointer(Generic[_T]):
    def __getitem__(self, index: int | i32 | i64 | u32 | u64) -> _T:
        return _intrinsic_impl()

    def __setitem__(self, index: int | i32 | i64 | u32 | u64, value: _T) -> None:
        return _intrinsic_impl()

    @property
    def value(self) -> _T:
        return _intrinsic_impl()

    @value.setter
    def value(self, value: _T) -> None:
        return _intrinsic_impl()


# hir.GlobalContext.get().flush()