from functools import cache
from luisa_lang import hir
from luisa_lang.utils import unique_hash, unwrap
from luisa_lang.codegen import CodeGen, ScratchBuffer
from typing import Any, Callable, Dict, Set, Tuple, Union

from luisa_lang.hir.defs import GlobalContext
from luisa_lang.hir import get_dsl_func
from luisa_lang.hir.infer import run_inference_on_function


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
            case _:
                raise NotImplementedError(f"unsupported type: {ty}")


_OPERATORS: Set[str] = set([
    '__add__',
    '__sub__',
    '__mul__',
    '__truediv__',
    '__floordiv__',
    '__mod__',
    '__pow__',
    '__and__',
    '__or__',
    '__xor__',
    '__lshift__',
    '__rshift__',
    '__eq__',
    '__ne__',
    '__lt__',
    '__le__',
    '__gt__',
    '__ge__',
])


@cache
def map_builtin_to_cpp_func(name: str) -> str:
    comps = name.split(".")
    if comps[0] == "luisa_lang" and comps[1] == "math_types":
        if comps[3] in _OPERATORS:
            return f'{comps[3]}<{comps[2]}>'
        return f'{comps[2]}_{comps[3]}'

    else:
        raise NotImplementedError(f"unsupported builtin function: {name}")


def mangle_name(name: str) -> str:
    return name.replace(".", "_")


class Mangling:
    cache: Dict[hir.Type | hir.FunctionLike, str]

    def __init__(self) -> None:
        self.cache = {}

    def mangle(self, obj: Union[hir.Type, hir.FunctionLike]) -> str:
        if obj in self.cache:
            return self.cache[obj]
        else:
            res = self.mangle_impl(obj)
            self.cache[obj] = res
            return res

    def mangle_impl(self, obj: Union[hir.Type, hir.FunctionLike]) -> str:

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
            case hir.VectorType(element=element, count=count):
                return f"V{count}{self.mangle(element)}"
            case hir.Function(name=name, params=params, return_type=ret):
                assert ret
                name = mangle_name(name)
                return f'{name}_' + unique_hash(f"F{name}_{self.mangle(ret)}{''.join(self.mangle(unwrap(p.type)) for p in params)}")
            case hir.BuiltinFunction(name=name):
                name = map_builtin_to_cpp_func(name)
                return f"__builtin_{name}"
            case hir.StructType(name=name):
                return name
            case _:
                raise NotImplementedError(f"unsupported object: {obj}")


class CppCodeGen(CodeGen):
    type_cache: TypeCodeGenCache
    func_cache: Dict[int, Tuple[hir.Function, str]]
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
            dsl_func = get_dsl_func(func)
            assert dsl_func is not None
            assert not dsl_func.is_generic, f"Generic functions should be resolved before codegen: {func}"
            func_tmp = dsl_func.resolve([])
            assert isinstance(func_tmp, hir.Function), f"Expected function, got {func_tmp}"
            func = func_tmp
        if id(func) in self.func_cache:
            return self.func_cache[id(func)][1]
        run_inference_on_function(func)
        func_code_gen = FuncCodeGen(self, func)
        name = func_code_gen.name
        self.func_cache[id(func)] = (func, name)
        func_code_gen.gen()
        self.generated_code.merge(func_code_gen.body)
        return name

    def finalize_code(self) -> str:
        return self.type_cache.impl.body + self.generated_code.body


class FuncCodeGen:
    base: CppCodeGen
    body: ScratchBuffer
    name: str
    signature: str
    func: hir.Function
    params: Set[str]

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
        assert func.return_type
        self.signature = f'extern "C" auto {self.name}({params}) -> {base.type_cache.gen(func.return_type)}'
        self.body = ScratchBuffer()
        self.params = set(p.name for p in func.params)

    def gen_ref(self, ref: hir.Ref) -> str:
        match ref:
            case hir.Var() as var:
                return var.name
            case hir.Member() as member:
                if isinstance(member.base, hir.Ref):
                    base = self.gen_ref(member.base)
                else:
                    base = self.gen_expr(member.base)
                return f"{base}.{member.field}"
            case hir.ValueRef() as value_ref:
                return self.gen_expr(value_ref.value)
            case _:
                raise NotImplementedError(f"unsupported reference: {ref}")

    def gen_expr(self, expr: hir.Value) -> str:
        match expr:
            case hir.Load() as load:
                return self.gen_ref(load.ref)
            case hir.Call() as call:
                assert call.resolved, f"unresolved call: {call}"
                kind = call.kind
                assert kind == hir.CallOpKind.FUNC and isinstance(
                    call.op, hir.Value)
                op = self.gen_expr(call.op)
                return f"{op}({','.join(self.gen_expr(arg) for arg in call.args)})"
            case hir.Constant() as constant:
                value = constant.value
                if isinstance(value, int):
                    return str(value)
                elif isinstance(value, float):
                    return str(value)
                elif isinstance(value, bool):
                    return "true" if value else "false"
                elif isinstance(value, str):
                    return f'"{value}"'
                elif isinstance(value, hir.Function):
                    return self.base.gen_function(value)
                elif isinstance(value, hir.BuiltinFunction):
                    return self.base.mangling.mangle(value)
                else:
                    raise NotImplementedError(
                        f"unsupported constant: {constant}")
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
            case hir.If() as if_stmt:
                cond = self.gen_expr(if_stmt.cond)
                self.body.writeln(f"if ({cond}) {{")
                self.body.indent += 1
                for stmt in if_stmt.then_body:
                    self.gen_stmt(stmt)
                self.body.indent -= 1
                self.body.writeln("}")
                if if_stmt.else_body:
                    self.body.writeln("else {")
                    self.body.indent += 1
                    for stmt in if_stmt.else_body:
                        self.gen_stmt(stmt)
                    self.body.indent -= 1
                    self.body.writeln("}")
            case hir.VarDecl() as var_decl:
                pass
            case _:
                raise NotImplementedError(f"unsupported statement: {stmt}")

    def gen_locals(self):
        for local in self.func.locals:
            if local.name in self.params:
                continue
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
