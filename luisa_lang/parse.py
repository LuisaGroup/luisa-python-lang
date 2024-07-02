import ast
import os
from typing import List, Optional, Union, overload
import luisa_lang
import luisa_lang.hir as hir
import sys
from luisa_lang.hir import (
    Env,
    Path,
    Type,
    BoundType,
    ParametricType,
    Function,
    Var,
    UnresolvedCall,
)
from typing import NoReturn, cast, Set, reveal_type


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


def parse_type(type: ast.AST, ctx: hir.Context) -> Type:
    if isinstance(type, ast.Name):
        ty = ctx.items.lookup(Path(type.id))
        if ty is None:
            report_error(type, f"unknown type {type.id}")
        if not isinstance(ty, Type):
            report_error(type, f"expected type")
        return ty
    elif isinstance(type, ast.Subscript):
        parameteric_type = parse_type(type.value, ctx)
        if not isinstance(parameteric_type, ParametricType):
            report_error(type, f"expected parameteric type")
        slice = type.slice
        args = []
        if isinstance(slice, ast.Name):
            args = [parse_type(slice, ctx)]
        elif isinstance(slice, ast.Tuple):
            args = [parse_type(arg, ctx) for arg in slice.elts]
        else:
            report_error(type, f"unparsable type arguments")
        if len(args) != len(parameteric_type.params):
            report_error(type, f"expected {len(parameteric_type.params)} arguments")
        return BoundType(parameteric_type, args)
    elif isinstance(type, ast.Constant):
        if type.value is None:
            return hir.UnitType()
        else:
            raise NotImplementedError(f"unsupported constant type {type.value}")
    else:
        report_error(type, f"unparsable type")


def resolve_file(filename: str) -> Optional[str]:
    search_paths = ["."] + sys.path
    for path in search_paths:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    return None


def parse_import(imp: ast.Import | ast.ImportFrom, ctx: hir.Context):
    if isinstance(imp, ast.Import):
        for name in imp.names:
            resolved_file = resolve_file(name.name)
            if not resolved_file:
                report_error(imp, f"cannot find module {name.name}")
            module_ast = ast.parse(resolved_file)
            assert isinstance(module_ast, ast.Module)
            module_parser = ModuleParser(module_ast, ctx)
            module_parser.parse()
            asname = name.asname
    else:
        pass


class FuncParser:
    ctx: hir.Context
    vars: Env[str, hir.Var]

    def __init__(self, ctx: hir.Context):
        self.ctx = ctx
        self.vars = Env()

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


class ModuleParser:
    ctx: hir.Context
    module: ast.Module

    def __init__(self, module: ast.Module, ctx: hir.Context):
        self.module = module
        self.ctx = ctx

    def parse(self) -> hir.Module:
        m = hir.Module()
        for stmt in self.module.body:
            if isinstance(stmt, ast.FunctionDef):
                f = parse_function(stmt, self.ctx)
                m.functions[f.name] = f
            else:
                raise NotImplementedError(f"unsupported statement {stmt}")
        return m



def parse_function(func: ast.FunctionDef, ctx: hir.Context) -> Function:
    name = func.name
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
    return_type: Type
    if func.returns is None:
        return_type = hir.UnitType()
    else:
        return_type = parse_type(func.returns, ctx)
    body = func.body
    parser = FuncParser(ctx)
    parsed_body = [parser.parse_stmt(stmt) for stmt in body]
    params = []
    for i, arg_type in enumerate(arg_types):
        span = hir.Span.from_ast(args.args[i])
        params.append(hir.Var(f"arg{i}", arg_type, span))
    return Function(
        name, params, return_type, [x for x in parsed_body if x is not None]
    )


# # attempt to parse the AST and update the context
# def parse(tree: ast.AST, ctx: hir.Context):
#     print(ast.dump(tree))
#     assert isinstance(tree, ast.Module)
#     for stmt in tree.body:
#         if isinstance(stmt, ast.FunctionDef):
#             parse_function(stmt, ctx)
#         else:
#             raise NotImplementedError(f"unsupported statement {stmt}")
