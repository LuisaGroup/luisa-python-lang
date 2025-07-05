
import luisa_lang as lc
import subprocess
from luisa_lang.compile import Compiler

@lc.struct
class Point:
    x: lc.f32
    y: lc.f32

    @lc.trace
    def __init__(self, x: lc.f32, y: lc.f32):
        self.x = x
        self.y = y

@lc.func
def sqr(x):
    return x * x

@lc.func
def foo(a, b):
    # p = Point(lc.f32(1.0), lc.f32(2.0))
    p = Point(a, b)
    z = sqr(a)
    if a < b:
        return z
    else:
        return a - b
    

compiler = Compiler('cpp')
compiler.compile(foo, example_inputs=(lc.f32(1.0),lc.f32(3)), name="foo_example")
output_code = compiler.output()
with open("test.cpp", "w") as f:
    f.write(output_code)

subprocess.run(["clang","-O3", "-std=c++20", "test.cpp", "-S", "-emit-llvm", "-o", "test.ll"])