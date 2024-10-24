from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast
from luisa_lang import hir
from luisa_lang._utils import report_error
from luisa_lang.hir.defs import is_type_compatible_to
import traceback

class TypeInferencer:
    pass


F = TypeVar('F', bound=Callable[..., Any])


def _infer_cache(func: F) -> F:
    def wrapper(inferencer: 'FuncTypeInferencer', node: hir.TypedNode, *args) -> Optional[hir.Type]:
        if node.type:
            return node.type
        ty = func(inferencer, node, *args)
        node.type = ty
        return ty
    return cast(F, wrapper)


def is_function_fully_typed(func: hir.Function) -> bool:
    if not func.return_type:
        return False
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
        case hir.If(cond=cond, then_body=then_body, else_body=else_body):
            if not is_expr_fully_typed(cond):
                return False
            for stmt in then_body:
                if not is_stmt_fully_typed(stmt):
                    return False
            for stmt in else_body:
                if not is_stmt_fully_typed(stmt):
                    return False
            return True
        case hir.VarDecl(var=var, expected_type=ty):
            return var.type is not None and ty is not None
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
        case hir.Member(base=base):
            if isinstance(base, hir.Ref):
                return is_ref_fully_typed(base)
            return is_expr_fully_typed(base)
        case hir.Index(base=base, index=index):
            if isinstance(base, hir.Ref):
                return is_ref_fully_typed(base) and is_expr_fully_typed(index)
            return is_expr_fully_typed(base) and is_expr_fully_typed(index)
        case _:
            raise NotImplementedError(f"Unsupported ref type: {ref}")


