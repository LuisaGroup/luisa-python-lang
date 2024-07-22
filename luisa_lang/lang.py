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
from luisa_lang._math_type_exports import *
from luisa_lang._markers import _builtin_type, _builtin, _intrinsic_impl
import ast

_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Any])
_KernelType = TypeVar("_KernelType", bound=Callable[..., None])


class _ObjKind(Enum):
    STRUCT = auto()
    FUNC = auto()
    KERNEL = auto()


def _dsl_decorator_impl(obj: _T, kind: _ObjKind, attrs: Dict[str, Any]) -> _T:
    import sourceinspect
    obj_src = sourceinspect.getsource(obj)
    obj_ast = ast.parse(obj_src)
    if kind == _ObjKind.STRUCT:
        return obj
    elif kind == _ObjKind.FUNC or kind == _ObjKind.KERNEL:
        assert callable(obj)
        func_globals = getattr(obj, "__globals__", None)
        if kind == _ObjKind.FUNC:

            def dummy(*args, **kwargs):
                raise RuntimeError("DSL function should only be called in DSL context.")

            return cast(_T, dummy)
        else:
            return cast(_T, obj)
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
    if len(args) == 1 and len(kwargs) == 0:
        f = args[0]
        return f

    def decorator(f):
        return f

    return decorator


@_builtin_type
class Buffer(Generic[_T]):
    def __getitem__(self, index: int | u32 | u64) -> _T:
        return _intrinsic_impl()

    def __setitem__(self, index: int | u32 | u64, value: _T) -> None:
        return _intrinsic_impl()

    def __len__(self) -> u32 | u64:
        return _intrinsic_impl()


@_builtin_type
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
