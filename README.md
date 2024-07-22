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
luisa_lang provides a metaprogramming feature similar to C++ that allows users to generate code at compile time. This is useful when you want to generate code based on some input parameters, or when you want to generate code that is repetitive.

```python

```

### Standalone Compiler
It is possible to retarget luisa_lang to serve as another DSL. For example, one may want to use it as a customized shader language different from what LuisaCompute provides, or use it to generate customized C++/CUDA source. In this case, one can use the standalone compiler to compile the luisa_lang code into a standalone shader file.

```python
```