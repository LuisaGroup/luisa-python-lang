import ast
import textwrap
import types
from typing import Any, Callable, Dict, List, NoReturn, Optional, Tuple, TypeVar, cast, overload
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


def dedent_and_retrieve_indentation(lines: List[str]) -> Tuple[str, int]:
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
            f"{self.file}:{self.start[0]}:{
                self.start[1]}-{self.end[0]}:{self.end[1]}"
        )

    @staticmethod
    def from_ast(ast: ast.AST) -> Optional["Span"]:
        if not hasattr(ast, "lineno"):
            return None
        if not hasattr(ast, "col_offset"):
            return None
        if not hasattr(ast, "end_lineno") or getattr(ast, "end_lineno") is None:
            return None
        if not hasattr(ast, "end_col_offset") or getattr(ast, "end_col_offset") is None:
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


def print_yellow(message: str) -> None:
    print(f"\033[33m{message}\033[0m")


def print_red(message: str) -> None:
    print(f"\033[31m{message}\033[0m")


def show_warning(message: str, span: Optional[Span] = None) -> None:
    if span is not None:
        print_yellow(f"Warning: {span}: {message}")
    else:
        print_yellow(f"Warning: {message}")


def get_union_args(union: Any) -> List[type]:
    if hasattr(union, "__args__") or isinstance(union, types.UnionType):
        return list(union.__args__)
    return []


def get_typevar_constrains_and_bounds(t: TypeVar) -> Tuple[List[Any], Optional[Any]]:
    """
    Find the constraints and bounds of a TypeVar.
    Only one of the two can be present.
    """
    constraints = []
    bound = None
    if hasattr(t, "__constraints__"):
        constraints = list(t.__constraints__)
    if hasattr(t, "__bound__"):
        bound = t.__bound__
    return constraints, bound


def checked_cast(t: type[T], obj: Any) -> T:
    if not isinstance(obj, t):
        raise TypeError(f"expected {t}, got {type(obj)}")
    return obj


def unique_hash(s: str) -> str:
    return sha256(s.encode()).hexdigest().upper()[:8]


def round_to_align(s: int, a: int) -> int:
    return s + (a - s % a) % a


class NestedHashMap[K, V]:
    parent: Optional["NestedHashMap[K, V]"]
    mapping: Dict[K, V]

    def __init__(self, parent: Optional["NestedHashMap[K, V]"] = None) -> None:
        self.parent = parent
        self.mapping = {}

    def insert(self, key: K, value: V) -> None:
        self.mapping[key] = value

    def get(self, key: K) -> Optional[V]:
        if key in self.mapping:
            return self.mapping[key]
        if self.parent is not None:
            return self.parent.get(key)
        return None

    def contains(self, key: K) -> bool:
        return self.get(key) is not None

    def push(self) -> "NestedHashMap[K, V]":
        return NestedHashMap(parent=self)


class Lazy[T]:
    _instance: Optional[T]
    _factory: Callable[[], T]
    _initialized: bool

    def __init__(self, factory: Callable[[], T]) -> None:
        self._factory = factory
        self._initialized = False
        self._instance = None

    def _init_instance(self):
        if not self._initialized:
            self._instance = self._factory()
            self._initialized = True

    def get(self) -> T:
        self._init_instance()
        return cast(T, self._instance)


def inherit[T](cls: type[T], parent: Any, init_fn: Callable[..., None]) -> type[T]:
    """
    Dynamically inherit from `parent` class and ensure the parent's
    __init__ is called when instantiating the new class.
    """
    original_init = cls.__dict__.get('__init__', None)

    def new_init(self, *args, **kwargs):
        init_fn(self, *args, **kwargs)

        # Call original class (child) initializer
        if original_init:
            original_init(self, *args, **kwargs)

    # Copy attributes and override __init__
    attrs = dict(cls.__dict__)
    attrs['__init__'] = new_init

    # Construct new type with parent + original bases
    return type(cls.__name__, (parent,) + cls.__bases__, attrs)
