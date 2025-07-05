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

device = = lc.Device('cuda')  # or 'cpu', 'metal', etc.
buf_aabb = device.create_buffer(AABB, 1)  # create a buffer to hold the struct on the device
buf_aabb[0] = aabb  # copy the struct to the device buffer
buf_size = device.create_buffer(lc.float3, 1)  # create a buffer to hold the size on the device

@lc.kernel
def compute_aabb_size(aabb_buf: lc.Buffer[AABB], size_buf: lc.Buffer[lc.float3]):
    i = lc.dispatch_id().x
    aabb = aabb_buf[i]
    size_buf[i] = aabb.size()  # call the method on the device

stream = device.create_stream()  # create a stream to execute the kernel
stream.submit([
    compute_aabb_size(buf_aabb, buf_size).dispatch(1)
]).synchronize()  # submit the kernel to the stream and wait for it to finish

print(f"AABB size: {buf_size[0]}")  # print the size of the AABB on the host
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
    lc.print(new_a)  # Should print 11
    lc.print(s.a)  # Should also print 11, as 's' is modified by reference
    lc.print(i) # should print 5 since scalars are passed by value and immutable

```

#### Dynamic and Static Control Flow

#### Assignment Behavior ####
The semantics of assignment operator `=` is the same as in Python: when assinging to immutable types (scalars), the value is copied into the variable, while for mutable types (vectors, matrices, structs), the reference is copied. The only difference is that when assigning to a field of a struct, the value is copied into the struct.
However, not all references can be implemented on GPU. LuisaCompute would detect such case and ask to to rewrite such assignment by explicitly copying the value using `lc.copy()` function. 

The behavior can be summarize in the following table:

| Type        | Assignment | Field/Index Assignment | Function Argument Passing | `@lc.trace` Return | `@lc.func` Return |
|-------------|------------|------------------------|---------------------------|-----------------|-------------|
| Python Object | Reference   | Reference              | Reference                 | Reference       | Reference |
| Scalar (e.g. lc.int) | Value       | N/A                  | Value                     | Value           | Value   |
| Compound Type (e.g. lc.float3, lc.float4x4) | Reference   | Copy              | Reference                 | Reference | Value |


Let's take a look at an example:

```python
@lc.kernel
def assignment_example():
    s = MyStruct(10, lc.float3(1.0, 2.0, 3.0))
    v = lc.float3(4.0, 5.0, 6.0)
    t = s # t is a reference to s as in Python
    t.b = v # v is copied into t.b.
    v.x += 1.0
    lc.print(t.b, s.b) # should print (4.0, 5.0, 6.0) twice
    lc.print(v) # should print (5.0, 5.0, 6.0)
    t2 = lc.copy(s) # t2 is a copy of s, not a reference
    t2.a += 1
    lc.print(t2.a, s.a) # should print 11, 10
```

#### Transient vs Persistent Values
Values in LuisaCompute can be categorized into transient and persistent values. Transient values are similar to rvalues in C++, meaning that they are temporarily created and hasn't bind to any variable yet. Persistent values are similar to lvalues in C++, meaning that they are bound to a variable and can be used as assignment target.

Since phyiscal reference might be supported on GPU, it is not possible to dynamically create reference to persistent values,
for example
```python
@lc.kernel
def transient_vs_persistent():
    v1 = lc.float3(1.0, 2.0, 3.0)
    v2 = lc.float3(4.0, 5.0, 6.0)

    # the following code is allowed since both `v1 + 1.0` and `v2 + 1.0` are transient values.
    if dynamic_cond:
        dynamic = v1 + 1.0
    else:
        dynamic = v2 + 1.0
        
    # the following code is not allowed since such dynamically created reference to persitent values cannot be implemented on GPU:
    if dynamic_cond:
        dynamic = v1
    else:
        dynamic = v2

    # instead, you can either use lc.copy() to create a copy of the struct:
    if dynamic_cond:
        dynamic = lc.copy(v1)
    else:
        dynamic = lc.copy(v2)

    # or use a static condition:
    if lc.comptime(cond):
        dynamic = v1
    else:
        dynamic = v2

```

### Functions and Methods
Functions and methods in LuisaCompute are defined using the `@lc.func` or `@lc.trace` decorators. Both decorator transforms the python function into a LuisaCompute function that can be executed on both host (native Python) and device (LuisaCompute backend). The difference is that `@lc.trace` **inline**s the function body into the caller each time it is called, while `@lc.func` creates a separate function on the device.

In terms of usage, `@lc.trace` has a minor restriction on dynamic control flow (only a single dynamic return statement is allowed) while `@lc.func` has no restrictions. However, `@lc.trace` allows you to return references to variables, while `@lc.func` does not (since it is not possible to return reference to a local variable on device).

| Decorator   | Inline Function Body | Dynamic Control Flow Restrictions | Multiple Return Statement | Return Refences| Example Usage |
|-------------|----------------------|-----------------------------------|---------------------------|----------------|--------------|
| `@lc.func`  | No                   | Any control flow is allowed                                | Multiple returns allowed | No|Use for larger functions or when dynamic control flow is needed |
| `@lc.trace` | Yes                  | Cannot have dynamic return statement within dynamic loops                               | Single dynamic return statement only. Multiple static return statements allowed (statements guarded under `if lc.comptime(...)`| Yes |Use for small functions or when performance is critical |
| `@lc.kernel` | No                  | No                               | Multiple returns allowed. Cannot return values | No | Entry point for compute kernels |




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

### Kernel Lifecycle
```python

