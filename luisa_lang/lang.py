from typing_extensions import TypeAliasType
from typing import TypeAlias, TypeVar, Union, Generic, Literal, overload, Any


def lcpyc(*args, **kwargs):
    def decorator(func):
        return func

    return decorator


def intrinsic_impl(*args, **kwargs) -> Any:
    raise NotImplementedError(
        "intrinsic functions should not be called in normal Python code"
    )


u16 = TypeAliasType("u16", int)
u32 = TypeAliasType("u32", int)
u64 = TypeAliasType("u64", int)
i16 = TypeAliasType("i16", int)
i32 = TypeAliasType("i32", int)
i64 = TypeAliasType("i64", int)
f32 = TypeAliasType("f32", float)
f64 = TypeAliasType("f64", float)

Primitives = Union[u16, u32, u64, i16, i32, i64, f32]
Primitive = TypeVar("Primitive", bound=Primitives)
IntPrimitives = Union[u16, u32, u64, i16, i32, i64]
IntPrimitive = TypeVar("IntPrimitive", bound=IntPrimitives)
FloatPrimitives = Union[f32]
FloatPrimitive = TypeVar("FloatPrimitive", bound=FloatPrimitives)
VecLen = TypeVar("VecLen")


class Vector(Generic[Primitive, VecLen]):
    @overload
    def __init__(self, x: Primitive) -> None: ...
    @overload
    def __init__(self, x: Primitive, y: Primitive) -> None: ...
    @overload
    def __init__(self, x: Primitive, y: Primitive, z: Primitive) -> None: ...
    @overload
    def __init__(
        self, x: Primitive, y: Primitive, z: Primitive, w: Primitive
    ) -> None: ...
    def __init__(self, *args, **kwargs) -> None:
        intrinsic_impl()

    def __add__(
        self, other: Primitive | "Vector[Primitive, VecLen]"
    ) -> "Vector[Primitive, VecLen]":
        return intrinsic_impl()

    def __radd__(self, other: Primitive) -> "Vector[Primitive, VecLen]":
        return intrinsic_impl()

    def __sub__(
        self, other: Primitive | "Vector[Primitive, VecLen]"
    ) -> "Vector[Primitive, VecLen]":
        return intrinsic_impl()

    def __rsub__(self, other: Primitive) -> "Vector[Primitive, VecLen]":
        return intrinsic_impl()

    def __mul__(
        self, other: Primitive | "Vector[Primitive, VecLen]"
    ) -> "Vector[Primitive, VecLen]":
        return intrinsic_impl()

    def __rmul__(self, other: Primitive) -> "Vector[Primitive, VecLen]":
        return intrinsic_impl()

    def dot(self, other: "Vector[Primitive, VecLen]") -> Primitive:
        return intrinsic_impl()

    def cross(
        self: "Vector[Primitive, Literal[3]]", other: "Vector[Primitive, Literal[3]]"
    ) -> "Vector[Primitive, Literal[3]]":
        return intrinsic_impl()

    def reduce_and(self) -> Primitive:
        return intrinsic_impl()

    def reduce_or(self) -> Primitive:
        return intrinsic_impl()

    def reduce_xor(self) -> Primitive:
        return intrinsic_impl()

    def reduce_sum(self) -> Primitive:
        return intrinsic_impl()

    def reduce_prod(self) -> Primitive:
        return intrinsic_impl()


float2 = Vector[f32, Literal[2]]
float3 = Vector[f32, Literal[3]]
float4 = Vector[f32, Literal[4]]
int2 = Vector[i32, Literal[2]]
int3 = Vector[i32, Literal[3]]
int4 = Vector[i32, Literal[4]]
uint2 = Vector[u32, Literal[2]]
uint3 = Vector[u32, Literal[3]]
uint4 = Vector[u32, Literal[4]]

Element = TypeVar("Element")


# class Buffer(Generic[Element]):
#     def __getitem__(self, index: u32 | u64) -> Element: ...
#     def __setitem__(self, index: u32 | u64, value: Element) -> None: ...
#     def __len__(self) -> u32 | u64: ...
