import ast
from dataclasses import dataclass
import os
import sys
from typing import Generic, List, Optional, Tuple, Dict, Final, TypeVar, Union
from abc import ABC, abstractmethod

PATH_PREFIX = "luisa_lang"


class Path:
    """A path such as `a.b.c`."""

    parts: List[str]

    def __init__(self, parts: List[str] | str) -> None:
        if isinstance(parts, str):
            parts = parts.split(".")
        self.parts = parts

    def __str__(self) -> str:
        return ".".join(self.parts)

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Path) and value.parts == self.parts

    def __hash__(self) -> int:
        return hash(tuple(self.parts))


class Type(ABC):
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def align(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass


class UnitType(Type):
    def size(self) -> int:
        return 0

    def align(self) -> int:
        return 1

    def __eq__(self, value: object) -> bool:
        return isinstance(value, UnitType)


class ScalarType(Type):
    pass


class BoolType(ScalarType):
    def size(self) -> int:
        return 1

    def align(self) -> int:
        return 1

    def __eq__(self, value: object) -> bool:
        return isinstance(value, BoolType)


class IntType(ScalarType):
    bits: int
    signed: bool

    def __init__(self, bits: int, signed: bool) -> None:
        self.bits = bits
        self.signed = signed

    def size(self) -> int:
        return self.bits // 8

    def align(self) -> int:
        return self.size()

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, IntType)
            and value.bits == self.bits
            and value.signed == self.signed
        )


class FloatType(ScalarType):
    bits: int

    def __init__(self, bits: int) -> None:
        self.bits = bits

    def size(self) -> int:
        return self.bits // 8

    def align(self) -> int:
        return self.size()

    def __eq__(self, value: object) -> bool:
        return isinstance(value, FloatType) and value.bits == self.bits


# INT8: Final[IntType] = IntType(8, True)
# INT16: Final[IntType] = IntType(16, True)
# INT32: Final[IntType] = IntType(32, True)
# INT64: Final[IntType] = IntType(64, True)

# UINT8: Final[IntType] = IntType(8, False)
# UINT16: Final[IntType] = IntType(16, False)
# UINT32: Final[IntType] = IntType(32, False)
# UINT64: Final[IntType] = IntType(64, False)

# FLOAT16: Final[FloatType] = FloatType(16)
# FLOAT32: Final[FloatType] = FloatType(32)
# FLOAT64: Final[FloatType] = FloatType(64)


class VectorType(Type):
    element: ScalarType
    count: int

    def __init__(self, element: ScalarType, count: int) -> None:
        self.element = element
        self.count = count

    def _special_size_align(self) -> Optional[Tuple[int, int]]:
        if self.count != 3:
            return None
        if self.element.size() == 4:
            return (16, 16)
        return None

    def size(self) -> int:
        special = self._special_size_align()
        if special is not None:
            return special[0]
        return self.element.size() * self.count

    def align(self) -> int:
        special = self._special_size_align()
        if special is not None:
            return special[1]
        return self.element.align()

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, VectorType)
            and value.element == self.element
            and value.count == self.count
        )


class ArrayType(Type):
    element: Type
    count: int

    def __init__(self, element: Type, count: int) -> None:
        self.element = element
        self.count = count

    def size(self) -> int:
        return self.element.size() * self.count

    def align(self) -> int:
        return self.element.align()

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, ArrayType)
            and value.element == self.element
            and value.count == self.count
        )


class StructType(Type):
    fields: List[Tuple[str, Type]]

    def __init__(self, fields: List[Tuple[str, Type]]) -> None:
        self.fields = fields

    def size(self) -> int:
        return sum(field.size() for _, field in self.fields)

    def align(self) -> int:
        return max(field.align() for _, field in self.fields)

    def __eq__(self, value: object) -> bool:
        return value is self or (
            isinstance(value, StructType) and value.fields == self.fields
        )


class SymbolicType(Type):
    """A type that is not yet resolved."""

    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def size(self) -> int:
        raise RuntimeError("SymbolicType has no size")

    def align(self) -> int:
        raise RuntimeError("SymbolicType has no align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, SymbolicType) and value.name == self.name


class TypeParameter:
    symbol: SymbolicType
    bound: Optional[List[Type]]

    def __init__(self, symbol: SymbolicType, bound: Optional[List[Type]]) -> None:
        self.symbol = symbol
        self.bound = bound


class OpaqueType(Type):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def size(self) -> int:
        raise RuntimeError("OpaqueType has no size")

    def align(self) -> int:
        raise RuntimeError("OpaqueType has no align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, OpaqueType) and value.name == self.name


class ParametricType(Type):
    """A parametric type that is not yet resolved."""

    name: Path
    params: List[TypeParameter]
    body: Type

    def __init__(self, name: Path, params: List[TypeParameter], body: Type) -> None:
        self.name = name
        self.params = params
        self.body = body

    def size(self) -> int:
        raise RuntimeError("ParametricType has no size")

    def align(self) -> int:
        raise RuntimeError("ParametricType has no align")

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, ParametricType)
            and value.name == self.name
            and value.params == self.params
        )


