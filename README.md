# luisa-python-lang (WIP)
A new Python DSL frontend for LuisaCompute. Will be integrated into LuisaCompute python package once it's ready.

## Introduction

```python
import luisa_lang as lc

@lc.struct
class AABB:
    min: lc.float3
    max: lc.float3

    @lc.trace
    def __init__(self, min: lc.float3, max: lc.float3):
        self.min = min
        self.max = max

    @lc.trace
    def size(self) -> lc.float3:
        return self.max - self.min


# create a struct instance on the host
aabb = AABB(lc.float3(0.0, 0.0, 0.0), lc.float3(1.0, 1.0, 1.0))
# you can call the method on the host
size = aabb.size()


```


## Basic Syntax
### Types
#### Scalar types:
Scalar types are immutable and passed by value. They can be used in arithmetic operations, comparisons, and other expressions. LuisaCompute supports the following scalar types:
- `lc.i8`, `lc.int8`, `lc.byte`, lc.ubyte`: 8-bit signed and unsigned integers.
- `lc.i16`, `lc.int16`, `lc.short`, `lc.ushort`: 16-bit signed and unsigned integers.
- `lc.i32`, `lc.int32`, `lc.int`, `lc.uint`: 32-bit signed and unsigned integers.
- `lc.i64`, `lc.int64`, `lc.long`, `lc.ulong`: 64-bit signed and unsigned integers.
- `lc.bool`: Boolean type.
- `lc.f32`, `lc.float`, `lc.f64`, `lc.double`: Floating point types.

#### Vector types
Compound types such as vectors and matrices are mutable and passed by reference. LuisaCompute supports the following vector types:
- `lc.byte2`, `lc.byte3`, `lc.byte4`: 2, 3, and 4-component byte vectors.
- `lc.ubyte2`, `lc.ubyte3`, `lc.ubyte4`: 2, 3, and 4-component unsigned byte vectors.
- `lc.short2`, `lc.short3`, `lc.short4`: 2, 3, and 4-component signed short vectors.
- `lc.ushort2`, `lc.ushort3`, `lc.ushort4`: 2, 3, and 4-component unsigned short vectors.
- `lc.int2`, `lc.int3`, `lc.int4`: 2, 3, and 4-component signed integer vectors.
- `lc.uint2`, `lc.uint3`, `lc.uint4`: 2, 3, and 4-component unsigned integer vectors.
- `lc.long2`, `lc.long3`, `lc.long4`: 2, 3, and 4-component signed long vectors.
- `lc.ulong2`, `lc.ulong3`, `lc.ulong4`: 2, 3, and 4-component unsigned long vectors.
- `lc.float2`, `lc.float3`, `lc.float4`: 2, 3, and 4-component floating point vectors.
- `lc.double2`, `lc.double3`, `lc.double4`: 2, 3, and 4-component double precision floating point vectors.

#### Matrix types
- `lc.float2x2`, `lc.float3x3`, `lc.float4x4`: 2x2, 3x3, and 4x4 floating point matrices.
- `lc.double2x2`, `lc.double3x3`, `lc.double4x4`: 2x2, 3x3, and 4x4 double precision floating point matrices.

#### User-defined structs
`lc.struct`: Used to define user-defined types (similar to C structs). Fields can be of any type, including other structs, vectors, and matrices. Structs are passed by reference, and can be instantiated on both the host and device. However, assigning to struct fields copies the value into the struct, in contrast to ordinary Python objects where assignment is by reference.

Example:
```python
@lc.struct
class MyStruct:
    a: lc.int
    b: lc.float3
    c: lc.double4x4

    @lc.trace
    def __init__(self, a: lc.int, b: lc.float3, c: lc.double4x4):
        self.a = a
        self.b = b
        self.c = c
    
    def get_a(self) -> lc.int:
        return self.a

# struct can be instantiated on the host or device
s = MyStruct(42, lc.float3(1.0, 2.0, 3.0), lc.double4x4.identity())
a = s.get_a()  # Call method on the host as well
v = float3(1.0, 2.0, 3.0) + s.b  # Vector addition
# assigning to struct field COPIES the value into the struct
s.b = v

```

### Value and Reference Semantics
To ensure the host and device code behave consistently, LuisaCompute uses a mix of value and reference semantics for different types that largely resembles Python's behavior but with some differences:
In LuisaCompute, scalar types are passed by value, meaning that when you pass a scalar to a function or assign it to another variable, a copy is made. In contrast, compound types (vectors, matrices, and structs) are passed by reference, meaning that when you pass them to a function or assign them to another variable, the reference to the original object is used, not a copy. However, when you assign a value to a field of a struct, the value is copied into the struct.