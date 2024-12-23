# luisa-python-lang (WIP)
A new Python DSL frontend for LuisaCompute. Will be integrated into LuisaCompute python package once it's ready.


## Content
- [Introduction](#introduction)
- [Basics](#basic-syntax)
    - [Difference from Python](#difference-from-python)
    - [Types](#types)
    - [Value & Reference Semantics](#value--reference-semantics)
    - [Functions](#functions)
    - [User-defined Structs](#user-defined-structs)
    - [Control Flow](#control-flow)
    - [Define DSL Operation for Non-DSL Types](#define-dsl-operation-for-non-dsl-types)
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
### Difference from Python
There are some notable differences between luisa_lang and Python:
- Variables have value semantics by default. Use `byref` to indicate that an argument that is passed by reference.
- Generic functions and structs are implemented via monomorphization (a.k.a instantiation) at compile time rather than via type erasure.
- Overloading subscript operator and attribute access is different from Python. Only `__getitem__` and `__getattr__` are needed, which returns a local reference.

### Types
```python
```

### Functions
Functions are defined using the `@lc.func` decorator. The function body can contain any valid LuisaCompute code. You can also include normal Python code that will be executed at DSL comile time using `lc.comptime()`. (See [Metaprogramming](#metaprogramming) for more details)

```python
@lc.func
def add(a: lc.float, b: lc.float) -> lc.float:
    with lc.comptime():
        print('compiliing add function')
    return a + b

```


### Value & Reference Semantics
Variables have value semantics by default. This means that when you assign a variable to another, a copy is made.
```python
a = lc.float3(1.0, 2.0, 3.0)
b = a
a.x = 2.0
lc.print(f'{a.x} {b.x}') # prints 2.0 1.0
```

You can use `byref` to indicate that a variable is passed as a *local reference*. Assigning to an `byref` variable will update the original variable.
```python
@luisa.func(a=byref, b=byref)
def swap(a: int, b: int):
    a, b = b, a

a = lc.float3(1.0, 2.0, 3.0)
b = lc.float3(4.0, 5.0, 6.0)
swap(a.x, b.x)
lc.print(f'{a.x} {b.x}') # prints 4.0 1.0
```

When overloading subscript operator or attribute access, you actually return a local reference to the object. 

#### Local References
Local references are like pointers in C++. However, they cannot escape the expression boundary. This means that you cannot store a local reference in a variable and use it later. While you can return a local reference from a function, it must be returned from a uniform path. That is you cannot return different local references based on a condition.


```python
@lc.struct
class InfiniteArray:
    def __getitem__(self, index: int) -> int:
        return self.data[index] # returns a local reference

    # this method will be ignored by the compiler. but you can still put it here for linting
    def __setitem__(self, index: int, value: int):
        pass

    # Not allowed, non-uniform return
    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.data[0]
        else:
            return self.data[1]

```





### User-defined Structs
```python
@lc.struct
class Sphere:
    center: lc.float3
    radius: lc.float
```

### Define DSL Operation for Non-DSL Types
Sometimes we want to use a non-DSL type in our DSL code. Such type could be imported from a third-party library or a built-in Python type. As long as we know the object layout, we can define the DSL operation for it by first defining a proxy struct that mirrors the object layout, and then define the operation for the proxy struct.

```python
# Assume we have a third-party library that defines a Vec3 class
class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

@lc.struct
class Vec3Proxy:
    x: lc.float
    y: lc.float
    z: lc.float

    # write DSL operations here

lc.register_dsl_type_alias(Vec3, Vec3Proxy)

@lc.func
def use_vec3(v: Vec3): # Vec3 is now treated as Vec3Proxy internally
    v.x = 1.0
    v.y = 2.0
    v.z = 3.0

```

### Generics
```python
T = TypeVar('T', bound=Any)
@lc.func
def add(a: T, b: T) -> T:
    return a + b

```


### Metaprogramming
luisa_lang provides a metaprogramming feature similar to C++ that allows users to generate code at compile time. 

```python
# Compile time reflection
@lc.func
def get_x_or_zero(x: Any):
    t = lc.comptime(type(x))
    if lc.comptime(hasattr(t, 'x')):
        return x.x
    else:
        return 0.0

# Lambdas/Function objects
F = TypeVar('F', bound=Callable) # TypeVar bounds facilliatate type inference in Mypy etc. but are not strictly necessary
T = TypeVar('T', bound=Any)

@lc.func
def apply_func(f: F, x: T):
    return f(x)

# Generate code at compile time
@lc.func
def call_n_times(f: F):
    with lc.comptime():
        n = input('how many times to call?')
        for i in range(n):
            # lc.embed_code(expr) will generate add expr to the DSL code
            lc.embed_code(apply_func(f, i))
            # or 
            lc.embed_code('apply_func(f, i)')

# Hint a parameter is constexpr
@lc.func(n=lc.comptime) # without this, n will be treated as a runtime variable and result in an error
def pow(x: lc.float, n: int) -> lc.float:
    p = 1.0
    with lc.comptime():
        for _ in range(n):
            lc.embed_code('p *= x')
    return p
```
### Limitation & Caveats
- Lambda and nested function do not support updating nonlocal variables.
- All DSL types have value semantics, which means they are copied when passed around.
- `lc.embed_code` cannot be used to generate a new variable that is referenced in later code. Declare the variable with `Any` type prior to using `lc.embed_code`.
- `lc.struct` can only be used at the top level of a module.

### Standalone Compiler
It is possible to retarget luisa_lang to serve as another DSL. For example, one may want to use it as a customized shader language different from what LuisaCompute provides, or use it to generate customized C++/CUDA source. In this case, one can use the standalone compiler to compile the luisa_lang code into a standalone shader file.

```python
```