class BoundType(Type):
    generic: ParametricType
    args: List[Type]

    def __init__(self, generic: ParametricType, args: List[Type]) -> None:
        self.generic = generic
        self.args = args

    def size(self) -> int:
        raise RuntimeError("don't call size on BoundedType")

    def align(self) -> int:
        raise RuntimeError("don't call align on BoundedType")

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, BoundType)
            and value.generic == self.generic
            and value.args == self.args
        )


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
        return Span(
            file=None,
            start=(ast.lineno, ast.col_offset),
            end=(ast.end_lineno, ast.end_col_offset),
        )


class Node:
    type: Optional[Type]
    span: Optional[Span]

    def __init__(
        self, type: Optional[Type] = None, span: Optional[Span] = None
    ) -> None:
        self.type = type
        self.span = span


class Ref(Node):
    pass


class Value(Node):
    pass


class ValueRef(Ref):
    value: Value

    def __init__(self, value: Value) -> None:
        super().__init__(value.type, value.span)
        self.value = value


class Var(Ref):
    name: str

    def __init__(self, name: str, type: Optional[Type], span: Optional[Span]) -> None:
        super().__init__(type, span)
        self.name = name
        self.type = type

    def __hash__(self) -> int:
        return self.name.__hash__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Var) and other.name == self.name


class Member(Ref):
    base: Ref
    field: str

    def __init__(self, base: Ref, field: str, span: Optional[Span]) -> None:
        super().__init__(None, span)
        self.base = base
        self.field = field


class Index(Ref):
    base: Ref
    index: Value

    def __init__(self, base: Ref, index: Value, span: Optional[Span]) -> None:
        super().__init__(None, span)
        self.base = base
        self.index = index


class Load(Value):
    ref: Ref

    def __init__(self, ref: Ref) -> None:
        super().__init__(ref.type, ref.span)
        self.ref = ref


class UnresolvedCall(Value):
    op: str
    args: List[Value]
    is_method: bool

    def __init__(
        self, op: str, args: List[Value], is_method=False, span: Optional[Span] = None
    ) -> None:
        super().__init__(None, span)
        self.op = op
        self.args = args
        self.is_method = is_method


class Call(Value):
    op: Value
    args: List[Value]

    def __init__(self, op: Value, args: List[Value], span: Optional[Span]) -> None:
        super().__init__(op.type, span)
        self.op = op
        self.args = args


class TypeRule(ABC):
    @abstractmethod
    def infer(self, ctx: "Context", args: List[Type]) -> Type:
        pass


class BuiltinFunction:
    name: str
    type_rule: TypeRule

    def __init__(self, name: str, type_rule: TypeRule) -> None:
        self.name = name
        self.type_rule = type_rule


class Stmt:
    pass


class VarDecl(Stmt):
    var: Var
    expected_type: Type

    def __init__(self, var: Var, expected_type: Type) -> None:
        self.var = var
        self.expected_type = expected_type


class Assign(Stmt):
    ref: Ref
    value: Value
    expected_type: Optional[Type]

    def __init__(self, ref: Ref, expected_type: Optional[Type], value: Value) -> None:
        self.ref = ref
        self.value = value
        self.expected_type = expected_type


class Function:
    name: str
    params: List[Var]
    return_type: Type
    body: List[Stmt]
    builtin: bool

    def __init__(
        self,
        name: str,
        params: List[Var],
        return_type: Type,
        body: List[Stmt],
        builtin: bool = False,
    ) -> None:
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.builtin = builtin


class Module:
    functions: Dict[str, Function]

    def __init__(self) -> None:
        self.functions = {}


class Package:
    is_std: bool
    root: Module
    path: str

    def __init__(self, path: str, is_std: bool, root: Module) -> None:
        self.path = path
        self.is_std = is_std
        self.root = root


K = TypeVar("K")
V = TypeVar("V")


