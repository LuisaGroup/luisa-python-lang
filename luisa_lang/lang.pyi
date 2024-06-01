# for compiler internal use only
from typing import TypeVar, Union, Generic, Literal, overload

def lcpyc(*args, **kwargs): ...
@lcpyc("builtin_type")
class u16(int):
    pass

@lcpyc("builtin_type")
class u32(int):
    pass

@lcpyc("builtin_type")
class u64(int):
    pass

@lcpyc("builtin_type")
class i16(int):
    pass

@lcpyc("builtin_type")
class i32(int):
    pass

@lcpyc("builtin_type")
class i64(int):
    pass

@lcpyc("builtin_type")
class f32(float):
    pass

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
    @overload
    def __add__(
        self, other: Vector[Primitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __add__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    def __radd__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    @overload
    def __sub__(
        self, other: Vector[Primitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __sub__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    def __rsub__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    @overload
    def __mul__(
        self, other: Vector[Primitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __mul__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    def __rmul__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    @overload
    def __truediv__(
        self, other: Vector[Primitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __truediv__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    def __rtruediv__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    @overload
    def __floordiv__(
        self, other: Vector[Primitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __floordiv__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    def __rfloordiv__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    @overload
    def __mod__(
        self, other: Vector[Primitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __mod__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    def __rmod__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    @overload
    def __pow__(
        self, other: Vector[Primitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __pow__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    def __rpow__(self, other: Primitive) -> Vector[Primitive, VecLen]: ...
    @overload
    def __lshift__(
        self: Vector[IntPrimitive, VecLen], other: Vector[IntPrimitive, VecLen]
    ) -> Vector[IntPrimitive, VecLen]: ...
    @overload
    def __lshift__(
        self: Vector[IntPrimitive, VecLen], other: IntPrimitive
    ) -> Vector[IntPrimitive, VecLen]: ...
    def __rlshift__(
        self: Vector[IntPrimitive, VecLen], other: IntPrimitive
    ) -> Vector[IntPrimitive, VecLen]: ...
    @overload
    def __rshift__(
        self: Vector[IntPrimitive, VecLen], other: Vector[IntPrimitive, VecLen]
    ) -> Vector[Primitive, VecLen]: ...
    @overload
    def __rshift__(
        self: Vector[IntPrimitive, VecLen], other: IntPrimitive
    ) -> Vector[Primitive, VecLen]: ...
    def dot(self, other: Vector[Primitive, VecLen]) -> Primitive: ...
    def cross(
        self: Vector[Primitive, Literal[3]], other: Vector[Primitive, Literal[3]]
    ) -> Vector[Primitive, Literal[3]]: ...
    def reduce_and(self) -> Primitive: ...
    def reduce_or(self) -> Primitive: ...
    def reduce_xor(self) -> Primitive: ...
    def reduce_sum(self) -> Primitive: ...
    def reduce_prod(self) -> Primitive: ...

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

class Buffer(Generic[Element]):
    def __getitem__(self, index: u32 | u64) -> Element: ...
    def __setitem__(self, index: u32 | u64, value: Element) -> None: ...
    def __len__(self) -> u32 | u64: ...
