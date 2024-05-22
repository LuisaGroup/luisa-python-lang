import ast
from typing import overload
import luisa_lang
import luisa_lang.hir as hir
from luisa_lang.hir import Type, BoundType, ParametricType
from typing import NoReturn


def _report_error_span(span: hir.Span, message: str) -> NoReturn:
    raise RuntimeError(f"error at {span.start}: {message}")


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


def parse_type(type: ast.AST, type_env: hir.TypeEnv) -> Type:
    if isinstance(type, ast.Name):
        ty = type_env.lookup(type.id)
        if ty is None:
            report_error(type, f"unknown type {type.id}")
        return ty
    elif isinstance(type, ast.Subscript):
        parameteric_type = parse_type(type.value, type_env)
        if not isinstance(parameteric_type, ParametricType):
            report_error(type, f"expected parameteric type")
        slice = type.slice
        args = []
        if isinstance(slice, ast.Name):
            args = [parse_type(slice, type_env)]
        elif isinstance(slice, ast.Tuple):
            args = [parse_type(arg, type_env) for arg in slice.elts]
        else:
            report_error(type, f"unparsable type arguments")
        if len(args) != len(parameteric_type.params):
            report_error(type, f"expected {len(parameteric_type.params)} arguments")
        return BoundType(parameteric_type, args)
    else:
        report_error(type, f"unparsable type")


def parse_function(func: ast.FunctionDef, ctx: hir.Context):
    pass


# attempt to parse the AST and update the context
def parse(tree: ast.AST, ctx: hir.Context):
    print(ast.dump(tree))
    assert isinstance(tree, ast.Module)
    for stmt in tree.body:
        if isinstance(stmt, ast.FunctionDef):
            parse_function(stmt, ctx)
        else:
            raise NotImplementedError(f"unsupported statement {stmt}")
