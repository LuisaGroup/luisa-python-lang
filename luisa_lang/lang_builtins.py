

from luisa_lang.math_types import *
import luisa_lang.hir as hir
import typing
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
    Generic,
    Literal,
    overload,
    Any,
)
from luisa_lang._builtin_decor import builtin, builtin_type, _intrinsic_impl
from luisa_lang import parse

T = TypeVar("T")
N = TypeVar("N", int, u32, u64)


@builtin("dispatch_id")
def dispatch_id() -> uint3:
    return _intrinsic_impl()


@builtin("thread_id")
def thread_id() -> uint3:
    return _intrinsic_impl()


@builtin("block_id")
def block_id() -> uint3:
    return _intrinsic_impl()


@builtin("cast")
def cast(target: type[T], value: Any) -> T:
    """
    Attempt to convert the value to the target type.
    """
    return _intrinsic_impl()


@builtin("bitcast")
def bitcast(target: type[T], value: Any) -> T:
    return _intrinsic_impl()


class ComptimeBlock:
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self):
        pass


class _ComptimeBlockMarker:
    pass


F = TypeVar("F", bound=Callable[..., Any])


def instantiate(f: F, *args: List[type]) -> F:
    return _intrinsic_impl()


@overload
def comptime(a: _ComptimeBlockMarker) -> ComptimeBlock: ...


@overload
def comptime(src: str) -> Any: ...


@overload
def comptime(a: T) -> T: ...


def comptime(a):
    """
    Allowing mixing normal python object as compile-time value with DSL code.
    Usage:
        - `lc.comptime(e)` marks the expression `e` as a compile-time value.
        - `with lc.comptime() as block: ...` marks the block as a compile-time block.
    """
    if isinstance(a, _ComptimeBlockMarker):
        return ComptimeBlock()
    return a


parse.comptime = comptime


def static_assert(cond: Any, msg: str = ""):
    pass


def unroll(range_: Sequence[int]) -> Sequence[int]:
    return range_


@builtin("address_of")
def address_of(a: T) -> 'Pointer[T]':
    return _intrinsic_impl()

# class StaticEval:
#


def type_of_opt(value: Any) -> Optional[hir.Type]:
    if isinstance(value, hir.Type):
        return value
    if isinstance(value, type):
        return hir.GlobalContext.get().types[value]
    return hir.GlobalContext.get().types.get(type(value))


def typeof(value: Any) -> hir.Type:
    ty = type_of_opt(value)
    if ty is None:
        raise TypeError(f"Cannot determine type of {value}")
    return ty


_t = hir.SymbolicType(hir.GenericParameter("_T", "luisa_lang.lang"))
_n = hir.SymbolicConstant(hir.GenericParameter(
    "_N", "luisa_lang.lang")), typeof(u32)


# @_builtin_type(
#     hir.ParametricType(
#         "Array", [hir.TypeParameter(_t, bound=[])], hir.ArrayType(_t, _n)
#     )
# )
class Array(Generic[T, N]):
    def __init__(self) -> None:
        return _intrinsic_impl()

    def __getitem__(self, index: int | u32 | u64) -> T:
        return _intrinsic_impl()

    def __setitem__(self, index: int | u32 | u64, value: T) -> None:
        return _intrinsic_impl()

    def __len__(self) -> u32 | u64:
        return _intrinsic_impl()

def __buffer_ty():
    t = hir.GenericParameter("T", "luisa_lang.lang")
    return hir.ParametricType(
        [t], hir.OpaqueType("Buffer"), None
    )

# @builtin_type(
#     # hir.ParametricType(
#     #     "Buffer", [hir.TypeParameter(_t, bound=[])], hir.OpaqueType("Buffer")
#     # )
# )
class Buffer(Generic[T]):
    def __getitem__(self, index: int | u32 | u64) -> T:
        return _intrinsic_impl()

    def __setitem__(self, index: int | u32 | u64, value: T) -> None:
        return _intrinsic_impl()

    def __len__(self) -> u32 | u64:
        return _intrinsic_impl()


# @builtin_type(
#     hir.ParametricType(
#         "Pointer", [hir.TypeParameter(_t, bound=[])], hir.PointerType(_t)
#     )
# )
class Pointer(Generic[T]):
    def __getitem__(self, index: int | i32 | i64 | u32 | u64) -> T:
        return _intrinsic_impl()

    def __setitem__(self, index: int | i32 | i64 | u32 | u64, value: T) -> None:
        return _intrinsic_impl()

    @property
    def value(self) -> T:
        return _intrinsic_impl()

    @value.setter
    def value(self, value: T) -> None:
        return _intrinsic_impl()


__all__: List[str] = [
    'Pointer',
    'Buffer',
    'Array',
    'comptime',
    'address_of',
    'unroll',
    'static_assert',
    'type_of_opt',
    'typeof',
    "dispatch_id",
    "thread_id",
    "block_id",
]
