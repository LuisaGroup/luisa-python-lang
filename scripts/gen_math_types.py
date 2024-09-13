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
            "log2" "sin",
            "sinh",
            "sqrt",
            "tan",
            "tanh",
            "trunc",
        ]
        FLOAT_BULTINS_2 = ["atan2", "copysign"]
        exports: List[str] = (
            ["FLOAT_TYPES", "FloatType", "FloatBuiltin"]
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
            "from luisa_lang._builtin_decor import _builtin, _builtin_type, _intrinsic_impl",
        )
        print("import luisa_lang.hir as _hir")
        print("_ctx = _hir.GlobalContext.get()")
        print("_ctx.types[bool] = _hir.BoolType()")

        def gen_float_builtins():
            print("class FloatBuiltin(tp.Generic[_F]):")
            for builtin in FLOAT_BULTINS_1:
                print(f"    def {builtin}(self: _F) -> _F: return _intrinsic_impl()")
            for builtin in FLOAT_BULTINS_2:
                print(
                    f"    def {builtin}(self: _F, _other: _F) -> _F: return _intrinsic_impl()"
                )
            print("")
            for builtin in FLOAT_BULTINS_1:
                print(
                    f"@_builtin\ndef {builtin}(x: FloatType) -> FloatType: return _intrinsic_impl()"
                )
            for builtin in FLOAT_BULTINS_2:
                print(
                    f"@_builtin\ndef {builtin}(x: FloatType, y: FloatType) -> FloatType: return _intrinsic_impl()"
                )

        def gen_binop(op: str, ty: str, operand_ty: str):
            print(
                f"""
    def {op}(self, _other: {operand_ty}) -> '{ty}': return _intrinsic_impl()
"""
            )

        def gen_common_binop(ty: str, operand_ty: str, kind: Kind):
            def gen(op: str, inplace: bool = True):
                gen_binop(f"__{op}__", ty, operand_ty)
                gen_binop(f"__r{op}__", ty, operand_ty)
                # gen in-place version
                if inplace:
                    gen_binop(f"__i{op}__", ty, operand_ty)

            if kind != Kind.BOOL:
                gen("add")
                gen("sub")
                gen("mul")
                gen("mod")
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

        def gen_scalar_type(ty: str, literal_ty: str, kind: Kind):
            nonlocal exports
            exports.append(ty)
            inherits = []
            if kind == Kind.FLOAT:
                inherits.append(f"FloatBuiltin['{ty}']")
            inherits_str = "" if len(inherits) == 0 else f"({', '.join(inherits)})"
            if kind == Kind.FLOAT:
                bits = 32 if ty == "f32" else 64
                hir_ty = f"_hir.FloatType({bits})"
            else:
                signed = ty[0] == "i"
                hir_ty = f"_hir.IntType({int(ty[1:])}, {signed})"
            print(
                f"""@_builtin_type({hir_ty})
class {ty}{inherits_str}:
    def __init__(self, _value: tp.Union['{ty}', {literal_ty}]) -> None: return _intrinsic_impl()
"""
            )
            gen_common_binop(ty, f" tp.Union['{ty}', {literal_ty}]", kind)           
            print("")

        def gen_vector_type(ty: str, scalar_ty: str, literal_scalar_ty: str, size: int):
            nonlocal exports
            exports.append(ty)
            comps = "xyzw"[:size]
            fields_def = "".join([f"    {comp}: {scalar_ty}\n" for comp in comps])
            print(
                f"""@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[{scalar_ty}]), {size}))
class {ty}:
{fields_def}
"""
            )
            gen_common_binop(
                ty, f" tp.Union['{ty}', {scalar_ty}, {literal_scalar_ty}]", Kind.FLOAT
            )
            print("")

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
        gen_float_builtins()
        gen_scalar_type("f32", "float", Kind.FLOAT)
        gen_scalar_type("f64", "float", Kind.FLOAT)

        for bits in [8, 16, 32, 64]:
            gen_scalar_type(f"i{bits}", f"int", Kind.INT)
            gen_scalar_type(f"u{bits}", f"int", Kind.INT)

        for size in [2, 3, 4]:
            gen_vector_type(f"bool{size}", "bool", "bool", size)
            gen_vector_type(f"float{size}", "f32", "float", size)
            gen_vector_type(f"double{size}", "f64", "float", size)
            names = {8: "byte", 16: "short", 32: "int", 64: "long"}
            for bits in [8, 16, 32, 64]:
                name = names[bits]
                gen_vector_type(f"{name}{size}", f"i{bits}", "int", size)
                gen_vector_type(f"u{name}{size}", f"u{bits}", "int", size)
        print("__all__ = " + str(exports))


if __name__ == "__main__":
    main()
