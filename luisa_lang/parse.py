import ast
import os
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload
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


# def _retrieve_metadata(obj: Any) -> Optional[hir.FuncMetadata | hir.StructMetadata]:
#     meta = getattr(obj, '__lc_metadata', None)

NamedResolution = hir.Type | hir.Function | hir.Var


def _is_hir_types(obj: Any) -> bool:
    return (
        isinstance(obj, hir.Type)
        or isinstance(obj, hir.Function)
        or isinstance(obj, hir.Var)
    )


class AccessKind(Enum):
    SUBSCRIPT = 0
    ATTRIBUTE = 1


AccessKey = Union[str, ast.AST, "AccessChain"]


class AccessChain:
    """
    AccessChain are used to represent access chains like `a.b.c.d` or `a[b].c.d`,
    where keys are resolvable at compile time.
    Usually the chain can be resolved to either types or functions.
    """

    parent: Any
    chain: List[Tuple[AccessKind, List[AccessKey]]]

    def __init__(self, parent: Any):
        self.parent = parent
        self.chain = []


class ParsingContext:
    globals: Dict[str, Any]
    global_ctx: hir.GlobalContext
    name_eval_cache: Dict[str, Optional[Any]]

    def __init__(self, globals: Dict[str, Any], global_ctx: hir.GlobalContext):
        self.globals = globals
        self.global_ctx = global_ctx
        self.name_eval_cache = {}

    def __eval_name(self, name: str) -> Optional[Any]:
        try:
            result = eval(name, self.globals)
            self.name_eval_cache[name] = result
            return result
        except NameError:
            self.name_eval_cache[name] = None
            return None

    # def __resolve_object(self, obj: Any) -> Optional[NamedResolution]:
    #     if _is_hir_types(obj):
    #         return obj
    #     pass

    def __resolve_access_chain(self, tree: ast.AST) -> Optional[AccessChain]:
        """
        Attempt to resolve a static access chain from the given AST tree.
        """

        def check_is_access(tree: ast.AST) -> bool:
            return (
                isinstance(tree, ast.Name)
                or isinstance(tree, ast.Attribute)
                or isinstance(tree, ast.Subscript)
            )

        if isinstance(tree, ast.Name):
            r = self.__eval_name(tree.id)
            if r is None:
                return None
            return AccessChain(r)
        elif isinstance(tree, ast.Attribute):
            parent = self.__resolve_access_chain(tree.value)
            if parent is None:
                return None
            parent.chain.append((AccessKind.ATTRIBUTE, [tree.attr]))
            return parent
        elif isinstance(tree, ast.Subscript):
            parent = self.__resolve_access_chain(tree.value)
            if parent is None:
                return None
            if isinstance(tree.slice, ast.Tuple):
                keys: List[AccessKey] = []
                for s in tree.slice.elts:
                    if not check_is_access(s):
                        return None
                    resolve_s = self.__resolve_access_chain(s)
                    if resolve_s is None:
                        return None
                    keys.append(resolve_s)
                parent.chain.append((AccessKind.SUBSCRIPT, keys))
            if check_is_access(tree.slice):
                child_chain = self.__resolve_access_chain(tree.slice)
                if child_chain is None:
                    return None
                parent.chain.append((AccessKind.SUBSCRIPT, [tree.slice]))
                return parent
            parent.chain.append((AccessKind.SUBSCRIPT, [tree.slice]))
            return parent
        report_error(tree, f"unsupported access chain {tree}")

    def parse_type(self, type_tree: ast.AST) -> Optional[Type]:
        acess_chain = self.__resolve_access_chain(type_tree)
        if acess_chain is None:
            return None
        cur: Any = None
        chain_idx = None
        while True:
            if isinstance(cur, type):
                if cur in self.global_ctx.types:
                    if chain_idx is None or chain_idx >= len(acess_chain.chain):
                        return self.global_ctx.types[cur]
                    return self.global_ctx.types[cur]
            break
        raise NotImplementedError("TODO: parse type")


class FuncParser:
    p_ctx: ParsingContext
    vars: Dict[str, hir.Var]
    func: ast.FunctionDef
    arg_types: List[Type]
    return_type: Optional[Type]

    def __init__(self, func: ast.FunctionDef, p_ctx: ParsingContext) -> None:
        self.p_ctx = p_ctx
        self.vars = {}
        self.func = func
        self.arg_types = []
        self.return_type = None
        self._init_signature()

    def _init_signature(
        self,
    ) -> None:
        assert self.return_type is None
        func = self.func
        p_ctx = self.p_ctx
        args = func.args
        if args.vararg is not None:
            report_error(args.vararg, f"vararg not supported")
        if args.kwarg is not None:
            report_error(args.kwarg, f"kwarg not supported")
        arg_types: List[Type] = []
        for arg in args.args:
            if arg.annotation is None:
                raise RuntimeError("TODO: infer type")
            if (arg_ty := p_ctx.parse_type(arg.annotation)) is not None:
                arg_types.append(arg_ty)
        if func.returns is None:
            self.return_type = hir.UnitType()
        else:
            self.return_type = p_ctx.parse_type(func.returns)

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
            var = self.vars.get(expr.id)
            if var is None:
                if not maybe_new_var:
                    report_error(expr, f"unknown variable {expr.id}")
                var = hir.Var(expr.id, None, span)
                self.vars[expr.id] = var
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
            ty = self.p_ctx.parse_type(type_annotation)
            if ty is None:
                report_error(type_annotation, f"failed to parse type")
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
