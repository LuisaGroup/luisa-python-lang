# luisa-python-lang (WIP)
A new Python DSL frontend for LuisaCompute. Will be integrated into LuisaCompute python package once it's ready.

## Content
- [Introduction](#introduction)
- [Basics](#basic-syntax)
    - [Types](#types)
    - [Functions](#functions)
    - [User-defined Structs](#user-defined-structs)
    - [Value Semantics](#value-semantics)
    - [Local References](#local-references)
    - [Control Flow](#control-flow)
    - [Accessing Host Types](#accessing-host-types)
- [Advanced Usage](#advanced-syntax)
    - [Generics](#generics)
    - [Metaprogramming](#metaprogramming)
    - [User-defined Builtins](#user-defined-builtins)
    - [Standalone Compilation](#standalone-compilation)


## Introduction
```python
import luisa_lang as lc
```
## Basic Syntax

### Types
LuisaCompute supports the following core types:
```python
# scalar:
lc.i8, lc.i16, lc.i32, lc.i64, lc.u8, lc.u16, lc.u32, lc.u64, lc.f32, lc.f64, lc.bool
# vector types for each scalar type:
lc.int2, lc.int3, lc.int4, ...

# matrix types:
lc.float2x2, lc.float3x3, lc.float4x4

# fixed-size array:
lc.Array[T, Literal[10]] # T is the element type, N is the size

# Pointer:
lc.Ptr[T]

# Local (logical) reference
lc.Ref[T]

```

### Functions
Functions can be defined in two ways. The first way is to use the `@lc.trace` decorator. Each time the function is called, it will generate a trace of DSL code, in a spirit similar to `torch.jit.trace`. Different from `torch.jit.trace`, the function body can contain any valid LuisaCompute code, including arbitrary control flows. You can also include normal Python code that will be executed at DSL comile time that is guarded behind `lc.static(). (See [Metaprogramming](#metaprogramming) for more details). 

**Note**: In tracing mode, each function should have only one return statement. 

```python
@lc.trace
def add(a: lc.float, b: lc.float) -> lc.float:
    if lc.static(True):
        print('tracing add function')
    return a + b

# call the function
c = add(1.0, 2.0) 
d = add(3.0, c)
# will print 'tracing add function' twice
```
One downside of using `@lc.trace` is that the function body will be duplicated each time it is called. This can lead to code bloat if the function is called many times. To avoid this, you can use the `@lc.func` decorator. The function body will be compiled only once and reused each time the function is called. 

```python
@lc.func
def add(a: lc.float, b: lc.float) -> lc.float:
    if lc.static(True):
        print('compiliing add function')
    return a + b

# call the function
c = add(1.0, 2.0)
d = add(3.0, c)
# will print 'compiling add function' only once
```


### User-defined Structs
```python
@lc.struct
class Sphere:
    center: lc.float3
    radius: lc.float

    @lc.func
    def __init__(self, center: lc.float3, radius: lc.float):
        self.center = center
        self.radius = radius

    @lc.trace
    def volume(self) -> lc.float:
        return 4.0 / 3.0 * 3.1415926 * self.radius ** 3
```


### Value Semantics
Variables have value semantics by default. This means that when you assign a variable to another, a copy is made.
```python
a = lc.float3(1.0, 2.0, 3.0)
b = a
a.x = 2.0
print(f'{a.x} {b.x}') # prints 2.0 1.0
```

#### Local References
There is a logical reference type `lc.Ref[T]` that can be used to pass a value by reference, similar to `inout` in GLSL/HLSL. The value can be accessed through the `val` attribute. 
```python
@luisa.func
def swap(a: lc.Ref[lc.float], b: lc.Ref[lc.float]):
    a.val, b.val = b.val, a.val

a = lc.float3(1.0, 2.0, 3.0)
b = lc.float3(4.0, 5.0, 6.0)
swap(lc.Ref(a.x), lc.Ref(b.x))
lc.print(f'{a.x} {b.x}') # prints 4.0 1.0
```
However, `lc.Ref[T]` is more powerful than `inout` in GLSL/HLSL. You can even return a reference from a function and use it later (only available in `@lc.trace` functions).

```python
@lc.trace
def get_ref(a: lc.float3) -> lc.Ref[lc.float]:
    return a.x

a = lc.float3(1.0, 2.0, 3.0)
b = get_ref(a))
b.val = 2.0
lc.print(f'{a.x} {b.val}') # prints 2.0 2.0
```

**Important**: `lc.Ref[T]` is not a true reference type nor a pointer. It is a logical reference that is resolved at compile time. This means that you cannot store a `lc.Ref[T]` in an aggregate type, such as an array or a struct. You also cannot define a local reference inside non-uniform control flow such as `if` or `for` statements. See the following example for the semantics of local references.
```python
a: lc.Ref[T] = some_ref_func() # a is bound to the reference returned by some_ref_func()
if cond():
    a.val = another_ref_func() # # OK, update the value of the reference
    b: lc.Ref[T] = another_ref_func() # error, cannot define a local reference inside non-uniform control flow
    # to workaround the above issue, you should define a new scope

    @lc.trace
    def inner():
        b: lc.Ref[T] = another_ref_func() # OK
        # do something with b
    inner()
```

### Control Flow
```python
# the following control flow constructs are supported
if cond:
    pass
elif cond:
    pass
else:
    pass

while cond:
    pass

for i in lc.range(10):
    pass
```

### Accessing Host Types
Each DSL type has a corresponding native host type that can be accessed through the `dtype` attribute. The host type is a struct that contains the same fields and as the DSL type. You can use the host type to pass data between the host and the DSL code. 

```python
class Sphere:
    center: lc.float3
    radius: lc.float

# explicitly using the host type
a = Sphere.dtype(center=lc.float3.dtype(1.0, 2.0, 3.0), radius=1.0)
# outside lc.trace and lc.func, the above line is equivalent to
a = Sphere(center=lc.float3(1.0, 2.0, 3.0), radius=1.0) 
assert isinstance(a, Sphere.dtype)
```

### Generics
Generic types and functions are supported. However, generic type constraints are not checked as type checking are only done during instantiation. 
```python
class Point2D[T]:
    x: T
    y: T

@lc.func
def add_point(a: Point2D[T], b: Point2D[T]) -> Point2D[T]:
    return Point2D(a.x + b.x, a.y + b.y)

@lc.func
def apply_func(f: Callable[[T], T], x: T) -> T:
    return f(x)

@lc.func
def make_type(t: type[T], *args) -> T:
    return t(*args)
```


### Metaprogramming
We provide a flexible approach to metaprogramming by allowing users to mix Python code and DSL code. DSL variables can be stored in Python variables, and users can use this to build computation graph dynamically. 

```python
# Compile time reflection
@lc.func
def get_x_or_zero(x: Any):
    t = type(x)
    if lc.static(hasattr(t, 'x')):
        return x.x
    else:
        return 0.0

@lc.func
def powi(x: lc.float, n: int) -> lc.float: # pass in n as a native python type
    p = lc.float(1.0)
    for i in lc.static(range(n)): # lc.static() is to hint that the control flow can be determined at compile time
        p = p * x
    return p

powi(x, 3) # would unroll the loop 3 times

@lc.func
def dispatch_func(tag: lc.int, funcs: List[Callable[[Any], Any]], x: Any) -> Any:
    with lc.switch(tag) as s:
        for i in lc.static(range(len(funcs))):
            with s.case(i):
                return funcs[i](x)

```


### Limitation & Caveats


### Standalone Compiler
It is possible to retarget luisa_lang to serve as another DSL. For example, one may want to use it as a customized shader language different from what LuisaCompute provides, or use it to generate customized C++/CUDA source. In this case, one can use the standalone compiler to compile the luisa_lang code into a standalone shader file.

```python
```