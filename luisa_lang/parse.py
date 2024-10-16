import ast
import os
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload
import luisa_lang
from luisa_lang._utils import report_error
import luisa_lang.hir as hir
import sys
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

from luisa_lang.hir.defs import get_dsl_type


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
    where the prefixes of the chain can often be resolved to a python object.
    For example,
    - `my_module.a_global_var['a']` can be resolved to a python object.
    - `my_module.my_type` would be resolved into a type.
    In some cases, the chain cannot be fully resolved, then we attempt
    to resolve as much as possible and return the most resolved object and the remaining chain.
    """

    parent: Any
    chain: List[Tuple[AccessKind, List[AccessKey]]]

    def __init__(
        self,
        parent: Any,
        chain: Optional[List[Tuple[AccessKind, List[AccessKey]]]] = None,
    ):
        self.parent = parent
        if chain is None:
            self.chain = []
        else:
            self.chain = chain

    def __repr__(self) -> str:
        return f"AccessChain({self.parent}, {self.chain})"

    def resolve(self) -> Tuple[Any, Optional["AccessChain"]]:
        """
        Attempt to resolve the access chain.
        if the chain is fully resolved, return the final object and None.
        otherwise, return most resolved object and the remaining chain.
        """
        cur = self.parent
        chain_idx = None

        def eval_keys(
            cur: Any, access: Tuple[AccessKind, List[AccessKey]]
        ) -> Tuple[bool, Any]:
            kind, keys = access
            if kind == AccessKind.ATTRIBUTE:
                assert len(keys) == 1, f"expected single key"
                assert isinstance(keys[0], str), f"expected string key"
                return True, getattr(cur, keys[0])
            # kind == AccessKind.SUBSCRIPT
            evaled_keys: List[Any] = []
            for key in keys:
                if isinstance(key, str):
                    evaled_keys.append(key)
                elif isinstance(key, ast.AST):
                    raise NotImplementedError("TODO: eval ast key")
                else:
                    assert isinstance(
                        key, AccessChain), f"expected AccessChain key"
                    resolved, remaining = key.resolve()
                    if remaining is not None:
                        return False, None
                    evaled_keys.append(resolved)
            try:
                return True, cur[tuple(evaled_keys)]
            except KeyError:
                return False, None

        def get_access_key() -> Optional[Tuple[AccessKind, List[AccessKey]]]:
            if chain_idx is None:
                if len(self.chain) == 0:
                    return None
                return self.chain[0]
            if chain_idx + 1 >= len(self.chain):
                return None
            return self.chain[chain_idx + 1]

        ctx = hir.GlobalContext.get()
        while True:
            access = get_access_key()

            # check type of cur to determine what to do
            # is cur a module?
            if type(cur) == ModuleType:
                if access is None:
                    break
                success, cur = eval_keys(cur, access)
                if not success:
                    break
            # is cur a type?
            elif type(cur) == type:
                hir_ty = ctx.types.get(cur)
                if hir_ty is None:
                    if access is None:
                        break
                    success, cur = eval_keys(cur, access)
                    if not success:
                        break
                else:
                    if access is None:
                        return hir_ty, None
                    raise NotImplementedError()
            if chain_idx is None:
                if len(self.chain) == 0:
                    break
                chain_idx = 0
            else:
                chain_idx += 1
                if chain_idx >= len(self.chain):
                    break
        if chain_idx is None:
            return cur, self
        return cur, AccessChain(cur, self.chain[chain_idx:])


class ParsingContext:
    globals: Dict[str, Any]
    global_ctx: hir.GlobalContext
    name_eval_cache: Dict[str, Optional[Any]]

    def __init__(self, globals: Dict[str, Any]):
        self.globals = globals
        self.global_ctx = hir.GlobalContext.get()
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

    def _parse_access_chain(self, tree: ast.AST) -> Optional[AccessChain]:
        """
        Attempt to resolve a static access chain from the given AST tree.

        Example:
        - `module.type` -> `AccessChain(module, [(AccessKind.ATTRIBUTE, ['type'])])`
        - `identifier.attr` -> None
        - `module.type['key']` -> `AccessChain(module, [(AccessKind.ATTRIBUTE, ['type']), (AccessKind.SUBSCRIPT, ['key'])])`

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
            parent = self._parse_access_chain(tree.value)
            if parent is None:
                return None
            parent.chain.append((AccessKind.ATTRIBUTE, [tree.attr]))
            return parent
        elif isinstance(tree, ast.Subscript):
            parent = self._parse_access_chain(tree.value)
            if parent is None:
                return None
            if isinstance(tree.slice, ast.Tuple):
                keys: List[AccessKey] = []
                for s in tree.slice.elts:
                    if not check_is_access(s):
                        return None
                    resolve_s = self._parse_access_chain(s)
                    if resolve_s is None:
                        return None
                    keys.append(resolve_s)
                parent.chain.append((AccessKind.SUBSCRIPT, keys))
            if check_is_access(tree.slice):
                child_chain = self._parse_access_chain(tree.slice)
                if child_chain is None:
                    return None
                parent.chain.append((AccessKind.SUBSCRIPT, [tree.slice]))
                return parent
            parent.chain.append((AccessKind.SUBSCRIPT, [tree.slice]))
            return parent
        return None
        # report_error(tree, f"unsupported access chain {tree}")

    def parse_type(self, type_tree: ast.AST) -> Optional[Type]:
        acess_chain: AccessChain | None = self._parse_access_chain(type_tree)
        if acess_chain is None:
            return None
        # print(acess_chain)
        resolved, remaining = acess_chain.resolve()
        # print(resolved, remaining)
        if remaining is not None:
            report_error(type_tree, f"failed to resolve type")
        if isinstance(resolved, hir.Type):
            return resolved
        return None


