from typing_extensions import TypeAliasType
from typing import (
    Callable,
    Optional,
    TypeAlias,
    TypeVar,
    Union,
    Generic,
    Literal,
    overload,
    Any,
)


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


def dataclass(cls: type, align: Optional[int] = None) -> type:
    """
    Mark a class as a DSL struct.

    Example:
    ```python
    @luisa.dataclass
    class Sphere:
        center: luisa.float3
        radius: luisa.float

        def volume(self) -> float:
            return 4.0 / 3.0 * math.pi * self.radius ** 3
    ```
    """
    return cls


struct = dataclass


def kernel(func: KernelType, *args, **kwargs) -> KernelType:
    return func


class InoutMarker:
    value: str

    def __init__(self, value: str):
        self.value = value


inout = InoutMarker("inout")
out = InoutMarker("out")


def func(func: F, *args, **kwargs) -> F:
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
    return func


class CommonArithOps(Generic[T, Scalar]):
    def __init__(self, value: Scalar) -> None:
        return _intrinsic_impl()

    def __add__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __radd__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __sub__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __rsub__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __mul__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __rmul__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __mod__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __rmod__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __pow__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __rpow__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()


class IntArithOps(Generic[T, Scalar, Float]):
    def __truediv__(self: T, other: Scalar | T) -> Float:
        return _intrinsic_impl()

    def __rtruediv__(self: T, other: Scalar | T) -> Float:
        return _intrinsic_impl()

    def __floordiv__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __rfloordiv__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()


class FloatTypeMarker:
    pass


class MathIntrinsics(Generic[T]):
    def sin(self: T) -> T:
        return _intrinsic_impl()

    def cos(self: T) -> T:
        return _intrinsic_impl()

    def tan(self: T) -> T:
        return _intrinsic_impl()

    def asin(self: T) -> T:
        return _intrinsic_impl()

    def acos(self: T) -> T:
        return _intrinsic_impl()

    def atan(self: T) -> T:
        return _intrinsic_impl()

    def atan2(self: T, other: T) -> T:
        return _intrinsic_impl()

    def sinh(self: T) -> T:
        return _intrinsic_impl()

    def cosh(self: T) -> T:
        return _intrinsic_impl()

    def tanh(self: T) -> T:
        return _intrinsic_impl()


class FloatArithOps(Generic[T, Scalar], FloatTypeMarker):
    def __truediv__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __rtruediv__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __floordiv__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()

    def __rfloordiv__(self: T, other: Scalar | T) -> T:
        return _intrinsic_impl()


@_builtin_type
class u8(CommonArithOps["u8", int]):
    pass


@_builtin_type
class u16(CommonArithOps["u16", int]):
    pass


@_builtin_type
class u32(CommonArithOps["u32", int]):
    pass


@_builtin_type
class u64(CommonArithOps["u64", int]):
    pass


@_builtin_type
class i8(CommonArithOps["i8", int]):
    pass


@_builtin_type
class i16(CommonArithOps["i16", int]):
    pass


@_builtin_type
class i32(CommonArithOps["i32", int]):
    pass


@_builtin_type
class i64(CommonArithOps["i64", int]):
    pass


class Vector2Base(Generic[Scalar]):
    x: Scalar
    y: Scalar

    @overload
    def __init__(self, x: Scalar): ...
    @overload
    def __init__(self, x: Scalar, y: Scalar): ...
    def __init__(self, *args, **kwargs) -> None:
        return _intrinsic_impl()


class Vector3Base(Generic[Scalar]):
    x: Scalar
    y: Scalar
    z: Scalar

    @overload
    def __init__(self, x: Scalar): ...
    @overload
    def __init__(self, x: Scalar, y: Scalar): ...
    @overload
    def __init__(self, x: Scalar, y: Scalar, z: Scalar): ...
    def __init__(self, *args, **kwargs) -> None:
        return _intrinsic_impl()


class Vector3Cross(Generic[T]):
    @_builtin
    def cross(self: T, other: T) -> T:
        return _intrinsic_impl()


class Vector4Base(Generic[Scalar]):
    x: Scalar
    y: Scalar
    z: Scalar
    w: Scalar

    @overload
    def __init__(self, x: Scalar): ...
    @overload
    def __init__(self, x: Scalar, y: Scalar): ...
    @overload
    def __init__(self, x: Scalar, y: Scalar, z: Scalar): ...
    @overload
    def __init__(self, x: Scalar, y: Scalar, z: Scalar, w: Scalar): ...
    def __init__(self, *args, **kwargs) -> None:
        return _intrinsic_impl()


class IntVector2(
    Generic[T, Scalar], Vector2Base[Scalar], CommonArithOps[T, Scalar | int]
):
    pass


class IntVector3(
    Generic[T, Scalar], Vector3Base[Scalar], CommonArithOps[T, Scalar | int]
):
    pass


class IntVector4(
    Generic[T, Scalar], Vector4Base[Scalar], CommonArithOps[T, Scalar | int]
):
    pass


class FloatVector2(
    Generic[T, Scalar],
    Vector2Base[Scalar],
    CommonArithOps[T, Scalar | int],
    FloatArithOps[T, Scalar],
):
    pass


class FloatVector3(
    Generic[T, Scalar],
    Vector3Base[Scalar],
    CommonArithOps[T, Scalar | int],
    FloatArithOps[T, Scalar],
    Vector3Cross[T],
):
    pass


class FloatVector4(
    Generic[T, Scalar],
    Vector4Base[Scalar],
    CommonArithOps[T, Scalar | int],
    FloatArithOps[T, Scalar],
):
    pass


class int2(IntVector2["int2", i32]):
    pass


class int3(IntVector3["int3", i32]):
    pass


class int4(IntVector4["int4", i32]):
    pass


class uint2(IntVector2["uint2", u32]):
    pass


class uint3(IntVector3["uint3", u32]):
    pass


class uint4(IntVector4["uint4", u32]):
    pass


class long2(IntVector2["long2", i64]):
    pass


class long3(IntVector3["long3", i64]):
    pass


class long4(IntVector4["long4", i64]):
    pass


class ulong2(IntVector2["ulong2", u64]):
    pass


class ulong3(IntVector3["ulong3", u64]):
    pass


class ulong4(IntVector4["ulong4", u64]):
    pass


Element = TypeVar("Element")


class Buffer(Generic[Element]):
    def __getitem__(self, index: u32 | u64) -> Element:
        return _intrinsic_impl()

    def __setitem__(self, index: u32 | u64, value: Element) -> None:
        return _intrinsic_impl()

    def __len__(self) -> u32 | u64:
        return _intrinsic_impl()


def constexpr(a: Any) -> Any:
    return a
