import ast
from dataclasses import dataclass
from enum import Enum, auto
import os
import sys
from typing import (
    Any,
    Callable,
    Generic,
    List,
    Optional,
    Tuple,
    Dict,
    Final,
    TypeVar,
    Union,
)
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
    methods: Dict[str, "Function"]
    is_builtin: bool

    def __init__(self):
        self.methods = {}
        self.is_builtin = False

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def align(self) -> int:
        pass

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


class UnitType(Type):
    def size(self) -> int:
        return 0

    def align(self) -> int:
        return 1

    def __eq__(self, value: object) -> bool:
        return isinstance(value, UnitType)

    def __hash__(self) -> int:
        return hash(UnitType)


class ScalarType(Type):
    pass


class BoolType(ScalarType):
    def size(self) -> int:
        return 1

    def align(self) -> int:
        return 1

    def __eq__(self, value: object) -> bool:
        return isinstance(value, BoolType)

    def __hash__(self) -> int:
        return hash(BoolType)


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

    def __hash__(self) -> int:
        return hash((IntType, self.bits, self.signed))

    def __repr__(self) -> str:
        return f"IntType({self.bits}, {self.signed})"


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

    def __repr__(self) -> str:
        return f"FloatType({self.bits})"

    def __hash__(self) -> int:
        return hash((FloatType, self.bits))


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

    def __repr__(self) -> str:
        return f"VectorType({self.element}, {self.count})"

    def __hash__(self) -> int:
        return hash((VectorType, self.element, self.count))


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

    def __repr__(self) -> str:
        return f"ArrayType({self.element}, {self.count})"


class PointerType(Type):
    element: Type

    def __init__(self, element: Type) -> None:
        self.element = element

    def size(self) -> int:
        return 8

    def align(self) -> int:
        return 8

    def __eq__(self, value: object) -> bool:
        return isinstance(value, PointerType) and value.element == self.element

    def __repr__(self) -> str:
        return f"PointerType({self.element})"


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
        file = None
        if hasattr(ast, "source_file"):
            file = getattr(ast, "source_file")
        return Span(
            file=file,
            start=(getattr(ast, "lineno", 0), getattr(ast, "col_offset", 0)),
            end=(getattr(ast, "end_lineno", 0), getattr(ast, "end_col_offset", 0)),
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
    byval: bool

    def __init__(
        self, name: str, type: Optional[Type], span: Optional[Span], byval=True
    ) -> None:
        super().__init__(type, span)
        self.name = name
        self.type = type
        self.byval = byval

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

class CallOpKind(Enum):
    FUNC = auto()
    BINARY_OP = auto()
    UNARY_OP = auto()
    

class UnresolvedCall(Value):
    op: str
    args: List[Value]
    kind: CallOpKind

    def __init__(
        self, op: str, args: List[Value], kind: CallOpKind, span: Optional[Span] = None
    ) -> None:
        super().__init__(None, span)
        self.op = op
        self.args = args
        self.kind = kind


class Call(Value):
    op: Value
    args: List[Value]
    kind: CallOpKind

    def __init__(self, op: Value, args: List[Value],kind: CallOpKind, span: Optional[Span]) -> None:
        super().__init__(op.type, span)
        self.op = op
        self.args = args
        self.kind = kind


class TypeRule(ABC):
    @abstractmethod
    def infer(self, ctx: "GlobalContext", args: List[Type]) -> Type:
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


class Return(Stmt):
    value: Optional[Value]

    def __init__(self, value: Optional[Value]) -> None:
        self.value = value


class Function:
    name: str
    params: List[Var]
    return_type: Type
    body: List[Stmt]
    builtin: bool
    export: bool

    def __init__(
        self,
        name: str,
        params: List[Var],
        return_type: Type,
        body: List[Stmt],
        builtin: bool = False,
        export: bool = False,
    ) -> None:
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.builtin = builtin
        self.export = export

    @property
    def is_parametric(self) -> bool:
        for p in self.params:
            if p.type is None:
                return True
            if isinstance(p.type, ParametricType):
                return True
        if isinstance(self.return_type, ParametricType):
            return True
        return False


# K = TypeVar("K")
# V = TypeVar("V")


# class Env(Generic[K, V]):
#     _map: Dict[K, V]
#     _parent: Optional["Env[K, V]"]

#     def __init__(self) -> None:
#         self._map = {}
#         self._parent = None

#     def fork(self) -> "Env[K, V]":
#         env = Env[K, V]()
#         env._parent = self
#         return env

#     def lookup(self, key: K) -> Optional[V]:
#         res = self._map.get(key)
#         if res is not None:
#             return res
#         if self._parent is not None:
#             return self._parent.lookup(key)
#         return None

#     def bind(self, key: K, value: V) -> None:
#         self._map[key] = value


# Item = Union[Type, Function, BuiltinFunction]
# ItemEnv = Env[Path, Item]

_global_context: Optional["GlobalContext"] = None


class GlobalContext:
    types: Dict[type, Type]
    functions: Dict[Callable[..., Any], Function]

    @staticmethod
    def get() -> "GlobalContext":
        global _global_context
        if _global_context is None:
            _global_context = GlobalContext()
        return _global_context

    def __init__(self) -> None:
        assert _global_context is None, "GlobalContext should be a singleton"
        self.types = {type(None): UnitType()}
        self.functions = {}


class FuncMetadata:
    pass


class StructMetadata:
    pass
