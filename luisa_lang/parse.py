import ast
import os
from types import FunctionType, ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload
import typing
import luisa_lang
from luisa_lang.utils import get_typevar_constrains_and_bounds, report_error
import luisa_lang.hir as hir
import sys
from luisa_lang.utils import retrieve_ast_and_filename
from luisa_lang.hir import (
    Type,
    BoundType,
    ParametricType,
    Function,
    Var,
    get_dsl_func
)
from typing import NoReturn, cast, Set, reveal_type
from enum import Enum
import inspect
from luisa_lang.hir import get_dsl_type
import luisa_lang.classinfo as classinfo


class ComptimeValue:
    value: Any
    update_func: Optional[Callable[[Any], None]]

    def __init__(self, value: Any, update_func: Callable[[Any], None] | None) -> None:
        self.value = value
        self.update_func = update_func

    def update(self, value: Any) -> None:
        if self.update_func is not None:
            self.update_func(value)
        else:
            raise RuntimeError("unable to update comptime value")


def _any_typevar_name(i: int) -> str:
    return f"Any#{i}"


def is_valid_comptime_value_in_dsl_code(value: Any) -> bool:
    if isinstance(value, (int, float, bool)):
        return True
    if isinstance(value, ModuleType):
        return True
    if get_dsl_type(type(value)) is not None:
        return True
    return False


