from functools import cache
from luisa_lang import hir
from luisa_lang.utils import unique_hash, unwrap
from luisa_lang.codegen import CodeGen, ScratchBuffer
from typing import Any, Callable, Dict, Optional, Set, Tuple, Union


@cache
def _get_cpp_lib() -> str:
    from luisa_lang.codegen.cpp_lib import CPP_LIB_COMPRESSED
    import bz2
    import base64
    return bz2.decompress(base64.b64decode(CPP_LIB_COMPRESSED)).decode('utf-8')


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
                int_names = {
                    '8': 'byte',
                    '16': 'short',
                    '32': 'int',
                    '64': 'long',
                }
                if signed:
                    return f"lc_{int_names[str(bits)]}"
                else:
                    return f"lc_u{int_names[str(bits)]}"
            case hir.FloatType(bits=bits):
                match bits:
                    case 16:
                        return 'lc_half'
                    case 32:
                        return 'lc_float'
                    case 64:
                        return 'lc_double'
                    case _:
                        raise RuntimeError("invalid float type")
            case hir.BoolType():
                return "lc_bool"
            case hir.PointerType(element=element):
                return f"lc_ptr<{self.gen(element)}>"
            case hir.VectorType(element=element, count=count):
                return f"{self.gen(element)}{count}>"
            case hir.ArrayType(element=element, count=count):
                return f"lc_array<{self.gen(element)}, {count}>"
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
            case hir.OpaqueType():
                def do():
                    match ty.name:
                        case 'Buffer':
                            elem_ty = self.gen(ty.extra_args[0])
                            return f'__builtin__Buffer<{elem_ty}>'
                        case _:
                            raise NotImplementedError(
                                f"unsupported opaque type: {ty.name}")
                return do()
            case hir.RefType():
                return f"{self.gen(ty.element)} &"
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

        match obj:
            case hir.UnitType():
                return 'u'
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
                # params = list(filter(lambda p: not isinstance(
                #     p.type, (hir.FunctionType)), params))
                return f'{name}_' + unique_hash(f"F{name}_{self.mangle(ret)}{''.join(self.mangle(unwrap(p.type)) for p in params)}")
            case hir.StructType(name=name):
                return name
            case hir.TupleType():
                elements = [self.mangle(e) for e in obj.elements]
                return f"T{unique_hash(''.join(elements))}"
            case hir.OpaqueType():
                return obj.name
            case hir.RefType():
                return f'R{self.mangle(obj.element)}'
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

    def gen_function(self, func: hir.Function) -> str:
        if id(func) in self.func_cache:
            return self.func_cache[id(func)][1]
        func_code_gen = FuncCodeGen(self, func)
        name = func_code_gen.name
        self.func_cache[id(func)] = (func, name)
        func_code_gen.gen()
        self.generated_code.merge(func_code_gen.body)
        return name

    def finalize_code(self) -> str:
        return _get_cpp_lib() + self.type_cache.impl.body + self.generated_code.body