class FuncParser:
    p_ctx: ParsingContext
    vars: Dict[str, hir.Var]
    func: ast.FunctionDef
    arg_types: List[Type]
    return_type: Optional[Type]
    name: str

    def __init__(self, name: str, func: ast.FunctionDef, p_ctx: ParsingContext) -> None:
        self.name = name
        self.p_ctx = p_ctx
        self.vars = {}
        self.func = func
        self.arg_types = []
        self.return_type = None
        self._init_signature()
        # print(self.arg_types, "->", self.return_type)

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
        for arg in args.args:
            if arg.annotation is None:
                raise RuntimeError("TODO: infer type")
            if (arg_ty := p_ctx.parse_type(arg.annotation)) is not None:
                self.arg_types.append(arg_ty)
                self.vars[arg.arg] = hir.Var(
                    arg.arg, arg_ty, hir.Span.from_ast(arg))
            else:
                report_error(arg.annotation, f"invalid type for argument")
        if func.returns is None:
            self.return_type = hir.UnitType()
        else:
            self.return_type = p_ctx.parse_type(func.returns)

    def parse_const(self, const: ast.Constant) -> hir.Value:
        span = hir.Span.from_ast(const)
        value = const.value
        if isinstance(value, (int, float, str, bool)):
            return hir.Constant(value, span)
        report_error(const, f"unsupported constant type {type(value)}")

    def parse_expr(self, expr: ast.expr) -> hir.Value:
        span = hir.Span.from_ast(expr)
        if (
            isinstance(expr, ast.Name)
            or isinstance(expr, ast.Attribute)
            or isinstance(expr, ast.Subscript)
        ):
            ref = self.parse_ref(expr)
            assert isinstance(ref, hir.Ref)
            return hir.Load(ref)
        if isinstance(expr, ast.Constant):
            return self.parse_const(expr)
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
                ast.RShift: ">>"
            }
            op = m0[type(expr.op)]
            return hir.Call(op, [lhs, rhs], kind=hir.CallOpKind.BINARY_OP, resolved=False, span=span)
        if isinstance(expr, ast.UnaryOp):
            operand = self.parse_expr(expr.operand)
            m1 = {
                ast.USub: "-",
                ast.UAdd: "+",
                ast.Invert: "~",
            }
            op = m1[type(expr.op)]
            return hir.Call(op, [operand], kind=hir.CallOpKind.UNARY_OP, resolved=False, span=span)
        if isinstance(expr, ast.Compare):
            comop_to_str = {
                ast.Eq: "==",
                ast.NotEq: "!=",
                ast.Lt: "<",
                ast.LtE: "<=",
                ast.Gt: ">",
                ast.GtE: ">=",
            }
            parsed_expr = self.parse_expr(expr.left)
            left_cmp_expr: hir.Value = parsed_expr
            for i, cmpop in enumerate(expr.ops):
                right = self.parse_expr(expr.comparators[i])
                op = comop_to_str[type(cmpop)]
                cmp_expr_tmp = hir.Call(op, [left_cmp_expr, right], kind=hir.CallOpKind.BINARY_OP, resolved=False, span=span)
                left_cmp_expr = right
                if i > 0:
                    parsed_expr = hir.Call('and', [parsed_expr, cmp_expr_tmp], kind=hir.CallOpKind.BINARY_OP, resolved=False, span=span)
                else:
                    parsed_expr = cmp_expr_tmp
            return parsed_expr
        if isinstance(expr, ast.Call):
            func = self.parse_expr(expr.func)
            args = [self.parse_expr(arg) for arg in expr.args]
            return hir.Call(func, args, kind=hir.CallOpKind.FUNC, resolved=True, span=span)
        report_error(expr, f"unsupported expression {expr}")

    def parse_ref(self, expr: ast.expr, maybe_new_var=False) -> hir.Ref | hir.Value:
        """
        Attempt to parse a reference from the given AST expression.
        In particule, it tries to parse expressions like Subscript, Name, Attribute.
        For other cases, it will return a Value.
        """
        span = hir.Span.from_ast(expr)
        access_chain: AccessChain | None = self.p_ctx._parse_access_chain(expr)
        if not access_chain:
            if isinstance(expr, ast.Subscript):
                obj = self.parse_ref(expr.value)
                index = self.parse_expr(expr.slice)
                return hir.Index(obj, index, span)
            elif isinstance(expr, ast.Name):
                var = self.vars.get(expr.id)
                if var is None:
                    if not maybe_new_var:
                        report_error(expr, f"unknown variable {expr.id}")
                    var = hir.Var(expr.id, None, span)
                    self.vars[expr.id] = var
                return var
            elif isinstance(expr, ast.Attribute):
                obj = self.parse_ref(expr.value)
                return hir.Member(obj, expr.attr, span)
            else:
                return self.parse_expr(expr)
            # report_error(expr, f"unsupported reference {expr}")
        resolved, remaining = access_chain.resolve()
        if remaining is None or remaining.chain == []:
            if callable(resolved):
                dsl_func = get_dsl_func(resolved)
                if dsl_func is None:
                    report_error(expr, f"expected DSL function")
                return hir.ValueRef(hir.Constant(dsl_func, span))
            elif isinstance(resolved, hir.Type):
                init = resolved.member("__init__")
                if not init:
                    report_error(expr, f"expected type constructor")
                if not isinstance(init, hir.FunctionType):
                    report_error(expr, f"expected callable type constructor")
                return hir.ValueRef(hir.Constant(init.func_like, span))
            else:
                report_error(
                    expr, f"expected callable or type constructor but got {resolved}")
        # print(resolved, remaining)
        parent = resolved
        for i in range(len(remaining.chain)):
            access = remaining.chain[i]
            kind, keys = access
            if kind == AccessKind.ATTRIBUTE:
                assert len(keys) == 1, f"expected single key"
                assert isinstance(keys[0], str), f"expected string key"
                parent = hir.Member(parent, keys[0], span)
            elif kind == AccessKind.SUBSCRIPT:
                raise NotImplementedError("TODO: resolve subscript")
            else:
                report_error(expr, f"unsupported access kind {kind}")
        return parent

    def parse_stmt(self, stmt: ast.stmt) -> Optional[hir.Stmt]:
        if isinstance(stmt, ast.AnnAssign):
            type_annotation = stmt.annotation
            ty = self.p_ctx.parse_type(type_annotation)
            if ty is None:
                report_error(type_annotation, f"failed to parse type")
            if not isinstance(stmt.target, ast.Name):
                report_error(stmt, f"expected name")
            var = self.parse_ref(stmt.target, maybe_new_var=True)
            assert isinstance(var, hir.Ref)
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
            assert isinstance(var, hir.Ref)
            return hir.Assign(var, None, value)
        if isinstance(stmt, ast.Return):
            if stmt.value is None:
                if not isinstance(self.return_type, hir.UnitType):
                    report_error(stmt, f"expected return value")
                return hir.Return(None)
            value = self.parse_expr(stmt.value)
            return hir.Return(value)
        if isinstance(stmt, ast.If):
            if_test = self.parse_expr(stmt.test)
            if_body: List[hir.Stmt] = []
            for s in stmt.body:
                parsed_stmt = self.parse_stmt(s)
                if parsed_stmt is not None:
                    if_body.append(parsed_stmt)
            if_else: List[hir.Stmt] = []
            for s in stmt.orelse:
                parsed_stmt = self.parse_stmt(s)
                if parsed_stmt is not None:
                    if_else.append(parsed_stmt)
            return hir.If(if_test, if_body, if_else)
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
        # a sorted list of vars
        vars = [self.vars[v] for v in sorted(self.vars.keys())]
        return Function(
            self.name,
            params,
            self.return_type,
            [x for x in parsed_body if x is not None],
            vars,
        )