class FuncTypeInferencer:
    func: hir.Function

    def __init__(self, func: hir.Function) -> None:
        self.func = func

    def infer(self) -> None:
        if self.func.fully_typed:
            return
        for stmt in self.func.body:
            self.infer_stmt(stmt)
        if is_function_fully_typed(self.func):
            self.func.fully_typed = True

    def infer_stmt(self, stmt: hir.Stmt) -> None:
        match stmt:
            case hir.Assign(ref=ref, value=value):
                ref_ty = self.infer_ref(ref)
                ty = self.infer_expr(value)
                if ty and not ref_ty:
                    ref.type = ty
                elif ref_ty and ty:
                    if not is_type_compatible_to(ty, ref_ty):
                        raise hir.TypeInferenceError(
                            stmt, f"Type mismatch in assignment: expected {ref_ty}, got {ty}")
            case hir.Return(value=value):
                if value:
                    ty = self.infer_expr(value)
                    if not self.func.return_type:
                        self.func.return_type = ty
                    elif self.func.return_type != ty:
                        report_error(
                            stmt.span,
                            f"Return type mismatch: expected {self.func.return_type}, got {ty}",
                        )
                elif self.func.return_type != hir.UnitType():
                    report_error(
                        stmt.span,
                        f"Return type mismatch: expected {self.func.return_type}, got void",
                    )
            case hir.If(cond=cond, then_body=then_body, else_body=else_body):
                self.infer_expr(cond)
                for stmt in then_body:
                    self.infer_stmt(stmt)
                for stmt in else_body:
                    self.infer_stmt(stmt)
            case hir.VarDecl(var=var, expected_type=ty):
                if not var.type:
                    var.type = ty
                elif var.type != ty:
                    report_error(
                        stmt.span,
                        f"Internal Compiler Error: Type mismatch in variable declaration: expected {ty}, got {var.type}",
                    )
            case _:
                raise NotImplementedError(f"Unsupported stmt type: {stmt}")

    def _infer_member(self, member: hir.Member) -> Optional[hir.Type]:
        if member.type:
            return member.type
        if isinstance(member.base, hir.Ref):
            base = self.infer_ref(member.base)
        else:
            base = self.infer_expr(member.base)
        if not base:
            return None
        field = member.field
        if not (ty := base.member(field)):
            raise hir.TypeInferenceError(
                member,
                f"Type {base} has no member {field}")
        return ty

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
                        expr,
                        f"Expected callable, got {op_ty}")
                if not isinstance(op, hir.Constant):
                    if isinstance(expr.op, hir.Load) and isinstance(expr.op.ref, hir.Member):
                        # map a.b(args...) to a.b.__call__(a, args...)
                        base = expr.op.ref.base
                        if isinstance(base, hir.Ref):
                            expr.args.insert(0, hir.Load(base))
                        else:
                            expr.args.insert(0, base)
                    expr.op = hir.Constant(op_ty.func_like)
                args = []
                for arg in expr.args:
                    arg_ty = self.infer_expr(arg)
                    if not arg_ty:
                        return None
                    args.append(arg_ty)
                return self._infer_call_helper(expr, op_ty.func_like, args)
            case hir.Member() as member:
                return self._infer_member(member)
            case hir.Constant() as constant:
                if isinstance(constant.value, hir.Function) \
                        or isinstance(constant.value, hir.FunctionTemplate)\
                        or isinstance(constant.value, hir.BuiltinFunction):
                    return hir.FunctionType(constant.value)
                if isinstance(constant.value, float):
                    return hir.GenericFloatType()
                if isinstance(constant.value, int):
                    return hir.GenericIntType()
                if isinstance(constant.value, bool):
                    return hir.BoolType()
                raise NotImplementedError(
                    f"Unsupported constant type: {constant.value}")
            case _:
                raise NotImplementedError(f"Unsupported expr type: {expr}")

    def _infer_call_helper(
        self, node: hir.Call, f: hir.FunctionLike | hir.FunctionTemplate, args: List[hir.Type]
    ) -> Optional[hir.Type]:
        if isinstance(f, hir.BuiltinFunction):
            try:
                return f.type_rule.infer(args)
            except hir.TypeInferenceError as e:
                e.node = node
                raise e
        elif isinstance(f, hir.FunctionTemplate):
            if self.func.is_generic:
                raise hir.TypeInferenceError(
                    node,
                    f"TODO: infer generic function {f.name}")
            if f.is_generic:
                template_resolve_args: hir.FunctionTemplateResolvingArgs = []
                template_params = f.params
                if len(template_params) != len(args):
                    raise hir.TypeInferenceError(
                        node,
                        f"Expected {len(template_params)} arguments, got {len(args)}")
                for i, (param, arg) in enumerate(zip(template_params, args)):
                    template_resolve_args.append((param, arg))
                try:
                    resolved_f = f.resolve(template_resolve_args)
                except Exception as e:
                    # traceback.print_exc()
                    raise hir.TypeInferenceError(
                        node,
                        f"Error during instantiating function template {f.name}: {e}") from e
            else:
                resolved_f = f.resolve(None)
            node.op = hir.Constant(resolved_f)
            node.op.type = hir.FunctionType(resolved_f)
            return self._infer_call_helper(node, resolved_f, args)
        else:
            if f.is_generic:
                raise hir.TypeInferenceError(
                    node,
                    f"Cannot infer generic function {f.name}")
            param_tys = []
            for p in f.params:
                assert p.type, f"Parameter {p.name} has no type"
                param_tys.append(p.type)
            if len(param_tys) != len(args):
                raise hir.TypeInferenceError(
                    node,
                    f"Expected {len(param_tys)} arguments, got {len(args)}"
                )
            for i, (param_ty, arg) in enumerate(zip(param_tys, args)):
                if not is_type_compatible_to(arg, param_ty):
                    raise hir.TypeInferenceError(
                        node,
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

            def infer_binop(name: str, rname: str) -> Optional[Tuple[hir.Type, hir.FunctionLike]]:
                try:
                    # TODO: generic operator overloading
                    # check if args[0] has the method {name} defined
                    if (method := left.resolved_method(name, None)) and method:
                        ty = self._infer_call_helper(
                            expr, method, [left, right])
                        if ty:
                            return ty, method
                    # check if args[1] has the method {rname} defined
                    if (method := right.resolved_method(rname, None)) and method:
                        ty = self._infer_call_helper(
                            expr, method, [right, left])
                        if ty:
                            return ty, method
                    raise hir.TypeInferenceError(
                        expr,
                        f"Operator {op} not defined for types {left} and {right}"
                    )
                except hir.TypeInferenceError as e:
                    e.node = expr
                    raise e

            method_names = BINOP_TO_METHOD_NAMES[op]
            name, rname = method_names
            infer_result = infer_binop(name, rname)
            if not infer_result:
                return None
            ty, method = infer_result
            expr.op = hir.Constant(method)
            expr.kind = hir.CallOpKind.FUNC
            if ty:
                expr.resolved = True
            return ty
        elif expr.kind == hir.CallOpKind.UNARY_OP:
            def helper():
                operand_ty = self.infer_expr(expr.args[0])
                if not operand_ty:
                    return None
                method_name = UNARY_OP_TO_METHOD_NAMES[op]
                if (method := operand_ty.resolved_method(method_name, None)) and method:
                    ty = self._infer_call_helper(expr, method, [operand_ty])
                    if ty:
                        expr.op = hir.Constant(method)
                        expr.kind = hir.CallOpKind.FUNC
                        expr.resolved = True
                        return ty
                return None
            return helper()

        raise NotImplementedError(f"Unsupported operator: {op} {expr.kind}")


def run_inference_on_function(func: hir.Function) -> None:
    # print(f"Running type inference on function {func.name}")
    inferencer = FuncTypeInferencer(func)
    inferencer.infer()


UNARY_OP_TO_METHOD_NAMES: Dict[str, str] = {
    "+": "__pos__",
    "-": "__neg__",
    "~": "__invert__",
}
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
