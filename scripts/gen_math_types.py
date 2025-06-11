from typing import List, Optional
from enum import Enum


class Kind(Enum):
    BOOL = 0
    INT = 1
    FLOAT = 2


def main() -> None:
    with open("luisa_lang/math_types.py", "w") as f:
        FLOAT_BULTINS_1 = [
            "abs",
            "acos",
            "acosh",
            "asin",
            "asinh",
            "atan",
            "atanh",
            "ceil",
            "cos",
            "cosh",
            "exp",
            "floor",
            "log",
            "log10",
            "log2",
            "sin",
            "sinh",
            "sqrt",
            "tan",
            "tanh",
            "trunc",
        ]
        FLOAT_BULTINS_2 = ["atan2", "copysign"]
        exports: List[str] = (
            ["FLOAT_TYPES", "FloatType"]
            + FLOAT_BULTINS_1
            + FLOAT_BULTINS_2
        )

        def print(s: str) -> None:
            if s == "":
                __builtins__.print(file=f)
            lines = s.split("\n")
            for line in lines:
                if line == "":
                    continue
                __builtins__.print(line, file=f)

        print("# fmt: off")
        print("import typing as tp")
        print(
            "from luisa_lang._builtin_decor import func, builtin_type, trace",
        )
        print(
            "from luisa_lang.lang_runtime import __intrinsic__, __intrinsic_checked__, __escape__, assign, type_of, is_jit, JitVar",
        )
        print(
            "from luisa_lang.core_types import Ref",
        )
        print(
            "from luisa_lang.classinfo import register_class",
        )
        print("import luisa_lang.hir as _hir")
        print('IntLiteral = int')
        print('FloatLiteral = float')
        print("_ctx = _hir.GlobalContext.get()")
        print(r"""
def _literal_to_value(literal, dtype):
    if isinstance(literal, JitVar):
        return literal
    return _hir.Constant(literal, dtype)
""")
        def gen_float_builtins():
        #     print("class FloatBuiltin(tp.Generic[_F]):")
        #     for builtin in FLOAT_BULTINS_1:
        #         print("    @trace")
        #         print(f"    def {builtin}(self: _F) -> _F: return __intrinsic__('math.{builtin}', _F, self) # type: ignore")
        #     for builtin in FLOAT_BULTINS_2:
        #         print("    @trace")
        #         print(
        #             f"    def {builtin}(self: _F, _other: _F) -> _F: return __intrinsic__('math.{builtin}', _F, self, other) # type: ignore"
        #         )
            print("")
            for builtin in FLOAT_BULTINS_1:
                print(
                    f"@func\ndef {builtin}(x: _F1) -> _F1: return __intrinsic__('math.{builtin}', _F1, x) # type: ignore"
                )
            for builtin in FLOAT_BULTINS_2:
                print(
                    f"@func\ndef {builtin}(x: _F1, y: _F1) -> _F1: return __intrinsic__('math.{builtin}', _F1, x, y) # type: ignore"
                )
        #     print("register_class(FloatBuiltin)")

        def gen_binop(op: str, ty: str, operand_ty: str, inplace=False):
            print(
                f"""
    @trace
    def {op}(self, _other: {operand_ty}) -> '{ty}': # type: ignore
        return __intrinsic_checked__("binop.{op}.{ty}", [{ty}, __escape__({operand_ty.replace('\'','')})], {ty},  {'self' if not inplace else 'Ref(self)'}, _other)
"""
            )

        def gen_cmpop(op: str, ty: str, operand_ty: str,retrun_ty:str):
            print(
                f"""
    @trace
    def {op}(self, _other: {operand_ty}) -> '{retrun_ty}': # type: ignore
        return __intrinsic_checked__("cmp.{op}.{ty}", [{ty}, __escape__({operand_ty.replace('\'','')})], {retrun_ty},  self, _other) # type: ignore
"""
            )

        def gen_common_binop(ty: str, operand_ty: str, mask_ty:str, kind: Kind):
            def gen(op: str, inplace: bool = True):
                gen_binop(f"__{op}__", ty, operand_ty)
                gen_binop(f"__r{op}__", ty, operand_ty)
                # gen in-place version
                if inplace:
                    gen_binop(f"__i{op}__", ty, operand_ty, inplace=True)

            if kind != Kind.BOOL:
                gen("add")
                gen("sub")
                gen("mul")
                gen("mod")
                gen_cmpop("__lt__", ty, operand_ty, mask_ty)
                gen_cmpop("__le__", ty, operand_ty, mask_ty)
                gen_cmpop("__gt__", ty, operand_ty, mask_ty)
                gen_cmpop("__ge__", ty, operand_ty, mask_ty)
            gen_cmpop("__eq__", ty, operand_ty, mask_ty)
            gen_cmpop("__ne__", ty, operand_ty, mask_ty)
            if kind == Kind.INT:
                gen("floordiv")
            if kind == Kind.FLOAT:
                gen("truediv")
                gen("pow")
                gen("floordiv", inplace=False)
            if kind == Kind.INT:
                gen("lshift")
                gen("rshift")
            if kind != Kind.FLOAT:
                gen("and")
                gen("or")
                gen("xor")

        def gen_unaryop(op: str, ty: str):
            print(
                f"""
    @trace
    def __{op}__(self) -> '{ty}': return __intrinsic__("unary.__{op}__.{ty}",  {ty}, self)
""")

        def gen_scalar_type(ty: str, literal_ty: str, kind: Kind):
            nonlocal exports
            exports.append(ty)
            inherits:List[str] = []
            # if kind == Kind.FLOAT:
            #     inherits.append(f"FloatBuiltin['{ty}']")
            inherits_str = "" if len(inherits) == 0 else f"({', '.join(inherits)})"
            if kind == Kind.FLOAT:
                bits = 32 if ty == "f32" else 64
                hir_ty = f"_hir.FloatType({bits})"
            elif kind == Kind.INT:
                signed = ty[0] == "i"
                hir_ty = f"_hir.IntType({int(ty[1:])}, {signed})"
            else:
                hir_ty = "_hir.BoolType()"
            print(
                f"""@builtin_type({hir_ty})
class {ty}{inherits_str}:
    @trace
    def __init__(self, _value: tp.Union['{ty}', {literal_ty}]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.{ty}",  {ty},  _literal_to_value(_value, type_of({ty}))))
        else:
            pass # TODO
"""
            )
            gen_common_binop(ty, f" tp.Union['{ty}', {literal_ty}]", 'bool', kind)
            if kind == Kind.FLOAT or kind == Kind.INT:
                gen_unaryop("neg", ty)
                gen_unaryop("pos", ty)
            if kind == Kind.INT or kind == Kind.BOOL:
                gen_unaryop("invert", ty)           
            print("")

        def gen_vector_type(ty: str, scalar_ty: str, literal_scalar_ty: str,kind: Kind, mask_ty:str, size: int):
            nonlocal exports
            exports.append(ty)
            comps = "xyzw"[:size]
            fields_def = "".join([f"    {comp}: {scalar_ty}\n" for comp in comps])
            inherits:List[str] = []
            # if kind == Kind.FLOAT:
            #     inherits.append(f"FloatBuiltin['{ty}']")
            inherits_str = "" if len(inherits) == 0 else f"({', '.join(inherits)})"
            print(
                f"""@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[{scalar_ty}].default()), {size}))
class {ty}{inherits_str}:
{fields_def}
""")        
            # literal_scalar_default = '0' if literal_scalar_ty == 'int' else '0.0'
            literal_scalar_default:str
            if literal_scalar_ty == 'IntLiteral':
                literal_scalar_default = 'IntLiteral()'
            elif literal_scalar_ty == 'FloatLiteral':
                literal_scalar_default = 'FloatLiteral()'
            else:
                literal_scalar_default = 'False'
            print('    @trace')
            print('    def __init__(self, '+\
                  ", ".join([f"{comp}: tp.Union[\'{scalar_ty}\', {literal_scalar_ty}] = {literal_scalar_default}" for comp in comps]) + \
                      ') -> None:')
            print('        if is_jit():')
            print('            assign(self, __intrinsic__("init.'+ty+'", '+ty+', '+", ".join([f'_literal_to_value({c}, type_of({ty}))' for c in comps])+'))')
            print('        else:')
            print('            pass # TODO')
            print("")

            gen_common_binop(
                ty, f" tp.Union['{ty}', {scalar_ty}, {literal_scalar_ty}]",mask_ty, kind
            )
            print("")

        def gen_matrix_type(ty:str, vector_ty:str, scalar_ty:str, literal_scalar_ty:str, dim:int):
            nonlocal exports
            exports.append(ty)
            comps = "xyzw"[:dim]
            fields_def = "".join([f"    {comp}: {vector_ty}\n" for comp in comps])
            inherits:List[str] = []
            # if kind == Kind.FLOAT:
            #     inherits.append(f"FloatBuiltin['{ty}']")
            inherits_str = "" if len(inherits) == 0 else f"({', '.join(inherits)})"
            print(
                f"""@builtin_type(_hir.MatrixType({dim}))
class {ty}{inherits_str}:
{fields_def}
    def __init__(self) -> None: self = __intrinsic__("init.{ty}", {ty})
""")

        float_types = ["f32", "f64"]
        for size in [2, 3, 4]:
            float_types.append(f"float{size}")
            float_types.append(f"double{size}")
        float_types_quoted = [f'"{x}"' for x in float_types]

        print(
            f'FLOAT_TYPES: tp.Final[tp.List[str]] = [{", ".join(float_types_quoted)}]'
        )
        print(f'FloatType = tp.Union[{", ".join(float_types_quoted)}]')
        print(f'_F = tp.TypeVar("_F")')
        print(f'_F1 = tp.TypeVar("_F1", {", ".join(float_types_quoted)})')
        gen_float_builtins()
        gen_scalar_type(f"boolean", f"bool", Kind.BOOL)
        gen_scalar_type("f32", "float", Kind.FLOAT)
        gen_scalar_type("f64", "float", Kind.FLOAT)

        for bits in [8, 16, 64]:
            gen_scalar_type(f"i{bits}", f"IntLiteral", Kind.INT)
            gen_scalar_type(f"u{bits}", f"IntLiteral", Kind.INT)
        gen_scalar_type(f"i32", f"IntLiteral", Kind.INT)
        gen_scalar_type(f"u32", f"IntLiteral", Kind.INT)


        for size in [2, 3, 4]:
            gen_vector_type(f"bool{size}", "boolean", "bool",Kind.BOOL, f"bool{size}",size)
            gen_vector_type(f"float{size}", "f32", "FloatLiteral",Kind.FLOAT,f"bool{size}",size)
            gen_vector_type(f"double{size}", "f64", "FloatLiteral",Kind.FLOAT,f"bool{size}", size)
            names = {8: "byte", 16: "short", 32: "int", 64: "long"}
            for bits in [8, 16, 32, 64]:
                name = names[bits]
                gen_vector_type(f"{name}{size}", f"i{bits}", "IntLiteral",Kind.INT,f"bool{size}", size)
                gen_vector_type(f"u{name}{size}", f"u{bits}", "IntLiteral",Kind.INT,f"bool{size}", size)
        exports.append('f32')
        exports.append('i32')
        print("__all__ = " + str(exports))


if __name__ == "__main__":
    main()
