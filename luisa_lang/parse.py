import ast
import os
from types import ModuleType
from typing import Any, Dict, List, Optional, Tuple, Union, overload
import luisa_lang
import luisa_lang.hir as hir
import sys
from luisa_lang.hir import (
    Path,
    Type,
    BoundType,
    ParametricType,
    Function,
    Var,
    UnresolvedCall,
)
from typing import NoReturn, cast, Set, reveal_type
from enum import Enum


def _report_error_span(span: hir.Span, message: str) -> NoReturn:
    raise RuntimeError(f"error at {span}: {message}")


def _report_error_tree(tree: ast.AST, message: str) -> NoReturn:
    span = hir.Span.from_ast(tree)
    if span is not None:
        _report_error_span(span, message)
    else:
        raise RuntimeError(f"error: {message}")


@overload
def report_error(obj: hir.Span, message: str) -> NoReturn: ...
@overload
def report_error(obj: ast.AST, message: str) -> NoReturn: ...
def report_error(obj, message: str) -> NoReturn:
    if isinstance(obj, hir.Span):
        _report_error_span(obj, message)
    elif isinstance(obj, ast.AST):
        _report_error_tree(obj, message)
    else:
        raise NotImplementedError(f"unsupported object {obj}")


class NameKind(Enum):
    MODULE = 0
    TYPE = 1
    FUNCTION = 2
    OTHER = 3


NameEvalResult = Tuple[NameKind, Any]
class ParsingContext:
    globals: Dict[str, Any]
    global_ctx: hir.GlobalContext
    name_eval_cache: Dict[str, Optional[NameEvalResult]]

    def __init__(self, globals: Dict[str, Any], global_ctx: hir.GlobalContext):
        self.globals = globals
        self.global_ctx = global_ctx
        self.name_eval_cache = {}

    def __eval_name(self, name: str) -> Optional[NameEvalResult]:
        if name in self.name_eval_cache:
            return self.name_eval_cache[name]
        try:
            result = eval(name, self.globals)
            if isinstance(result, ModuleType):
                return (NameKind.MODULE, result)
            if isinstance(result, type):
                return (NameKind.TYPE, result)
            if callable(result):
                return (NameKind.FUNCTION, result)
            result = (NameKind.OTHER, result)
        except NameError:
            result = None
        self.name_eval_cache[name] = result
        return result

    def parse_type(self, type: ast.AST) -> Type:
        if isinstance(type, ast.Name):
            r = self.__eval_name(type.id)
            if r is None:
                report_error(type, f"unknown type {type.id}")
            kind, result = r
            if kind != NameKind.TYPE:
                report_error(type, f"expected {NameKind.TYPE} but got {kind}")
            result = cast(Type, result)
            ty = self.global_ctx.types.get(result)
            if ty is None:
                report_error(type, f"unknown type {type.id}")
            if not isinstance(ty, Type):
                report_error(type, f"expected type")
            return ty
        elif isinstance(type, ast.Subscript):
            parameteric_type = self.parse_type(type.value)
            if not isinstance(parameteric_type, ParametricType):
                report_error(type, f"expected parameteric type")
            slice = type.slice
            args = []
            if isinstance(slice, ast.Name):
                args = [self.parse_type(slice)]
            elif isinstance(slice, ast.Tuple):
                args = [self.parse_type(arg) for arg in slice.elts]
            else:
                report_error(type, f"unparsable type arguments")
            if len(args) != len(parameteric_type.params):
                report_error(type, f"expected {len(parameteric_type.params)} arguments")
            return BoundType(parameteric_type, args)
        elif isinstance(type, ast.Attribute):
            pass
        elif isinstance(type, ast.Constant):
            if type.value is None:
                return hir.UnitType()
            else:
                raise NotImplementedError(f"unsupported constant type {type.value}")
        else:
            report_error(type, f"unparsable type")