class FuncParser:
    name: str
    func: object
    globalns: Dict[str, Any]
    self_type: Optional[Type]
    vars: Dict[str, hir.Var | ComptimeValue]
    func_def: ast.FunctionDef
    parsed_func: hir.Function
    type_var_ns: Dict[typing.TypeVar, hir.Type]
    bb_stack: List[hir.BasicBlock]

    def __init__(self, name: str,
                 func: object,
                 signature: classinfo.MethodType,
                 globalns: Dict[str, Any],
                 type_var_ns: Dict[typing.TypeVar, hir.Type],
                 any_param_types: List[hir.Type]) -> None:
        self.name = name
        self.func = func
        self.signature = signature
        self.globalns = globalns
        obj_ast, _obj_file = retrieve_ast_and_filename(func)
        print(ast.dump(obj_ast))
        assert isinstance(obj_ast, ast.Module), f"{obj_ast} is not a module"
        if not isinstance(obj_ast.body[0], ast.FunctionDef):
            raise RuntimeError("Function definition expected.")
        self.func_def = obj_ast.body[0]
        self.vars = {}
        self.parsed_func = hir.Function(name, [], None)
        self.type_var_ns = type_var_ns
        self.bb_stack = []

        params: List[Var] = []
        any_param_cnt = 0
        for arg in self.signature.args:
            param_type = self.parse_type(arg[1])
            if param_type is not None:
                params.append(Var(arg[0], param_type, span=None, byval=True))
            else:
                params.append(
                    Var(arg[0], any_param_types[any_param_cnt], span=None, byval=True))
                any_param_cnt += 1
        self.parsed_func.params = params
        for p in self.parsed_func.params:
            self.vars[p.name] = p
        return_type = self.parse_type(signature.return_type)
        if return_type is not None:
            self.parsed_func.return_type = return_type

    def cur_bb(self) -> hir.BasicBlock:
        return self.bb_stack[-1]

    def parse_type(self, ty: classinfo.VarType) -> Optional[hir.Type]:
        match ty:
            case classinfo.GenericInstance():
                raise NotImplementedError()
            case classinfo.TypeVar():
                return self.type_var_ns[ty]
            case classinfo.UnionType():
                raise RuntimeError("UnionType is not supported")
            case classinfo.SelfType():
                assert self.self_type is not None
                return self.self_type
            case classinfo.AnyType():
                return None
            case type():
                dsl_type = get_dsl_type(ty)
                assert dsl_type is not None
                return dsl_type

    def convert_constexpr(self, value: ComptimeValue, span: Optional[hir.Span] = None) -> Optional[hir.Value]:
        value = value.value
        if isinstance(value, int):
            return hir.Constant(value, type=hir.GenericIntType())
        elif isinstance(value, float):
            return hir.Constant(value, type=hir.GenericFloatType())
        elif isinstance(value, bool):
            return hir.Constant(value, type=hir.BoolType())
        elif isinstance(value, FunctionType):
            dsl_func = get_dsl_func(value)
            if dsl_func is None:
                report_error(span, f"expected DSL function but got {value}")
            if dsl_func.is_generic:
                return hir.Constant(dsl_func, type=None, span=span)
            else:
                resolved_f = dsl_func.resolve(None)
                assert not isinstance(
                    resolved_f, hir.TemplateMatchingError)
                return hir.Constant(resolved_f, type=hir.FunctionType(resolved_f), span=span)
        elif isinstance(value, type):
            dsl_type = get_dsl_type(value)
            if dsl_type is None:
                report_error(span, f"expected DSL type but got {value}")
            return hir.Ctor(dsl_type)
        return None

    def parse_const(self, const: ast.Constant) -> hir.Value:
        span = hir.Span.from_ast(const)
        value = const.value
        if isinstance(value, (int, float, bool)):
            cst = hir.Constant(value, type=None, span=span)
            match value:
                case int():
                    cst.type = hir.GenericIntType()
                case float():
                    cst.type = hir.GenericFloatType()
                case bool():
                    cst.type = hir.BoolType()
            return cst
        report_error(
            const, f"unsupported constant type {type(value)}, wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")

    def parse_name(self, name: ast.Name, maybe_new_var: bool) -> hir.Ref | hir.Value | ComptimeValue:
        span = hir.Span.from_ast(name)
        var = self.vars.get(name.id)
        if var is not None:
            return var
        if maybe_new_var:
            var = hir.Var(name.id, None, span)
            self.vars[name.id] = var
            return var
        else:
            # look up in global namespace
            if name.id in self.globalns:
                resolved = self.globalns[name.id]
                # assert isinstance(resolved, ComptimeValue), type(resolved)
                if not isinstance(resolved, ComptimeValue):
                    resolved = ComptimeValue(resolved, None)
                if (converted := self.convert_constexpr(resolved, span)) is not None:
                    return converted
                if is_valid_comptime_value_in_dsl_code(resolved.value):
                    return resolved
        report_error(name, f"unknown variable {name.id}")

    def try_convert_comptime_value(self,  value: ComptimeValue, span: hir.Span | None = None) -> hir.Value:
        if (cst := self.convert_constexpr(value)) is not None:
            return cst
        report_error(
            span, f"unsupported constant type {type(value.value)}, wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")

    def parse_access_ref(self, expr: ast.Subscript | ast.Attribute) -> hir.Ref | hir.Value | ComptimeValue:
        span = hir.Span.from_ast(expr)
        if isinstance(expr, ast.Subscript):
            value = self.parse_expr(expr.value)
            if isinstance(value, ComptimeValue):
                report_error(
                    expr, "attempt to access comptime value in DSL code; wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")
            index = self.parse_expr(expr.slice)
            index = self.convert_to_value(index, span)
            return self.cur_bb().append(hir.Index(value, index, type=None, span=span))
        elif isinstance(expr, ast.Attribute):
            value = self.parse_expr(expr.value)
            attr_name = expr.attr
            if isinstance(value, ComptimeValue):
                return ComptimeValue(getattr(value.value, attr_name), None)
            assert value.type
            member_ty = value.type.member(attr_name)
            if not member_ty:
                report_error(
                    expr, f"member {attr_name} not found in type {value.type}")
            return self.cur_bb().append(hir.Member(value, attr_name, type=member_ty, span=span))
        raise NotImplementedError()  # unreachable

    def parse_call_impl(self, span: hir.Span | None, f: hir.FunctionLike | hir.FunctionTemplate, args: List[hir.Value | hir.Ref]) -> hir.Value | hir.TemplateMatchingError:
        if isinstance(f, hir.FunctionTemplate):
            if f.is_generic:
                template_resolve_args: hir.FunctionTemplateResolvingArgs = []
                template_params = f.params
                if len(template_params) != len(args):
                    return hir.TemplateMatchingError(
                        span,
                        f"Expected {len(template_params)} arguments, got {len(args)}")
                for i, (param, arg) in enumerate(zip(template_params, args)):
                    assert arg.type is not None
                    template_resolve_args.append((param, arg.type))
                resolved_f = f.resolve(template_resolve_args)
                if isinstance(resolved_f, hir.TemplateMatchingError):
                    return resolved_f
            else:
                resolved_f = f.resolve(None)
                assert not isinstance(resolved_f, hir.TemplateMatchingError)
        else:
            resolved_f = f
        if isinstance(resolved_f, hir.Function):
            param_tys = []
            for p in resolved_f.params:
                assert p.type, f"Parameter {p.name} has no type"
                param_tys.append(p.type)
            if len(param_tys) != len(args):
                raise hir.TypeInferenceError(
                    span,
                    f"Expected {len(param_tys)} arguments, got {len(args)}"
                )
            for i, (param_ty, arg) in enumerate(zip(param_tys, args)):
                assert arg.type is not None
                if not hir.is_type_compatible_to(arg.type, param_ty):
                    raise hir.TypeInferenceError(
                        span,
                        f"Argument {i} expected {param_ty}, got {arg}"
                    )
            assert resolved_f.return_type
            return self.cur_bb().append(hir.Call(resolved_f, args, type=resolved_f.return_type, span=span))
        else:
            args_ty = []
            for arg in args:
                assert arg.type is not None
                args_ty.append(arg.type)
            ty = resolved_f.type_rule.infer(args_ty)
            return self.cur_bb().append(hir.Call(resolved_f, args, type=ty, span=span))
        raise NotImplementedError()  # unreachable

    def parse_call(self, expr: ast.Call) -> hir.Value:
        func = self.parse_expr(expr.func)

        if isinstance(func, hir.Ref):
            report_error(expr, f"function expected")
        elif isinstance(func, ComptimeValue):
            func = self.try_convert_comptime_value(
                func, hir.Span.from_ast(expr))

        def collect_args() -> List[hir.Value | hir.Ref]:
            args = [self.parse_expr(arg) for arg in expr.args]
            for i, arg in enumerate(args):
                if isinstance(arg, ComptimeValue):
                    args[i] = self.try_convert_comptime_value(
                        arg, hir.Span.from_ast(expr.args[i]))
            return cast(List[hir.Value | hir.Ref], args)

        if isinstance(func, hir.Ctor):
            cls = func.type
            assert cls
            init = cls.method("__init__")
            tmp = self.cur_bb().append(hir.Alloca(cls, span=hir.Span.from_ast(expr)))
            assert init is not None
            call = self.parse_call_impl(
                hir.Span.from_ast(expr), init,  [tmp]+collect_args())
            if isinstance(call, hir.TemplateMatchingError):
                report_error(expr, call.message)
            assert isinstance(call, hir.Call)
            return call

        if not isinstance(func.type, hir.FunctionType):
            report_error(expr, f"function expected")

        ret = self.parse_call_impl(
            hir.Span.from_ast(expr), func.type.func_like,  collect_args())
        if isinstance(ret, hir.TemplateMatchingError):
            report_error(expr, ret.message)
        return ret

    def parse_binop(self, expr: ast.BinOp) -> hir.Value:
        binop_to_op_str: Dict[type, str] = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.FloorDiv: "//",
            ast.Mod: "%",
            ast.Pow: "**",
            ast.LShift: "<<",
            ast.RShift: ">>",
            ast.BitAnd: '&',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",

        }
        op_str = binop_to_op_str[type(expr.op)]
        lhs = self.parse_expr(expr.left)
        if isinstance(lhs, ComptimeValue):
            lhs = self.try_convert_comptime_value(lhs, hir.Span.from_ast(expr))
        if not lhs.type:
            report_error(
                expr.left, f"unable to infer type of left operand of binary operation {op_str}")
        rhs = self.parse_expr(expr.right)
        if isinstance(rhs, ComptimeValue):
            rhs = self.try_convert_comptime_value(rhs, hir.Span.from_ast(expr))
        if not rhs.type:
            report_error(
                expr.right, f"unable to infer type of right operand of binary operation {op_str}")
        ops = BINOP_TO_METHOD_NAMES[type(expr.op)]

        def infer_binop(name: str, rname: str):
            assert lhs.type and rhs.type
            try:
                if (method := lhs.type.method(name)) and method:
                    ret = self.parse_call_impl(
                        hir.Span.from_ast(expr), method, [lhs, rhs])
                elif (method := rhs.type.method(rname)) and method:
                    ret = self.parse_call_impl(
                        hir.Span.from_ast(expr), method, [rhs, lhs])
                else:
                    report_error(
                        expr, f"Operator {op_str} not defined for types {lhs.type} and {rhs.type}")
                return ret
            except hir.TypeInferenceError as e:
                e.span = hir.Span.from_ast(expr)
                raise e from e
        return infer_binop(ops[0], ops[1])

    def parse_expr(self, expr: ast.expr, maybe_new_var: bool = False) -> hir.Ref | hir.Value | ComptimeValue:
        match expr:
            case ast.Constant():
                return self.parse_const(expr)
            case ast.Name():
                ret = self.parse_name(expr, maybe_new_var)
                return ret
            case ast.Subscript() | ast.Attribute():
                ret = self.parse_access_ref(expr)
                return ret
            case ast.BinOp():
                return self.parse_binop(expr)
            case ast.Call():
                return self.parse_call(expr)
            case _:
                raise RuntimeError(f"Unsupported expression: {ast.dump(expr)}")

    def eval_expr(self, tree: ast.Expression | ast.expr):
        if isinstance(tree, ast.expr):
            tree = ast.Expression(tree)
        code_object = compile(tree, "<string>", "eval")
        localns = {}
        for name, v in self.vars.items():
            if isinstance(v, ComptimeValue):
                localns[name] = v.value
        return eval(code_object, self.globalns, localns)

    def convert_to_value(self, value: hir.Value | hir.Ref | ComptimeValue, span: Optional[hir.Span] = None) -> hir.Value:
        if isinstance(value, ComptimeValue):
            value = self.try_convert_comptime_value(value, span)
        if isinstance(value, hir.Ref):
            value = hir.Load(value)
            self.cur_bb().append(value)
        return value

    def parse_stmt(self, stmt: ast.stmt):
        span = hir.Span.from_ast(stmt)
        match stmt:
            case ast.Return():
                def check_return_type(ty: hir.Type):
                    assert self.parsed_func
                    if self.parsed_func.return_type is None:
                        self.parsed_func.return_type = ty
                    else:
                        if not hir.is_type_compatible_to(ty, self.parsed_func.return_type):
                            report_error(
                                stmt, f"return type mismatch: expected {self.parsed_func.return_type}, got {ty}")
                if stmt.value:
                    value = self.parse_expr(stmt.value)
                    value = self.convert_to_value(value, span)
                    assert value.type
                    check_return_type(value.type)
                    self.cur_bb().append(hir.Return(value))
                else:
                    check_return_type(hir.UnitType())
                    self.cur_bb().append(hir.Return(None))
            case ast.Assign():
                if len(stmt.targets) != 1:
                    report_error(stmt, f"expected single target")
                target = stmt.targets[0]
                var = self.parse_expr(target, maybe_new_var=True)
                if isinstance(var, hir.Value):
                    report_error(target, f"value cannot be assigned")
                value = self.parse_expr(stmt.value)
                if isinstance(var, ComptimeValue):
                    if not isinstance(value, ComptimeValue):
                        report_error(
                            stmt, f"comptime value cannot be assigned with DSL value")
                    var.update(value.value)
                    return None
                value = self.convert_to_value(value, span)
                assert value.type
                if var.type:
                    if not hir.is_type_compatible_to(value.type, var.type):
                        report_error(
                            stmt, f"expected {var.type}, got {value.type}")
                else:
                    var.type = value.type
                return hir.Assign(var, value, span)
            case ast.AnnAssign():
                var = self.parse_expr(stmt.target, maybe_new_var=True)
                if isinstance(var, hir.Value):
                    report_error(stmt, f"value cannot be assigned")
                elif isinstance(var, hir.Ref):
                    type_annotation = self.eval_expr(stmt.annotation)
                    type_hint = classinfo.parse_type_hint(type_annotation)
                    ty = self.parse_type(type_hint)
                    assert ty
                    var.type = ty

                if stmt.value:
                    value = self.parse_expr(stmt.value)

                    if isinstance(var, ComptimeValue):
                        if not isinstance(value, ComptimeValue):
                            report_error(
                                stmt, f"comptime value cannot be assigned with DSL value")
                        var.update(value.value)
                        return None
                    if isinstance(value, ComptimeValue):
                        value = self.try_convert_comptime_value(
                            value, span)
                    elif isinstance(value, hir.Ref):
                        value = hir.Load(value)
                    assert value.type
                    assert ty
                    if not hir.is_type_compatible_to(value.type, ty):
                        report_error(
                            stmt, f"expected {ty}, got {value.type}")
                    return hir.Assign(var, value, span)
                else:
                    assert isinstance(var, hir.Var)
            case ast.Expression():
                self.parse_expr(stmt.body)
            case ast.Pass():
                return
            case _:
                raise RuntimeError(f"Unsupported statement: {ast.dump(stmt)}")

    def parse_body(self):
        assert self.parsed_func is not None
        body = self.func_def.body
        self.bb_stack.append(hir.BasicBlock())
        parsed_body = [self.parse_stmt(stmt) for stmt in body]
        assert len(self.bb_stack) == 1
        self.parsed_func.body = self.bb_stack.pop()
        self.parsed_func.locals = list(
            [x for x in self.vars.values() if isinstance(x, hir.Var)])
        return self.parsed_func


