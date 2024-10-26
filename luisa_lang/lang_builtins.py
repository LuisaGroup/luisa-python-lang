from typing_extensions import TypeAliasType
from luisa_lang.lang import _builtin, _intrinsic_impl
from luisa_lang.lang import *

_T = TypeVar("_T")


@_builtin
def dispatch_id() -> uint3:
    return _intrinsic_impl()


@_builtin
def thread_id() -> uint3:
    return _intrinsic_impl()


@_builtin
def block_id() -> uint3:
    return _intrinsic_impl()


class ConstexprBlock:
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self):
        pass


class _ConstexprBlockMarker:
    pass


@overload
def constexpr(a: _ConstexprBlockMarker) -> ConstexprBlock: ...


@overload
def constexpr(a: _T) -> _T: ...


def constexpr(a: _T | _ConstexprBlockMarker = _ConstexprBlockMarker()) -> Union[_T, ConstexprBlock]:
    """
    Allowing mixing normal python object as compile-time value with DSL code.
    Usage:
        - `lc.constexpr(e)` marks the expression `e` as a compile-time value.
        - `with lc.constexpr() as block: ...` marks the block as a compile-time block.
    """
    if isinstance(a, _ConstexprBlockMarker):
        return ConstexprBlock()
    return a


@_builtin
def device_log(_: Any):
    pass


def static_assert(cond: Any, msg: str = ""):
    pass


def unroll(range_: Sequence[int]) -> Sequence[int]:
    return range_


@_builtin
def address_of(a: _T) -> Pointer[_T]:
    return _intrinsic_impl()

# class StaticEval:
#
