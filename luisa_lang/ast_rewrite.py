import ast
from ast import NodeTransformer
from typing import Callable, Any, List, Set, cast
from utils import retrieve_ast_and_filename, NestedHashMap


class FuncRewriter(NodeTransformer):
    def __init__(self):
        pass

    # def handle_assign(self, targets: List[ast.expr], value: ast.expr) -> List[ast.stmt]:
    #     pass

    def runtime_intrinsic(self, name: str) -> ast.Attribute:
        return ast.Attribute(value=ast.Attribute(
            value=ast.Name(id='luisa_lang', ctx=ast.Load()),
            attr='lang_runtime',
            ctx=ast.Load()
        ), attr='name', ctx=ast.Load())

    def visit_Name(self, node: ast.Name) -> Any:
        call = ast.Call(
            func=self.runtime_intrinsic('redirect_name_lookup'),
            args=[node],
            keywords=[]
        )
        return ast.copy_location(call, node)

    def visit_Assign(self, node: ast.Assign) -> Any:
        """
        dst = src => dst = luisa_lang.lang_runtime.redirect_assign(dst, src)
        """
        self.generic_visit(node)
        assert len(node.targets) == 1
        call = ast.Call(
            func=self.runtime_intrinsic('redirect_assign'),
            args=[node.targets[0], node.value],
            keywords=[]
        )
        return ast.copy_location(call, node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        """
        dst: ty = src => dst = luisa_lang.lang_runtime.redirect_assign(dst, src, ty)
        """
        self.generic_visit(node)
        call = ast.Call(
            func=self.runtime_intrinsic('redirect_assign'),
            args=[node.target, node.value],
            keywords=[]
        )
        return ast.copy_location(call, node)
        


def rewrite_function[F: Callable[..., Any]](f: F) -> F:
    tree, _filename = retrieve_ast_and_filename(f)
    tree = FuncRewriter().visit(tree)
    ast.fix_missing_locations(tree)

    code = compile(tree, filename="<ast>", mode="exec")
    local_dict = {}
    exec(code, f.__globals__, local_dict)
    rewrote_f = local_dict[f.__name__]

    def wrapper(*args, **kwargs):
        return rewrote_f(*args, **kwargs)

    return cast(F, wrapper)