UNARY_OP_TO_METHOD_NAMES: Dict[type, str] = {
    ast.UAdd: "__pos__",
    ast.USub: "__neg__",
    ast.Not: "__not__",
    ast.Invert: "__invert__",
}


BINOP_TO_METHOD_NAMES: Dict[type, List[str]] = {
    ast.Add: ["__add__", "__radd__"],
    ast.Sub: ["__sub__", "__rsub__"],
    ast.Mult: ["__mul__", "__rmul__"],
    ast.Div: ["__truediv__", "__rtruediv__"],
    ast.FloorDiv: ["__floordiv__", "__rfloordiv__"],
    ast.Mod: ["__mod__", "__rmod__"],
    ast.Eq: ["__eq__", "__eq__"],
    ast.NotEq: ["__ne__", "__ne__"],
    ast.Lt: ["__lt__", "__gt__"],
    ast.LtE: ["__le__", "__ge__"],
    ast.Gt: ["__gt__", "__lt__"],
    ast.GtE: ["__ge__", "__le__"],
    ast.BitAnd: ["__and__", "__rand__"],
    ast.BitOr: ["__or__", "__ror__"],
    ast.BitXor: ["__xor__", "__rxor__"],
    ast.LShift: ["__lshift__", "__rlshift__"],
    ast.RShift: ["__rshift__", "__rrshift__"],
    ast.Pow: ["__pow__", "__rpow__"],
}