### Stage 1: Define the kernel
### At this strage, the kernel is just a normal Python function. Nothing has compiled yet. The `lc.kernel` decorator injects some code to aid compliation later.

type Op = Literal['+', '-', '*', '/']

@lc.kernel
def  vecop(a: lc.Buffer[lc.float3], b: lc.Buffer[lc.float3], c: lc.Buffer[lc.float3], op: Op):
    i = lc.dispatch_id().x
    va = a[i]
    vb = b[i]
    if lc.comptime(op == '+'):
        print('Adding vectors') # this line wil be executed during stage 2
        c[i] = va + vb
    elif lc.comptime(op == '-'):
        c[i] = va - vb
    elif lc.comptime(op == '*'):
        c[i] = va * vb
    elif lc.comptime(op == '/'):
        c[i] = va / vb
    else:
        raise ValueError(f"Unsupported operation: {op}")

### Stage 2: Kernel Instantiation and Symbolic Tracing
### When you call the kernel, the compiler first replace all DSL variables in the argument with symolic variables (in this case, `a`, `b`, `c` are replaced with symbolic buffers), while normal Python variables are passed as is (in this case, `op` is a Python variable). The compiler then traces the kernel body and generates a computation graph that is specific to the provided arguments. 

compiled_kernel = vecop(buf_a, buf_b, buf_c, op='+')
# prints: Adding vectors

### In this case, the generate kernel looks like this:
@lc.kernel
def vecop_add(a: lc.Buffer[lc.float3], b: lc.Buffer[lc.float3], c: lc.Buffer[lc.float3]):
    i = lc.dispatch_id().x
    va = a[i]
    vb = b[i]
    c[i] = va + vb
### Note the other operations are removed since they are not used in this instantiation.

### Stage 3: Kernel Compilation
### After the specialized kernel is generated, it is sent to the backend for code generation. The resulting artifact can be then dispatched to the device for execution.
stream.submit([
    compiled_kernel.dispatch(1024) 
]).synchronize()

```

### Comptime Expressions
Compile time expression are directives to instruct the compiler to specialize the code based on the provided values duriung Stage 2 of the kernel lifecycle. 

```python
v: lc.bool = ...
if v:
    print("Since v is symbolic during Stage 2 compilation, this code will be included in the compiled kernel.")
else:
    print("This code will be included in the kernel as well since at this stage we are not sure if v is True or False.")

if lc.comptime(True):
    print("This code will be included in the compiled kernel.")
else:
    print("This code will be excluded from the compiled kernel.")

```
### PyTrees
PyTrees are containers that have a tree-like structure, where each leaf node can either be DSL type or a Python object. PyTrees are used to pass complex data structure to functions and kernels. The compiler will inspect the contents of the PyTree and generate specialized code according to the provided tree structure.

Let's take a look at an example of using PyTrees to pass a tree-like structure to a function:

```python
@lc.pytree
class MyTree:
    v: lc.float3
    arr: List[lc.int32]

# Mytree.arr is not a valid DSL type since normally you cannot use Python lists on GPU.
# However, you can still pass it to a function or kernel, as long as the length of the list remains constant inside the kernel.

@lc.func
def foo(tree: MyTree) -> lc.float3:
    s = lc.float3(0.0, 0.0, 0.0)
    # use lc.comptime to hint that len(tree.arr) is known at kernel compile time
    for i in lc.comptime(range(len(tree.arr))):
        s += tree.v * lc.float32(tree.arr[i])
    return s

tree1 = MyTree(lc.float3(1.0, 2.0, 3.0), [lc.int32(1), lc.int32(2), lc.int32(3)])
tree2 = MyTree(lc.float3(4.0, 5.0, 6.0), [lc.int32(4), lc.int32(5)])

# These two calls will generate two versions of the `foo` function internally, based on the length of the `arr` field in each tree.
foo(tree1)
foo(tree2)
```

## Exporting Functions to IR or C++ (AOT Compilation)


```python
@lc.func
def generic_add(a, b):
    return a + b

compiler = lc.Compiler(backend='cpp')
compiler.compile(generic_add, example_inputs=(lc.f32(1.0), lc.f32(2.0)))
compiler.output('add_f32.cpp')

```