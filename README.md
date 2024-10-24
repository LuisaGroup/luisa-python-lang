# luisa-python-lang (WIP)
A new Python DSL frontend for LuisaCompute. Will be integrated into LuisaCompute python package once it's ready.


## Content
- [Introduction](#introduction)
- [Basics](#basic-syntax)
    - [Types](#types)
    - [Functions](#functions)
    - [User-defined Structs](#user-defined-structs)
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
```python
```


### Functions
Functions are defined using the `@lc.func` decorator. The function body can contain any valid LuisaCompute code. You can also include normal Python code that will be executed at DSL comile time using `lc.constexpr()`. (See [Metaprogramming](#metaprogramming) for more details)

```python
@lc.func
def add(a: lc.float, b: lc.float) -> lc.float:
    with lc.constexpr():
        print('compiliing add function')
    return a + b

```

LuisaCompute uses value semantics, which means that all types are passed by value. You can use `inout` to indicate that a variable can be modified in place.
```python
@luisa.func(a=inout, b=inout)
def swap(a: int, b: int):
    a, b = b, a
```

### User-defined Structs
```python
@lc.struct
class Sphere:
    center: lc.float3
    radius: lc.float
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
    t = lc.constexpr(type(x))
    if lc.constexpr(hasattr(t, 'x')):
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
    with lc.constexpr():
        n = input('how many times to call?')
        for i in range(n):
            # lc.embed_code(expr) will generate add expr to the DSL code
            lc.embed_code(apply_func(f, i))
            # or 
            lc.embed_code('apply_func(f, i)')

# Hint a parameter is constexpr
@lc.func(n=lc.constexpr) # without this, n will be treated as a runtime variable and result in an error
def pow(x: lc.float, n: int) -> lc.float:
    p = 1.0
    with lc.constexpr():
        for _ in range(n):
            lc.embed_code('p *= x')
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