class FuncParser:
    ctx: hir.GlobalContext
    vars: Env[str, hir.Var]
    func: ast.FunctionDef
    arg_types: List[Type]
    return_type: Optional[Type]

    def __init__(self, func: ast.FunctionDef, ctx: hir.GlobalContext):
        self.ctx = ctx
        self.vars = Env()
        self.func = func
        self.arg_types = []
        self.return_type = None
        self._init_signature()

    def _init_signature(
        self,
    ):
        assert self.return_type is None
        func = self.func
        ctx = self.ctx
        args = func.args
        if args.vararg is not None:
            report_error(args.vararg, f"vararg not supported")
        if args.kwarg is not None:
            report_error(args.kwarg, f"kwarg not supported")
        arg_types: List[Type] = []
        for arg in args.args:
            if arg.annotation is None:
                raise RuntimeError("TODO: infer type")
            arg_types.append(parse_type(arg.annotation, ctx))
        if func.returns is None:
            self.return_type = hir.UnitType()
        else:
            self.return_type = parse_type(func.returns, ctx)

    def parse_expr(self, expr: ast.expr) -> hir.Value:
        span = hir.Span.from_ast(expr)
        if (
            isinstance(expr, ast.Name)
            or isinstance(expr, ast.Attribute)
            or isinstance(expr, ast.Subscript)
        ):
            ref = self.parse_ref(expr)
            return hir.Load(ref)
        if isinstance(expr, ast.Constant):
            raise RuntimeError("TODO: parse constant")
        if isinstance(expr, ast.BinOp):
            lhs = self.parse_expr(expr.left)
            rhs = self.parse_expr(expr.right)
            m0 = {
                ast.Add: "+",
                ast.Sub: "-",
                ast.Mult: "*",
                ast.Div: "/",
                ast.FloorDiv: "//",
                ast.Mod: "%",
                ast.Pow: "**",
                ast.LShift: "<<",
            }
            op = m0[type(expr.op)]
            return UnresolvedCall(op, [lhs, rhs], span=span)
        if isinstance(expr, ast.UnaryOp):
            operand = self.parse_expr(expr.operand)
            m1 = {
                ast.USub: "-",
                ast.UAdd: "+",
                ast.Invert: "~",
            }
            op = m1[type(expr.op)]
            return UnresolvedCall(op, [operand])
        if isinstance(expr, ast.Call):
            func = self.parse_expr(expr.func)
            args = [self.parse_expr(arg) for arg in expr.args]
            return hir.Call(func, args, span)
        report_error(expr, f"unsupported expression {expr}")

    def parse_ref(self, expr: ast.expr, maybe_new_var=False) -> hir.Ref:
        span = hir.Span.from_ast(expr)
        if isinstance(expr, ast.Name):
            var = self.vars.lookup(expr.id)
            if var is None:
                if not maybe_new_var:
                    report_error(expr, f"unknown variable {expr.id}")
                var = hir.Var(expr.id, None, span)
                self.vars.bind(expr.id, var)
            return var
        if isinstance(expr, ast.Attribute):
            obj = self.parse_ref(expr.value)
            return hir.Member(obj, expr.attr, span)
        if isinstance(expr, ast.Subscript):
            obj = self.parse_ref(expr.value)
            index = self.parse_expr(expr.slice)
            return hir.Index(obj, index, span)
        return hir.ValueRef(self.parse_expr(expr))
        # report_error(expr, f"unsupported expression {expr}")

    def parse_stmt(self, stmt: ast.stmt) -> Optional[hir.Stmt]:
        if isinstance(stmt, ast.AnnAssign):
            type_annotation = stmt.annotation
            ty = parse_type(type_annotation, self.ctx)
            if not isinstance(stmt.target, ast.Name):
                report_error(stmt, f"expected name")
            var = self.parse_ref(stmt.target, maybe_new_var=True)
            if stmt.value is None:
                if not isinstance(var, hir.Var):
                    report_error(stmt, f"expected variable")
                return hir.VarDecl(var, ty)
            value = self.parse_expr(stmt.value)
            return hir.Assign(var, ty, value)
        if isinstance(stmt, ast.Assign):
            if len(stmt.targets) != 1:
                report_error(stmt, f"expected single target")
            target = stmt.targets[0]
            if not isinstance(target, ast.Name):
                report_error(target, f"expected name")
            var = self.parse_ref(target, maybe_new_var=True)
            value = self.parse_expr(stmt.value)
            return hir.Assign(var, None, value)
        if isinstance(stmt, ast.Pass):
            return None
        report_error(stmt, f"unsupported statement {stmt}")

    def parse_body(self) -> hir.Function:
        body = self.func.body
        parsed_body = [self.parse_stmt(stmt) for stmt in body]
        params = []
        args = self.func.args
        for i, arg_type in enumerate(self.arg_types):
            span = hir.Span.from_ast(args.args[i])
            params.append(hir.Var(f"arg{i}", arg_type, span))
        assert self.return_type is not None
        return Function(
            self.func.name,
            params,
            self.return_type,
            [x for x in parsed_body if x is not None],
        )


class ModuleParser:
    ctx: hir.GlobalContext
    module: ast.Module
    functions: Dict[str, FuncParser]

    def __init__(self, module: ast.Module, ctx: hir.GlobalContext):
        self.module = module
        self.ctx = ctx
        self.functions = {}

    def parse(self) -> hir.Module:
        m = hir.Module()
        for stmt in self.module.body:
            if isinstance(stmt, ast.FunctionDef):
                f = FuncParser(stmt, self.ctx)
                self.functions[stmt.name] = f
            else:
                raise NotImplementedError(f"unsupported statement {stmt}")
        for name, f in self.functions.items():
            m.functions[name] = f.parse_body()
        return m
