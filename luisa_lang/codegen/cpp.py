from luisa_lang import hir
from luisa_lang._utils import unwrap
from luisa_lang.codegen import CodeGen, ScratchBuffer
from typing import Any, Callable, Dict, Union

from luisa_lang.hir.defs import GlobalContext
from luisa_lang.lang import get_dsl_func


class TypeCodeGenCache:
    cache: Dict[hir.Type, str]

    def __init__(self) -> None:
        self.cache = {}

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
                    return f"int{bits}_t"
                else:
                    return f"uint{bits}_t"
            case hir.FloatType(bits=bits):
                return f"float{bits}_t"
            case hir.BoolType():
                return "bool"
            case _:
                raise NotImplementedError(f"unsupported type: {ty}")


class Mangling:
    cache: Dict[hir.Type | hir.Function, str]

    def __init__(self) -> None:
        self.cache = {}

    def mangle(self, obj: Union[hir.Type, hir.Function]) -> str:
        if obj in self.cache:
            return self.cache[obj]
        else:
            res = self.mangle_impl(obj)
            self.cache[obj] = res
            return res

    def mangle_impl(self, obj: Union[hir.Type, hir.Function]) -> str:
        def mangle_name(name: str) -> str:
            comps = name.split(".")
            mangled = "N"
            for i, c in enumerate(comps):
                mangled += f"{len(c)}{c}"
                if i != len(comps) - 1:
                    mangled += "E"
            return mangled

        match obj:
            case hir.IntType(bits=bits, signed=signed):
                if signed:
                    return f"i{bits}"
                else:
                    return f"u{bits}"
            case hir.FloatType(bits=bits):
                return f"f{bits}"
            case hir.BoolType():
                return "b"
            case hir.PointerType(element=element):
                return f"P{self.mangle(element)}"
            case hir.ArrayType(element=element, count=count):
                return f"A{count}{self.mangle(element)}"
            case hir.Function(name=name, params=params, return_type=ret):
                name = mangle_name(name)
                return f"F{name}_{self.mangle(ret)}_{'_'.join(self.mangle(unwrap(p.type)) for p in params)}"
            case _:
                raise NotImplementedError(f"unsupported object: {obj}")


class CppCodeGen(CodeGen):
    type_cache: TypeCodeGenCache
    func_cache: Dict[hir.Function, str]
    mangling: Mangling
    generated_code: ScratchBuffer

    def __init__(self) -> None:
        super().__init__()
        self.type_cache = TypeCodeGenCache()
        self.func_cache = {}
        self.mangling = Mangling()
        self.generated_code = ScratchBuffer()

    def gen_function(self, func: hir.Function | Callable[..., Any]) -> str:
        if callable(func):
            func = get_dsl_func(func)
        if func in self.func_cache:
            return self.func_cache[func]
        func_code_gen = FuncCodeGen(self, func)
        name = func_code_gen.name
        self.func_cache[func] = name
        func_code_gen.gen()
        self.generated_code.merge(func_code_gen.body)
        return name


class FuncCodeGen:
    base: CppCodeGen
    body: ScratchBuffer
    name: str
    signature: str
    func: hir.Function

    def gen_var(self, var: hir.Var) -> str:
        assert var.type
        ty = self.base.type_cache.gen(var.type)
        if var.byval:
            return f"{ty} {var.name}"
        else:
            return f"{ty}& {var.name}"

    def __init__(self, base: CppCodeGen, func: hir.Function) -> None:
        self.base = base
        self.name = base.mangling.mangle(func)
        self.func = func
        params = ",".join(self.gen_var(p) for p in func.params)
        self.signature = f'extern "C" auto {self.name}({params}) -> {base.type_cache.gen(func.return_type)}'
        self.body = ScratchBuffer()

    def gen_ref(self, ref: hir.Ref) -> str:
        match ref:
            case hir.Var() as var:
                return var.name
            case _:
                raise NotImplementedError(f"unsupported reference: {ref}")

    def gen_expr(self, expr: hir.Value) -> str:
        match expr:
            case hir.Load() as load:
                return self.gen_ref(load.ref)
            case hir.Call() as ucall if expr.is_unresolved():
                kind = ucall.kind
                match kind:
                    case hir.CallOpKind.BINARY_OP:
                        return f"{self.gen_expr(ucall.args[0])} {ucall.op} {self.gen_expr(ucall.args[1])}"
                    case hir.CallOpKind.UNARY_OP:
                        return f"{ucall.op}{self.gen_expr(ucall.args[0])}"
                    case hir.CallOpKind.FUNC:
                        # TODO: fix this
                        return f"{ucall.op}({','.join(self.gen_expr(arg) for arg in ucall.args)})"
            case _:
                raise NotImplementedError(f"unsupported expression: {expr}")

    def gen_stmt(self, stmt: hir.Stmt):
        match stmt:
            case hir.Return() as ret:
                if ret.value:
                    self.body.writeln(f"return {self.gen_expr(ret.value)};")
                else:
                    self.body.writeln("return;")
            case hir.Assign() as assign:
                ref = self.gen_ref(assign.ref)
                value = self.gen_expr(assign.value)
                self.body.writeln(f"{ref} = {value};")
            case _:
                raise NotImplementedError(f"unsupported statement: {stmt}")

    def gen_locals(self):
        for local in self.func.locals:
            assert (
                local.type
            ), f"Local variable {local.name} contains unresolved type, please resolve it via TypeInferencer"
            self.body.writeln(
                f"{self.base.type_cache.gen(local.type)} {local.name}{{}};"
            )

    def gen(self) -> None:
        self.body.writeln(f"{self.signature} {{")
        self.body.indent += 1
        self.gen_locals()
        for stmt in self.func.body:
            self.gen_stmt(stmt)
        self.body.indent -= 1
        self.body.writeln("}")
