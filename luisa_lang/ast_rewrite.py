import ast
from ast import NodeTransformer
import copy
from typing import Callable, Any, List, Set, cast
from utils import checked_cast, retrieve_ast_and_filename, NestedHashMap

"""
Rewrite rules:
a function `f(args...)` is rewritten to `f(__lc_ctx__, args...)`
each name lookup `name` is rewritten to `__lc_ctx__[`name`]`

`a: expr = b` is rewritten to `__lc_ctx__.anno_ty(a, expr); __lc_ctx__[a] = b`

`x op y` is rewritten to `__lc_ctx__.redirect_binary(op, x, y)`
`x op= y` is rewritten to `x = __lc_ctx__.redirect_unary(op, x, y)`
`x[y]` is rewritten to `__lc_ctx__.redirect_subscript(x)[y]`
`x.y` is rewritten to `__lc_ctx__.redirect_attr(x).y`

Control flow:
if cond:
    true_body1
else:
    false_body

is rewritten to:

with __lc_ctx__.if_(cond) as if_stmt:
    if_stmt.true_active():
        true_body
    if_stmt.false_active():
        false_body

for i in range(expr):
    body

is rewritten to:

with __lc_ctx__.for_range(expr) as for_stmt:
    for i in for_stmt.range():
        body

Terminators are rewritten in a slightly different way.
We check if the parent control flow is static or dynamic.
`return expr` is rewritten to 
if __lc_ctx__.is_parent_static():
    return expr
else:
    __lc_ctx__.return_(expr)

`break` is rewritten to
if __lc_ctx__.is_parent_static():
    break
else:
    __lc_ctx__.break_()

`continue` is rewritten to
if __lc_ctx__.is_parent_static():
    continue
else:
    __lc_ctx__.continue_()

"""


