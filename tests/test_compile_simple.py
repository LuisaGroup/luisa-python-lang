
import luisa_lang as lc
import subprocess
from luisa_lang.compile import Compiler

@lc.func
def sqr(x):
    return x * x

@lc.func
def foo(a, b):
    if a < b:
        return sqr(a + b)
    else:
        return a - b
    

compiler = Compiler('cpp')
compiler.compile(foo, example_inputs=(lc.f32(1.0),lc.f32(3.0)), name="foo_example")
output_code = compiler.output()
with open("test.cpp", "w") as f:
    f.write(output_code)

subprocess.run(["clang","-O3", "-std=c++20", "test.cpp", "-S", "-emit-llvm", "-o", "test.ll"])