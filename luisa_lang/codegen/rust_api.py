from typing import List, NamedTuple, Tuple, Dict, Any, Optional, Union
from luisa_lang.codegen import ScratchBuffer
from luisa_lang.codegen.cpp import mangle_name, Mangling
from luisa_lang import hir
from luisa_lang.utils import unique_hash
class TypeCodeGenCache:
    cache: Dict[hir.Type, str]
    impl: ScratchBuffer

    def __init__(self) -> None:
        self.cache = {}
        self.impl = ScratchBuffer(0)

    def gen(self, ty: hir.Type) -> str:
        if ty in self.cache:
            return self.cache[ty]
        else:
            res = self.gen_impl(ty)
            self.cache[ty] = res
            return res

    def gen_impl(self, ty: hir.Type) -> str:
        match ty:
            case hir.IntType(bits=bits, signed=signed):
                if signed:
                    return f"i{bits}"
                else:
                    return f"u{bits}"
            case hir.FloatType(bits=bits):
                return f"f{bits}"
            case hir.BoolType():
                return "bool"
            case hir.VectorType(element=element, count=count):
                return f"vec<{self.gen(element)}, {count}>"
            case hir.StructType(name=name, fields=fields):
                self.impl.writeln(f'struct {name} {{')
                for field in fields:
                    self.impl.writeln(f'    {self.gen(field[1])} {field[0]};')
                self.impl.writeln('};')
                return name
            case hir.UnitType():
                return 'void'
            case hir.TupleType():
                def do():
                    elements = [self.gen(e) for e in ty.elements]
                    name = f'Tuple_{unique_hash("".join(elements))}'
                    self.impl.writeln(f'struct {name} {{')
                    for i, element in enumerate(elements):
                        self.impl.writeln(f'    {element} _{i};')
                    self.impl.writeln('};')
                    return name
                return do()
            case hir.BoundType():
                assert ty.instantiated
                return self.gen(ty.instantiated)
            case hir.FunctionType():
                return ''
            case hir.TypeConstructorType():
                return ''
            case _:
                raise NotImplementedError(f"unsupported type: {ty}")

class RustAPIGenerator:
    """
    Generates Rust API code for a given DSL module
    """

    def __init__(self):
        pass