class FuncRewriter(NodeTransformer):
    def __init__(self, decorator_name: str):
        self.decorator_name = decorator_name
        self.id_cnt = 0

    def new_id(self) -> str:
        self.id_cnt += 1
        return f'__lc_id{self.id_cnt}'

    # def handle_assign(self, targets: List[ast.expr], value: ast.expr) -> List[ast.stmt]:
    #     pass

    def visit_list_stmt(self, stmts: List[ast.stmt]) -> List[ast.stmt]:
        res = []
        for stmt in stmts:
            transformed = self.visit(stmt)
            if isinstance(transformed, list):
                res.extend(transformed)
            else:
                res.append(transformed)
        for stmt in res:
            assert isinstance(stmt, ast.stmt), f"stmt is not ast.stmt: {stmt}"
        return cast(List[ast.stmt], res)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        # Filter out decorators matching our decorator_name
        # Remove the decorator we're interested in
        node.decorator_list = [
            d for d in node.decorator_list
            if not (isinstance(d, ast.Name) and d.id == self.decorator_name) and
            not (isinstance(d, ast.Attribute) and d.attr == self.decorator_name)
        ]

        # Add __lc_ctx__ to the function arguments
        node.args.args.insert(0, ast.arg(arg='__lc_ctx__', annotation=None))

        body = self.visit_list_stmt(node.body)
        node.body = body

        return node

    def visit_Name(self, node: ast.Name) -> Any:
        # rewrite to __lc_ctx__.name
        return ast.Subscript(value=ast.Name(id='__lc_ctx__', ctx=ast.Load()), slice=ast.Constant(value=node.id), ctx=node.ctx)

    def visit_Assign(self, node: ast.Assign) -> Any:
        return self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        target = checked_cast(ast.expr, self.visit(node.target))
        assert isinstance(target, (ast.Name, ast.Subscript, ast.Attribute))
        target.ctx = ast.Load()
        anno = ast.Expr(value=ast.Call(
            func=ast.Attribute(value=ast.Name(
                id='__lc_ctx__', ctx=ast.Load()), attr='anno_ty', ctx=ast.Load()),
            args=[target],
            keywords=[]
        ))
        if node.value is None:
            return anno
        target = copy.deepcopy(target)
        target.ctx = ast.Store()
        assign = ast.Assign(targets=[target], value=self.visit(
            node.value))
        return [anno, assign]

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        return ast.Call(
            func=ast.Attribute(value=ast.Name(
                id='__lc_ctx__', ctx=ast.Load()), attr='redirect_binary', ctx=ast.Load()),
            args=[ast.Constant(value=type(node.op).__name__), lhs, rhs],
            keywords=[]
        )

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        operand = self.visit(node.operand)
        return ast.Call(
            func=ast.Attribute(value=ast.Name(
                id='__lc_ctx__', ctx=ast.Load()), attr='redirect_unary', ctx=ast.Load()),
            args=[ast.Constant(value=type(node.op).__name__), operand],
            keywords=[]
        )

    def visit_Subscript(self, node: ast.Subscript) -> Any:
        value = self.visit(node.value)
        return ast.Subscript(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='redirect_subscript', ctx=ast.Load()),
                args=[value],
                keywords=[]
            ),
            slice=node.slice,
            ctx=node.ctx
        )

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        value = self.visit(node.value)
        return ast.Attribute(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='redirect_attr', ctx=ast.Load()),
                args=[value],
                keywords=[]
            ),
            attr=node.attr,
            ctx=node.ctx
        )

    def visit_If(self, node: ast.If) -> Any:
        if_id = self.new_id() + '_if'
        with_item = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='if_', ctx=ast.Load()),
                args=[node.test],
                keywords=[]
            ),
            optional_vars=ast.Name(id=if_id, ctx=ast.Store())
        )
        true_branch = ast.If(
            test=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id=if_id, ctx=ast.Load()), attr='true_active', ctx=ast.Load()),
                args=[],
                keywords=[]
            ),
            body=self.visit_list_stmt(node.body),
            orelse=[]
        )
        false_branch = ast.If(
            test=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id=if_id, ctx=ast.Load()), attr='false_active', ctx=ast.Load()),
                args=[],
                keywords=[]
            ),
            body=self.visit_list_stmt(node.orelse),
            orelse=[]
        )
        for stmt in node.orelse:
            false_branch.body.append(checked_cast(ast.stmt, self.visit(stmt)))
        with_stmt = ast.With(
            items=[with_item],
            body=[true_branch, false_branch]
        )
        return with_stmt

    def visit_Return(self, node: ast.Return) -> Any:
        ret_value: ast.expr | None = None
        if node.value is not None:
            tmp = self.visit(node.value)
            assert isinstance(tmp, ast.expr)
            ret_value = tmp
        return ast.If(
            test=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='is_parent_static', ctx=ast.Load()),
                args=[],
                keywords=[]
            ),
            body=cast(List[ast.stmt], [ast.Return(value=ret_value)]),
            orelse=cast(List[ast.stmt], [ast.Expr(value=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='return_', ctx=ast.Load()),
                args=[ret_value] if ret_value is not None else [],
                keywords=[]
            ))])
        )

    def visit_Break(self, node: ast.Break) -> Any:
        return ast.If(
            test=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='is_parent_static', ctx=ast.Load()),
                args=[],
                keywords=[]
            ),
            body=cast(List[ast.stmt], [ast.Break()]),
            orelse=cast(List[ast.stmt], [ast.Expr(value=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='break_', ctx=ast.Load()),
                args=[],
                keywords=[]
            ))])
        )

    def visit_Continue(self, node: ast.Continue) -> Any:
        return ast.If(
            test=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='is_parent_static', ctx=ast.Load()),
                args=[],
                keywords=[]
            ),
            body=cast(List[ast.stmt], [ast.Continue()]),
            orelse=cast(List[ast.stmt], [ast.Expr(value=ast.Call(
                func=ast.Attribute(value=ast.Name(
                    id='__lc_ctx__', ctx=ast.Load()), attr='continue_', ctx=ast.Load()),
                args=[],
                keywords=[]
            ))])
        )


def rewrite_function[F: Callable[..., Any]](f: F, decorator_name: str) -> F:
    tree, _filename = retrieve_ast_and_filename(f)
    tree = FuncRewriter(decorator_name).visit(tree)
    ast.fix_missing_locations(tree)
    # print(ast.unparse(tree))
    code = compile(tree, filename="<ast>", mode="exec")
    local_dict = {}
    exec(code, f.__globals__, local_dict)
    rewrote_f = local_dict[f.__name__]

    return cast(F, rewrote_f)