class Env(Generic[K, V]):
    _map: Dict[K, V]
    _parent: Optional["Env[K, V]"]

    def __init__(self) -> None:
        self._map = {}
        self._parent = None

    def fork(self) -> "Env[K, V]":
        env = Env[K, V]()
        env._parent = self
        return env

    def lookup(self, key: K) -> Optional[V]:
        res = self._map.get(key)
        if res is not None:
            return res
        if self._parent is not None:
            return self._parent.lookup(key)
        return None

    def bind(self, key: K, value: V) -> None:
        self._map[key] = value


Item = Union[Type, Function, BuiltinFunction]
ItemEnv = Env[Path, Item]


class Context:
    cur_path: str
    packages: Dict[str, Package]

    modules: Dict[str, Module]
    """Holds absolute path -> module."""

    items: ItemEnv
    """Item environment, which holds global name bindings."""

    resolution: Env[Path, Path]
    """Resolution environment, which holds alias -> alias | path bindings."""

    def __init__(self, cur_path: str, is_root: bool) -> None:
        self.cur_path = cur_path
        self.items = Env()
        self.resolution = Env()
        self.packages = {}
        self.modules = {}
        if is_root:
            self._init_builtins()

    def import_module_or_package(self, name: str) -> Optional[Module | Package]:
        def resolve_module(filename: str) -> Optional[str]:
            search_paths = [self.cur_path] + sys.path
            for path in search_paths:
                # first check if name.py exists
                full_path = os.path.join(path, filename + ".py")
                if os.path.exists(full_path):
                    return full_path
                # then check if name/__init__.py exists
                full_path = os.path.join(path, filename, "__init__.py")
                if os.path.exists(full_path):
                    return full_path
            return None

        result = resolve_module(name)
        if not result:
            return None
        result = os.path.abspath(result)
        if result.endswith("__init__.py"):
            # handling a multi-file module/package
            pass
        else:
            pass
        raise NotImplementedError("TODO")

    def resolve_name(self, name: str | Path) -> Path:
        """Resolve a name or path if it is imported/alias"""
        path = Path(name.split(".")) if isinstance(name, str) else name
        for _ in range(64):
            resolved = self.resolution.lookup(path)
            if resolved:
                path = resolved
            return path
        raise RuntimeError(f"failed to resolve name {name}: maybe circular alias?")

    # def fork(self) -> "Context":
    #     ctx = Context(self.cur_path, False)
    #     ctx.items = self.items.fork()
    #     ctx.resolution = self.resolution.fork()
    #     return ctx

    def _init_builtins(self) -> None:
        int_bits_to_name = {
            8: "byte",
            16: "short",
            32: "int",
            64: "long",
        }
        float_bits_to_name = {
            16: "half",
            32: "float",
            64: "double",
        }
        # int types
        for bits in [8, 16, 32, 64]:
            iname, itype = (
                f"{PATH_PREFIX}.{int_bits_to_name[bits]}",
                IntType(bits, True),
            )
            uname, utype = (
                f"{PATH_PREFIX}.u{int_bits_to_name[bits]}",
                IntType(bits, False),
            )
            self.items.bind(Path(iname), itype)
            self.items.bind(Path(uname), utype)
            for count in [2, 3, 4]:
                vname = f"{iname}{count}"
                self.items.bind(Path(vname), VectorType(itype, count))
                vname = f"{uname}{count}"
                self.items.bind(Path(vname), VectorType(utype, count))
        # float types
        for bits in [16, 32, 64]:
            fname, ftype = (
                f"{PATH_PREFIX}.{float_bits_to_name[bits]}",
                FloatType(bits),
            )
            self.items.bind(Path(fname), ftype)
            for count in [2, 3, 4]:
                vname = f"{fname}{count}"
                self.items.bind(Path(vname), VectorType(ftype, count))
        # bool type
        self.items.bind(Path(f"{PATH_PREFIX}.bool"), BoolType())
        for count in [2, 3, 4]:
            vname = f"{PATH_PREFIX}.bool{count}"
            self.items.bind(Path(vname), VectorType(BoolType(), count))

        # unit type
        self.items.bind(Path("None"), UnitType())

        # buffer type
        buffer_ty = ParametricType(
            Path(f"{PATH_PREFIX}.Buffer"),
            [TypeParameter(SymbolicType("T"), [])],
            OpaqueType("Buffer"),
        )
        self.items.bind(Path(f"{PATH_PREFIX}.Buffer"), buffer_ty)
        bulitins_file = os.path.join(os.path.dirname(__file__), "builtins.py")
        with open(bulitins_file) as f:
            code = f.read()
            tree = ast.parse(code)
            print(ast.dump(tree))
