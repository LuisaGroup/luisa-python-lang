from typing import Any, Callable, Dict, List, Optional, TypeVar
from luisa_lang import hir
from luisa_lang._utils import report_error


class TypeInferencer:
    pass


def _infer_cache(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(inferencer: 'FuncTypeInferencer', node: hir.TypedNode, *args) -> Optional[hir.Type]:
        if id(node) in inferencer._cache:
            return inferencer._cache[id(node)]
        if node.type:
            return node.type
        ty = func(inferencer, node, *args)
        node.type = ty
        inferencer._cache[id(node)] = ty
        return ty
    return wrapper


def is_function_fully_typed(func: hir.Function) -> bool:
    for stmt in func.body:
        if not is_stmt_fully_typed(stmt):
            return False
    return True


def is_stmt_fully_typed(stmt: hir.Stmt) -> bool:
    match stmt:
        case hir.Assign(ref=ref, value=value):
            return is_expr_fully_typed(value)
        case hir.Return(value=value):
            return value is None or is_expr_fully_typed(value)
        case _:
            raise NotImplementedError(f"Unsupported stmt type: {stmt}")


def is_expr_fully_typed(expr: hir.Value) -> bool:
    if not expr.type:
        return False
    match expr:
        case hir.Load(ref=ref):
            return is_ref_fully_typed(ref)
        case hir.Call(op=op) if isinstance(op, str):
            return False
        case hir.Call(op=op) if isinstance(op, hir.Value):
            return is_expr_fully_typed(op) and all(is_expr_fully_typed(arg) for arg in expr.args)
        case hir.Member(base=base, field=field):
            return is_ref_fully_typed(base)
        case hir.Constant():
            return True
        case _:
            raise NotImplementedError(f"Unsupported expr type: {expr}")


def is_ref_fully_typed(ref: hir.Ref) -> bool:
    match ref:
        case hir.ValueRef(value=value):
            return is_expr_fully_typed(value)
        case hir.Var():
            return ref.type is not None
        case hir.Member(base=base, field=field):
            return is_ref_fully_typed(base)
        case _:
            raise NotImplementedError(f"Unsupported ref type: {ref}")


class FuncTypeInferencer:
    func: hir.Function
    _cache: Dict[int, Optional[hir.Type]]

    def __init__(self, func: hir.Function) -> None:
        self.func = func
        self._cache = {}

    def infer(self) -> None:
        for stmt in self.func.body:
            self.infer_stmt(stmt)
        if is_function_fully_typed(self.func):
            self.func.fully_typed = True

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

    def _infer_member(self, member: hir.Member) -> Optional[hir.Type]:
        if member.type:
            return member.type
        base = self.infer_ref(member.base)
        if not base:
            return None
        field = member.field
        return base.member(field)

    @_infer_cache
    def infer_ref(self, ref: hir.Ref) -> Optional[hir.Type]:
        match ref:
            case hir.ValueRef(value=value):
                return self.infer_expr(value)
            case hir.Var():
                return ref.type
            case hir.Member() as member:
                return self._infer_member(member)
            case _:
                raise NotImplementedError(f"Unsupported ref type: {ref}")

    @_infer_cache
    def infer_expr(self, expr: hir.Value) -> Optional[hir.Type]:
        match expr:
            case hir.Load(ref=ref):
                ty = self.infer_ref(ref)
                return ty
            case hir.Call(op=op) if isinstance(op, str):
                ty = self._infer_operator(expr)
                return ty
            case hir.Call(op=op) if isinstance(op, hir.Value):
                op_ty = self.infer_expr(op)
                if not op_ty:
                    return None
                if not isinstance(op_ty, hir.FunctionType):
                    raise hir.TypeInferenceError(
                        f"Expected callable, got {op_ty}")
                args = [self.infer_expr(arg) for arg in expr.args]
                return self._infer_call_helper(op_ty.func_like, args)
            case hir.Member() as member:
                return self._infer_member(member)
            case hir.Constant() as constant:
                if isinstance(constant.value, hir.Function):
                    return hir.FunctionType(constant.value)
                raise NotImplementedError(
                    f"Unsupported constant type: {constant}")
            case _:
                raise NotImplementedError(f"Unsupported expr type: {expr}")

    def _infer_call_helper(
        self, f: hir.FunctionLike, args: List[hir.Type]
    ) -> Optional[hir.Type]:
        if isinstance(f, hir.BuiltinFunction):
            return f.type_rule.infer(args)
        else:
            param_tys = []
            for p in f.params:
                assert p.type, f"Parameter {p.name} has no type"
                param_tys.append(p.type)
            if len(param_tys) != len(args):
                raise hir.TypeInferenceError(
                    f"Expected {len(param_tys)} arguments, got {len(args)}"
                )
            for i, (param_ty, arg) in enumerate(zip(param_tys, args)):
                if param_ty != arg:
                    raise hir.TypeInferenceError(
                        f"Argument {i} expected {param_ty}, got {arg}"
                    )
            return f.return_type

    def _infer_operator(self, expr: hir.Call) -> Optional[hir.Type]:
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
            ty = infer_binop(name, rname)
            if ty:
                expr.resolved = True
            return ty
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
