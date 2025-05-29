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
#### Parameter Passing ####
To ensure the host and device code behave consistently, LuisaCompute uses a mix of value and reference semantics for different types that largely resembles Python's behavior but with some differences:
In LuisaCompute, scalar types are passed by value, meaning that when you pass a scalar to a function or assign it to another variable, a copy is made. In contrast, compound types (vectors, matrices, and structs) are passed by reference, meaning that when you pass them to a function or assign them to another variable, the reference to the original object is used, not a copy. However, when you assign a value to a field of a struct, the value is copied into the struct.

Let's take a look at some examples to illustrate this behavior:

```python
@lc.struct
class MyStruct:
    a: lc.int
    b: lc.float3

    @lc.trace
    def __init__(self, a: lc.int, b: lc.float3):
        self.a = a
        self.b = b


@lc.func # the semantics is the same for `@lc.func, @lc.trace`.
def inc_a(s: MyStruct, x: lc.int) -> lc.int:
    # This will modify the original struct's 'a' field
    s.a += 1
    x += 1
    return s.a


@lc.kernel
def kernel_example():
    s = MyStruct(10, lc.float3(1.0, 2.0, 3.0))
    i = lc.int(5)
    new_a = inc_a(s, i)  # This will modify 's.a' in the original struct
    print(new_a)  # Should print 11
    print(s.a)  # Should also print 11, as 's' is modified by reference
    print(i) # should print 5 since scalars are passed by value and immutable

```

#### Assignment Behavior ####
The semantics of assignment operator `=` is the same as in Python: when assinging to immutable types (scalars), the value is copied into the variable, while for mutable types (vectors, matrices, structs), the reference is copied. The only difference is that when assigning to a field of a struct, the value is copied into the struct.
However, not all references can be implemented on GPU. LuisaCompute would detect such case and ask to to rewrite such assignment by explicitly copying the value using `lc.copy()` function. For example:

```python
@lc.kernel
def kernel_example():
    s = MyStruct(10, lc.float3(1.0, 2.0, 3.0))
    v = lc.float3(4.0, 5.0, 6.0)
    t = s # t is a reference to s as in Python
    t.b = v # v is copied into t.b.
    v.x += 1.0
    print(t.b, s.b) # should print (4.0, 5.0, 6.0) twice
    print(v) # should print (5.0, 5.0, 6.0)
    t2 = lc.copy(s) # t2 is a copy of s, not a reference
    t2.a += 1
    print(t2.a, s.a) # should print 11, 10

    # the following code is not allowed since such dynamically created reference cannot be implemented on GPU:
    if dynamic_cond:
        dynamic = s
    else:
        dynamic = t2

    # instead, you can either use lc.copy() to create a copy of the struct:
    if dynamic_cond:
        dynamic = s
    else:
        dynamic = t2

    # or use a static condition:
    if lc.comptime(cond):
        dynamic = s
    else:
        dynamic = t2

```


### Functions and Methods
Functions and methods in LuisaCompute are defined using the `@lc.func` or `@lc.trace` decorators. Both decorator transforms the python function into a LuisaCompute function that can be executed on both host (native Python) and device (LuisaCompute backend). The difference is that `@lc.trace` **inline**s the function body into the caller each time it is called, while `@lc.func` creates a separate function on the device.

In terms of usage, `@lc.trace` has a minor restriction on dynamic control flow while `@lc.func` has no restrictions. However, `@lc.trace` on small functions is more efficient on the compiler side and would likely result in fast compilation time and better performance. Therefore, it is recommended to use `@lc.trace` for small functions and `@lc.func` for larger functions.

```python
# lc.func has no restrictions on dynamic control flow, so you can use it like this:
@lc.func
def my_abs(x: lc.float) -> lc.float:
    if x < 0.0:
        return -x
    else:
        return x

# However, lc.trace does not allow multiple returns, so the following code is not allowed:
@lc.trace
def my_abs_trace(x: lc.float) -> lc.float:
    if x < 0.0:
        return -x
    else:
        return x

# Instead, you can use a single return statement:
@lc.trace
def my_abs_trace(x: lc.float) -> lc.float:
    if x < 0.0:
        x = -x
    return x
```

#### Generic Functions
Technically, all functions in LuisaCompute are generic functions, meaning that they can accept arguments of any type. The compiler would instantiate the function upon the first call with the given types. The type hints of any LuisaCompute function are ignored by the compiler. However, you are encouraged to write type hints for better readability.

```python
def generic_add(a, b):
    return a + b

add(lc.f32(1.0), lc.f32(2.0))  # This will instantiate the function with f32 type
add(lc.int32(1), lc.int32(2))  # This will instantiate the function with int32 type

```

## Meta-Programming: Building Dynamic Computation Graph 
LuisaCompute has an excellent support for meta-programming, allowing you dynamically build your GPU program and computation graph in a natural and Pythonic way.

#### PyTrees


## Exporting Functions to IR or C++ (AOT Compilation)


```python
@lc.func
def generic_add(a, b):
    return a + b

compiler = lc.Compiler(backend='cpp')
compiler.compile(generic_add, example_inputs=(lc.f32(1.0), lc.f32(2.0)))
compiler.output('add_f32.cpp')

```