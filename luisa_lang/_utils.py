import ast
import textwrap
from typing import Optional, Tuple, TypeVar
import sourceinspect

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
            setattr(child, "col_offset", getattr(child, "col_offset", 0) + col_offset)
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
    tree = increment_lineno_and_col_offset(ast.parse(src), lineno - 1, indent + 1)
    for child in ast.walk(tree):
        setattr(child, "source_file", source_file)
    return tree, source_file
