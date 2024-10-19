import ast
import textwrap
import types
from typing import Any, List, NoReturn, Optional, Tuple, TypeVar, overload
import sourceinspect
from hashlib import sha256

T = TypeVar("T")


def unwrap(opt: Optional[T]) -> T:
    if opt is None:
        raise ValueError("unwrap None")
    return opt


def increment_lineno_and_col_offset(
    node: ast.AST, lineno: int, col_offset: int
) -> ast.AST:
    """
    Increment the line number and end line number of each node in the tree
    starting at *node* by *n*. This is useful to "move code" to a different
    location in a file.
    """
    for child in ast.walk(node):
        if "lineno" in child._attributes:
            setattr(child, "lineno", getattr(child, "lineno", 0) + lineno)
        if (
            "end_lineno" in child._attributes
            and (end_lineno := getattr(child, "end_lineno", 0)) is not None
        ):
            setattr(child, "end_lineno", end_lineno + lineno)
        if "col_offset" in child._attributes:
            setattr(child, "col_offset", getattr(
                child, "col_offset", 0) + col_offset)
        if (
            "end_col_offset" in child._attributes
            and (end_col_offset := getattr(child, "end_col_offset", 0)) is not None
        ):
            setattr(child, "end_col_offset", end_col_offset + col_offset)
    return node


def dedent_and_retrieve_indentation(lines: str) -> Tuple[str, int]:
    """
    Dedent the lines and return the indentation level of the first line.
    """
    if not lines:
        return "", 0
    return textwrap.dedent("".join(lines)), len(lines[0]) - len(lines[0].lstrip())


def retrieve_ast_and_filename(f: object) -> Tuple[ast.AST, str]:
    source_file = sourceinspect.getsourcefile(f)
    if source_file is None:
        source_file = "<unknown>"
    source_lines, lineno = sourceinspect.getsourcelines(f)
    src, indent = dedent_and_retrieve_indentation(source_lines)
    tree = increment_lineno_and_col_offset(
        ast.parse(src), lineno - 1, indent + 1)
    for child in ast.walk(tree):
        setattr(child, "source_file", source_file)
    return tree, source_file


def get_full_name(obj: Any) -> str:
    module = ""
    if hasattr(obj, "__module__"):
        module = obj.__module__
    return f"{module}.{obj.__qualname__}"


class Span:
    file: Optional[str]
    start: Tuple[int, int]
    end: Tuple[int, int]

    def __init__(
        self, file: Optional[str], start: Tuple[int, int], end: Tuple[int, int]
    ) -> None:
        self.file = file
        self.start = start
        self.end = end

    def __str__(self) -> str:
        if self.file is None:
            return f"{self.start[0]}:{self.start[1]}-{self.end[0]}:{self.end[1]}"
        return (
            f"{self.file}:{self.start[0]}:{self.start[1]}-{self.end[0]}:{self.end[1]}"
        )

    @staticmethod
    def from_ast(ast: ast.AST) -> Optional["Span"]:
        if not hasattr(ast, "lineno"):
            return None
        if not hasattr(ast, "col_offset"):
            return None
        if not hasattr(ast, "end_lineno") or ast.end_lineno is None:
            return None
        if not hasattr(ast, "end_col_offset") or ast.end_col_offset is None:
            return None
        file = None
        if hasattr(ast, "source_file"):
            file = getattr(ast, "source_file")
        return Span(
            file=file,
            start=(getattr(ast, "lineno", 0), getattr(ast, "col_offset", 0)),
            end=(getattr(ast, "end_lineno", 0),
                 getattr(ast, "end_col_offset", 0)),
        )


def _report_error_span(span: Span, message: str) -> NoReturn:
    raise RuntimeError(f"error at {span}: {message}")


def _report_error_tree(tree: ast.AST, message: str) -> NoReturn:
    span = Span.from_ast(tree)
    if span is not None:
        _report_error_span(span, message)
    else:
        raise RuntimeError(f"error: {message}")


@overload
def report_error(obj: Span | None, message: str) -> NoReturn: ...
@overload
def report_error(obj: ast.AST, message: str) -> NoReturn: ...


def report_error(obj, message: str) -> NoReturn:
    if obj is None:
        raise RuntimeError(f"error: {message}")
    if isinstance(obj, Span):
        _report_error_span(obj, message)
    elif isinstance(obj, ast.AST):
        _report_error_tree(obj, message)
    else:
        raise NotImplementedError(f"unsupported object {obj}")


def get_union_args(union: Any) -> List[type]:
    if hasattr(union, "__args__") or isinstance(union, types.UnionType):
        return list(union.__args__)
    return []

def checked_cast(t: type[T], obj: Any) -> T:
    if not isinstance(obj, t):
        raise TypeError(f"expected {t}, got {type(obj)}")
    return obj

def unique_hash(s: str) -> str:
    return sha256(s.encode()).hexdigest().upper()[:8]