class FuncCodeGen:
    base: CppCodeGen
    body: ScratchBuffer
    name: str
    signature: str
    func: hir.Function
    params: Set[str]
    node_map: Dict[hir.Node, str]
    vid_cnt: int

    def gen_var(self, var: hir.Var) -> str:
        assert var.type
        ty = self.base.type_cache.gen(var.type)
        if var.semantic == hir.ParameterSemantic.BYVAL:
            return f"{ty} {var.name}"
        else:
            return f"{ty} & {var.name}"

    def __init__(self, base: CppCodeGen, func: hir.Function) -> None:
        self.base = base
        self.name = base.mangling.mangle(func)
        self.func = func
        params = ",".join(self.gen_var(
            p) for p in func.params)
        assert func.return_type

        self.signature = f'auto {
            self.name}({params}) -> {base.type_cache.gen(func.return_type)}'
        # if func.export:
        #     self.signature = f'extern "C" {self.signature}'
        # else:
        #     self.signature = f"inline {self.signature}"
        # if func.inline_hint == 'always':
        #     self.signature = f"__lc_always_inline__ {self.signature}"
        # elif func.inline_hint == 'never':
        #     self.signature = f"__lc_never_inline {self.signature}"
        self.body = ScratchBuffer()
        self.params = set(p.name for p in func.params)
        self.node_map = {}
        self.vid_cnt = 0

    def new_vid(self) -> int:
        self.vid_cnt += 1
        return self.vid_cnt

    def gen_ref(self, ref: hir.Value) -> str:
        if ref in self.node_map:
            return self.node_map[ref]
        match ref:
            case hir.Var() as var:
                return var.name
            case hir.Member() as member:
                base = self.gen_ref(member.base)
                return f"{base}.{member.field}"
            case hir.Index() as index:
                base = self.gen_ref(index.base)
                idx = self.gen_expr(index.index)
                return f"{base}[{idx}]"
            case hir.Intrinsic() as intrin:
                def do():
                    intrin_name = intrin.name
                    gened_args = [self.gen_value_or_ref(
                        arg) for arg in intrin.args]
                    match intrin_name:
                        case 'buffer.ref' | 'array.ref':
                            return f"{gened_args[0]}[{gened_args[1]}]"
                        case 'buffer.size' | 'array.size':
                            return f"{gened_args[0]}.size"
                        case _:
                            raise RuntimeError(
                                f"unsupported intrinsic reference: {intrin_name}")
                return do()
            case hir.VarRef() as var_ref:
                return var_ref.var.name
            case _:
                raise NotImplementedError(f"unsupported reference: {ref}")

    def gen_func(self, f: hir.Function) -> str:
        if isinstance(f, hir.Function):
            return self.base.gen_function(f)
        else:
            raise NotImplementedError(f"unsupported constant")

    def gen_value_or_ref(self, value: hir.Value) -> str:
        # match value:
        #     case hir.Value() as value:
        #         return self.gen_node_checked(value)
        #     case hir.Ref() as ref:
        #         return self.gen_ref(ref)
        #     case _:
        #         raise NotImplementedError(
        #             f"unsupported value or reference: {value}")
        if value.is_ref():
            return self.gen_ref(value)
        else:
            return self.gen_expr(value)

    def gen_node_checked(self, node: hir.Node) -> str:
        if isinstance(node, hir.Constant):
            return self.gen_expr(node)

        return self.node_map[node]

    def gen_expr(self, expr: hir.Value) -> str:
        # if expr.type and isinstance(expr.type, hir.FunctionType):
        #     return ''
        if isinstance(expr, hir.Constant):
            value = expr.value
            if isinstance(value, int):
                return f"{value}"
            elif isinstance(value, float):
                return f"{value}f"
            elif isinstance(value, bool):
                return "true" if value else "false"
            elif isinstance(value, str):
                return f"\"{value}\""
            elif isinstance(value, hir.Function):
                return self.gen_func(value)
            else:
                raise NotImplementedError(
                    f"unsupported constant: {expr}")
        if expr in self.node_map:
            return self.node_map[expr]
        vid = self.new_vid()

        def impl() -> None:
            match expr:
                case hir.VarValue() as var_value:
                    self.body.writeln(
                        f"auto&& v{vid} = {var_value.var.name};")
                case hir.Load() as load:
                    self.body.writeln(
                        f"const auto &v{vid} = {self.gen_ref(load.ref)}; // load")
                case hir.Index() as index:
                    base = self.gen_value_or_ref(index.base)
                    idx = self.gen_expr(index.index)
                    self.body.writeln(f"auto&& v{vid} = {base}[{idx}];")
                case hir.Member() as member:
                    base = self.gen_value_or_ref(member.base)
                    self.body.writeln(
                        f"auto&& v{vid} = {base}.{member.field};")
                case hir.Call() as call:
                    op = self.gen_func(call.op)
                    args_s = ','.join(self.gen_value_or_ref(
                        arg) for arg in call.args)
                    if call.type != hir.UnitType():
                        self.body.writeln(
                            f"auto v{vid} = {op}({args_s});")
                    else:
                        self.body.writeln(f"{op}({args_s});")
                case hir.AggregateInit():
                    assert expr.type
                    ty = self.base.type_cache.gen(expr.type)
                    self.body.writeln(
                        f"{ty} v{vid}{{ {','.join(self.gen_expr(e) for e in expr.args)} }};")
                case hir.Intrinsic() as intrin:                    
                    def do():
                        assert intrin.type
                        intrin_ty_s = self.base.type_cache.gen(intrin.type)
                        intrin_name = intrin.name
                        comps = intrin_name.split('.')
                        gened_args = [self.gen_value_or_ref(
                            arg) for arg in intrin.args]
                        if comps[0] == 'init':
                            assert expr.type
                            ty = self.base.type_cache.gen(expr.type)
                            self.body.writeln(
                                f"{ty} v{vid}{{ {','.join(gened_args)} }};")
                        elif comps[0] == 'cast':
                            self.body.writeln(
                                f"auto v{vid} = static_cast<{intrin_ty_s}>({gened_args[0]});")
                        elif comps[0] == 'bitcast':
                            self.body.writeln(
                                f"auto v{vid} = lc_bit_cast<{intrin_ty_s}>({gened_args[0]});")
                        elif comps[0] == 'cmp':
                            cmp_dict = {
                                '__eq__': '==',
                                '__ne__': '!=',
                                '__lt__': '<',
                                '__le__': '<=',
                                '__gt__': '>',
                                '__ge__': '>=',
                            }
                            if comps[1] in cmp_dict:
                                cmp = cmp_dict[comps[1]]
                                self.body.writeln(
                                    f"auto v{vid} = {gened_args[0]} {cmp} {gened_args[1]};")
                            else:
                                raise NotImplementedError(
                                    f"unsupported cmp intrinsic: {intrin_name}")
                        elif comps[0] == 'unary':
                            unary_dict = {
                                '__neg__': '-',
                                '__pos__': '+',
                                '__invert__': '~',
                            }
                            if comps[1] in unary_dict:
                                unary = unary_dict[comps[1]]
                                self.body.writeln(
                                    f"auto v{vid} = {unary}{gened_args[0]};")
                            else:
                                raise NotImplementedError(
                                    f"unsupported unary intrinsic: {intrin_name}")
                        elif comps[0] == 'binop':
                            binop_dict = {
                                '__add__': '+',
                                '__sub__': '-',
                                '__mul__': '*',
                                '__truediv__': '/',
                                '__floordiv__': '/',  # TODO: fix floordiv
                                '__mod__': '%',
                                '__pow__': '**',
                                '__and__': '&',
                                '__or__': '|',
                                '__xor__': '^',
                                '__lshift__': '<<',
                                '__rshift__': '>>',
                                '__eq__': '==',
                                '__ne__': '!=',
                                '__lt__': '<',
                                '__le__': '<=',
                                '__gt__': '>',
                                '__ge__': '>=',
                            }
                            ibinop_dict = {
                                '__iadd__': '+=',
                                '__isub__': '-=',
                                '__imul__': '*=',
                                '__itruediv__': '/=',
                                '__ifloordiv__': '/=',  # TODO: fix floordiv
                                '__imod__': '%=',
                                '__ipow__': '**=',
                                '__iand__': '&=',
                                '__ior__': '|=',
                                '__ixor__': '^=',
                                '__ilshift__': '<<=',
                                '__irshift__': '>>=',
                            }
                            if comps[1] in binop_dict:
                                binop = binop_dict[comps[1]]
                                self.body.writeln(
                                    f"auto v{vid} = {gened_args[0]} {binop} {gened_args[1]};")
                            elif comps[1] in ibinop_dict:
                                binop = ibinop_dict[comps[1]]
                                self.body.writeln(
                                    f"{gened_args[0]} {binop} {gened_args[1]};  auto& v{vid} = {gened_args[0]};")
                            else:
                                raise NotImplementedError(
                                    f"unsupported binop intrinsic: {intrin_name}")
                        elif comps[0] == 'math':
                            args_s = ','.join(gened_args)
                            self.body.writeln(
                                f"auto v{vid} = lc_{comps[1]}({args_s});")
                        else:
                            intrin_name = intrin.name.replace('.', '_')
                            args_s = ','.join(gened_args)
                            self.body.writeln(
                                f"auto v{vid} = __intrin__{intrin_name}({args_s});")

                    do()
                case _:
                    raise NotImplementedError(
                        f"unsupported expression: {expr}")

        impl()
        self.node_map[expr] = f'v{vid}'
        return f'v{vid}'

    def gen_node(self, node: hir.Node) -> Optional[hir.BasicBlock]:
        match node:
            case hir.Return() as ret:
                if ret.value:
                    self.body.writeln(
                        f"return {self.gen_value_or_ref(ret.value)};")
                else:
                    self.body.writeln("return;")
            case hir.Assign() as assign:
                ref = self.gen_ref(assign.ref)
                value = self.gen_node_checked(assign.value)
                self.body.writeln(f"{ref} = {value};")
            case hir.If() as if_stmt:
                cond = self.gen_node_checked(if_stmt.cond)
                self.body.writeln(f"if ({cond}) {{")
                self.body.indent += 1
                self.gen_bb(if_stmt.then_body)
                self.body.indent -= 1
                self.body.writeln("}")
                if if_stmt.else_body:
                    self.body.writeln("else {")
                    self.body.indent += 1
                    self.gen_bb(if_stmt.else_body)
                    self.body.indent -= 1
                    self.body.writeln("}")
                return if_stmt.merge
            case hir.Break():
                self.body.writeln("__loop_break = true; break;")
            case hir.Continue():
                self.body.writeln("break;")
            case hir.Loop() as loop:
                """
                while(true) {
                    bool loop_break = false;
                    prepare();
                    if (!cond()) break;
                    do {
                        // break => { loop_break = true; break; }
                        // continue => { break; }
                    } while(false);
                    if (loop_break) break;
                    update();
                }

                """
                self.body.writeln("while(true) {")
                self.body.indent += 1
                self.body.writeln("bool __loop_break = false;")
                self.gen_bb(loop.prepare)
                if loop.cond:
                    cond = self.gen_node_checked(loop.cond)
                    self.body.writeln(f"if (!{cond}) break;")
                self.body.writeln("do {")
                self.body.indent += 1
                self.gen_bb(loop.body)
                self.body.indent -= 1
                self.body.writeln("} while(false);")
                self.body.writeln("if (__loop_break) break;")
                if loop.update:
                    self.gen_bb(loop.update)
                self.body.indent -= 1
                self.body.writeln("}")
                return loop.merge
            case hir.Alloca() as alloca:
                vid = self.new_vid()
                assert alloca.type
                ty = self.base.type_cache.gen(alloca.type.remove_ref())
                self.body.writeln(f"{ty} v{vid}{{}}; // alloca")
                self.node_map[alloca] = f"v{vid}"
            case hir.Print() as print_stmt:
                raise NotImplementedError("print statement")
            case hir.Assert() as assert_stmt:
                raise NotImplementedError("assert statement")
            case hir.AggregateInit() | hir.Intrinsic() | hir.Call() | hir.Constant() | hir.Load() | hir.Index() | hir.Member() | hir.VarValue():
                if isinstance(node, hir.TypedNode) and node.is_ref():
                    pass
                else:
                    self.gen_expr(node)
            case hir.VarRef():
                pass
            case _:
                raise NotImplementedError(f"unsupported node: {node}")
        return None

    def gen_bb(self, bb: hir.BasicBlock):

        while True:
            loop_again = False
            old_bb = bb
            self.body.writeln(f"// BasicBlock Begin {bb.span}")
            for node in bb.nodes():
                if (next := self.gen_node(node)) and next is not None:
                    assert node.next is None
                    loop_again = True
                    bb = next
                    break
            self.body.writeln(f"// BasicBlock End {old_bb.span}")
            if not loop_again:
                break

    def gen_locals(self):
        for local in self.func.locals:
            if local.name in self.params:
                continue
            # if isinstance(local.type, (hir.FunctionType, hir.TypeConstructorType)):
            #     continue
            assert (
                local.type
            ), f"Local variable `{local.name}` contains unresolved type"
            self.body.writeln(
                f"{self.base.type_cache.gen(local.type)} {local.name}{{}};"
            )

    def gen(self) -> None:
        self.body.writeln(f"{self.signature} {{")
        self.body.indent += 1
        self.gen_locals()
        if self.func.body:
            self.gen_bb(self.func.body)
        self.body.indent -= 1
        self.body.writeln("}")
