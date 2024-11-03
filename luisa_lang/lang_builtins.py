from typing import Any, Generic, List, Optional, Sequence, TypeVar, overload
from typing_extensions import TypeAliasType
from luisa_lang.lang import _builtin, _intrinsic_impl
from luisa_lang.math_types import *
import luisa_lang.hir as hir

_T = TypeVar("_T")
_N = TypeVar("_N")

@_builtin
def dispatch_id() -> uint3:
    return _intrinsic_impl()


@_builtin
def thread_id() -> uint3:
    return _intrinsic_impl()


@_builtin
def block_id() -> uint3:
    return _intrinsic_impl()


@_builtin
def convert(target: type[_T], value: Any) -> _T:
    """
    Attempt to convert the value to the target type.
    """
    return _intrinsic_impl()


@_builtin
def bitcast(target: type[_T], value: Any) -> _T:
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


@overload
def comptime(a: _ComptimeBlockMarker) -> ComptimeBlock: ...


@overload
def comptime(src: str) -> Any: ...


@overload
def comptime(a: _T) -> _T: ...


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


@_builtin
def device_log(_: Any):
    pass


def static_assert(cond: Any, msg: str = ""):
    pass


def unroll(range_: Sequence[int]) -> Sequence[int]:
    return range_


@_builtin
def address_of(a: _T) -> 'Pointer[_T]':
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


__all__: List[str] = [
    'Pointer',
    'Buffer',
    'Array',
    'comptime',
    'device_log',
    'address_of',
    'unroll',
    'static_assert',
    'type_of_opt',
    'typeof',
]
