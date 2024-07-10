from typing_extensions import TypeAliasType
from typing import (
    Callable,
    Optional,
    Sequence,
    TypeAlias,
    TypeVar,
    Union,
    Generic,
    Literal,
    overload,
    Any,
)
from luisa_lang._math_type_exports import *

T = TypeVar("T")
Scalar = TypeVar("Scalar")
Float = TypeVar("Float")
Int = TypeVar("Int")
ScalarLiteral = TypeVar("ScalarLiteral", int, float)
F = TypeVar("F", bound=Callable[..., Any])
KernelType = TypeVar("KernelType", bound=Callable[..., None])
Self = TypeVar("Self")


def _dsl_decorator_impl(any: T, is_builtin: bool) -> T:
    env = globals()
    if type(any) == type:
        # is a class
        pass
    elif callable(any):
        # is a function
        pass
    return any


def _builtin_type(any: T, *args, **kwargs) -> T:
    return any


def _builtin(func: F, *args, **kwargs) -> F:
    return func


def _intrinsic_impl(*args, **kwargs) -> Any:
    raise NotImplementedError(
        "intrinsic functions should not be called in normal Python code"
    )


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
def kernel(f: KernelType) -> KernelType: ...
@overload
def kernel(export: bool = False, **kwargs) -> Callable[[KernelType], KernelType]: ...
def kernel(*args, **kwargs) -> KernelType | Callable[[KernelType], KernelType]:
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
def func(f: F) -> F: ...
@overload
def func(inline: bool | Literal["always"] = False, **kwargs) -> Callable[[F], F]: ...
def func(*args, **kwargs) -> F | Callable[[F], F]:
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


Element = TypeVar("Element")


class Buffer(Generic[Element]):
    def __getitem__(self, index: int | u32 | u64) -> Element:
        return _intrinsic_impl()

    def __setitem__(self, index: int | u32 | u64, value: Element) -> None:
        return _intrinsic_impl()

    def __len__(self) -> u32 | u64:
        return _intrinsic_impl()


@_builtin
def consteval(a: Any) -> Any:
    return a


@_builtin
def device_log(_: Any):
    pass


def static_assert(cond: Any, msg: str = ""):
    pass


def unroll(range_: Sequence[int]) -> Sequence[int]:
    return range_
