from typing import Dict, List, Optional
from luisa_lang import hir
from luisa_lang._utils import report_error


class TypeInferencer:
    pass


class FuncTypeInferencer:
    func: hir.Function

    def __init__(self, func: hir.Function) -> None:
        self.func = func

    def infer(self) -> None:
        for stmt in self.func.body:
            self.infer_stmt(stmt)

    def infer_stmt(self, stmt: hir.Stmt) -> None:
        match stmt:
            case hir.Assign(ref=ref, value=value):
                ty = self.infer_expr(value)
                if ty:
                    ref.type = ty
            case hir.Return(value=value):
                if value:
                    ty = self.infer_expr(value)
                    if self.func.return_type != ty:
                        report_error(
                            stmt.span,
                            f"Return type mismatch: expected {self.func.return_type}, got {ty}",
                        )
                elif self.func.return_type != hir.UnitType():
                    report_error(
                        stmt.span,
                        f"Return type mismatch: expected {self.func.return_type}, got void",
                    )
            case _:
                raise NotImplementedError(f"Unsupported stmt type: {stmt}")

    def infer_ref(self, ref: hir.Ref) -> Optional[hir.Type]:
        match ref:
            case hir.ValueRef(value=value):
                ty = self.infer_expr(value)
                if ty:
                    ref.type = ty
                return ty
            case hir.Var():
                return ref.type
            case _:
                raise NotImplementedError(f"Unsupported ref type: {ref}")

    def infer_expr(self, expr: hir.Value) -> Optional[hir.Type]:
        match expr:
            case hir.Load(ref=ref):
                ty = self.infer_ref(ref)
                if ty:
                    expr.type = ty
                return ty
            case hir.Call(op=op) if isinstance(op, str):
                ty = self.infer_operator(expr)
                if ty:
                    expr.type = ty
                return ty
            case _:
                raise NotImplementedError(f"Unsupported expr type: {expr}")

    def _infer_call_helper(
        self, f: hir.FunctionLike, args: List[hir.Type]
    ) -> Optional[hir.Type]:
        if isinstance(f, hir.BuiltinFunction):
            return f.type_rule.infer(args)
        else:
            raise NotImplementedError(f"DOTO")

    def infer_operator(self, expr: hir.Call) -> Optional[hir.Type]:
        op = expr.op
        assert isinstance(op, str)
        if expr.kind == hir.CallOpKind.BINARY_OP:
            left = self.infer_expr(expr.args[0])
            if not left:
                return None
            right = self.infer_expr(expr.args[1])
            if not right:
                return None

            def infer_binop(name: str, rname: str) -> Optional[hir.Type]:
                try:
                    # check if args[0] has the method {name} defined
                    if (method := left.methods.get(name, None)) and method:
                        return self._infer_call_helper(method, [right, left])
                    # check if args[1] has the method {rname} defined
                    if (method := right.methods.get(rname, None)) and method:
                        return self._infer_call_helper(method, [left, right])
                    raise hir.TypeInferenceError(
                        f"Operator {op} not defined for types {left} and {right}"
                    )
                except hir.TypeInferenceError as e:
                    raise e

            method_names = BINOP_TO_METHOD_NAMES[op]
            name, rname = method_names
            return infer_binop(name, rname)
        raise NotImplementedError(f"Unsupported operator: {op} {expr.kind}")


BINOP_TO_METHOD_NAMES: Dict[str, List[str]] = {
    "+": ["__add__", "__radd__"],
    "-": ["__sub__", "__rsub__"],
    "*": ["__mul__", "__rmul__"],
    "/": ["__truediv__", "__rtruediv__"],
    "%": ["__mod__", "__rmod__"],
    "==": ["__eq__", "__eq__"],
    "!=": ["__ne__", "__ne__"],
    "<": ["__lt__", "__gt__"],
    "<=": ["__le__", "__ge__"],
    ">": ["__gt__", "__lt__"],
    ">=": ["__ge__", "__le__"],
    "&": ["__and__", "__rand__"],
    "|": ["__or__", "__ror__"],
    "^": ["__xor__", "__rxor__"],
    "<<": ["__lshift__", "__rlshift__"],
    ">>": ["__rshift__", "__rrshift__"],
    "**": ["__pow__", "__rpow__"],
    "//": ["__floordiv__", "__rfloordiv__"],
}
