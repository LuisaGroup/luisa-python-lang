import ast
from dataclasses import dataclass
from enum import Enum, auto
import os
import sys
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Set,
    Tuple,
    Dict,
    Union,
    cast,
)
from typing_extensions import override
from luisa_lang._utils import Span
from abc import ABC, abstractmethod

PATH_PREFIX = "luisa_lang"

FunctionLike = Union["Function", "BuiltinFunction"]


class Type(ABC):
    methods: Dict[str, FunctionLike]
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

    def member(self, field: Any) -> Optional['Type']:
        if isinstance(field, str):
            m = self.methods.get(field)
            if not m:
                return None
            return FunctionType(m)
        return None


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
        super().__init__()
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


class GenericFloatType(ScalarType):
    @override
    def __eq__(self, value: object) -> bool:
        return isinstance(value, GenericFloatType)

    @override
    def __hash__(self) -> int:
        return hash(GenericFloatType)

    @override
    def size(self) -> int:
        raise RuntimeError("GenericFloatType has no size")

    @override
    def align(self) -> int:
        raise RuntimeError("GenericFloatType has no align")


class GenericIntType(ScalarType):
    @override
    def __eq__(self, value: object) -> bool:
        return isinstance(value, GenericIntType)

    @override
    def __hash__(self) -> int:
        return hash(GenericIntType)

    @override
    def size(self) -> int:
        raise RuntimeError("GenericIntType has no size")

    @override
    def align(self) -> int:
        raise RuntimeError("GenericIntType has no align")


class FloatType(ScalarType):
    bits: int

    def __init__(self, bits: int) -> None:
        super().__init__()
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


class VectorType(Type):
    element: ScalarType
    count: int

    def __init__(self, element: ScalarType, count: int) -> None:
        super().__init__()
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
    count: Union[int, "SymbolicConstant"]

    def __init__(self, element: Type, count: Union[int, "SymbolicConstant"]) -> None:
        super().__init__()
        self.element = element
        self.count = count

    def size(self) -> int:
        if isinstance(self.count, SymbolicConstant):
            raise RuntimeError("ArrayType size is symbolic")
        return self.element.size() * self.count

    def align(self) -> int:
        if isinstance(self.count, SymbolicConstant):
            raise RuntimeError("ArrayType align is symbolic")
        return self.element.align()

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, ArrayType)
            and value.element == self.element
            and value.count == self.count
        )

    def __repr__(self) -> str:
        return f"ArrayType({self.element}, {self.count})"

    def __hash__(self) -> int:
        return hash((ArrayType, self.element, self.count))


class PointerType(Type):
    element: Type

    def __init__(self, element: Type) -> None:
        super().__init__()
        self.element = element

    def size(self) -> int:
        return 8

    def align(self) -> int:
        return 8

    def __eq__(self, value: object) -> bool:
        return isinstance(value, PointerType) and value.element == self.element

    def __repr__(self) -> str:
        return f"PointerType({self.element})"

    def __hash__(self) -> int:
        return hash((PointerType, self.element))


class StructType(Type):
    _fields: List[Tuple[str, Type]]
    _field_dict: Dict[str, Type]

    def __init__(self, fields: List[Tuple[str, Type]]) -> None:
        super().__init__()
        self._fields = fields
        self._field_dict = {name: ty for name, ty in fields}

    @property
    def fields(self) -> List[Tuple[str, Type]]:
        return self._fields

    def size(self) -> int:
        return sum(field.size() for _, field in self.fields)

    def align(self) -> int:
        return max(field.align() for _, field in self.fields)

    def __eq__(self, value: object) -> bool:
        return value is self or (
            isinstance(value, StructType) and value.fields == self.fields
        )

    @override
    def member(self, field: Any) -> Optional['Type']:
        if isinstance(field, str):
            if field in self._field_dict:
                return self._field_dict[field]
        return None


class SymbolicType(Type):
    """A type that is not yet resolved."""

    name: str

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def size(self) -> int:
        raise RuntimeError("SymbolicType has no size")

    def align(self) -> int:
        raise RuntimeError("SymbolicType has no align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, SymbolicType) and value.name == self.name

    def __hash__(self) -> int:
        return hash((SymbolicType, self.name))


class TypeParameter:
    symbol: Union[SymbolicType, "SymbolicConstant"]
    bound: List[Type]

    def __init__(
        self, symbol: Union[SymbolicType, "SymbolicConstant"], bound: List[Type]
    ) -> None:
        self.symbol = symbol
        self.bound = bound


class OpaqueType(Type):
    name: str

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def size(self) -> int:
        raise RuntimeError("OpaqueType has no size")

    def align(self) -> int:
        raise RuntimeError("OpaqueType has no align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, OpaqueType) and value.name == self.name

    def __hash__(self) -> int:
        return hash((OpaqueType, self.name))


class ParametricType(Type):
    """A parametric type that is not yet resolved."""

    name: str
    params: List[TypeParameter]
    body: Type

    def __init__(self, name: str, params: List[TypeParameter], body: Type) -> None:
        super().__init__()
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

    def __hash__(self) -> int:
        return hash((ParametricType, self.name, tuple(self.params)))


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


class FunctionType(Type):
    func_like: FunctionLike

    def __init__(self, func_like: FunctionLike) -> None:
        self.func_like = func_like

    def __eq__(self, value: object) -> bool:
        return isinstance(value, FunctionType) and id(value.func_like) == id(self.func_like)

    def __hash__(self) -> int:
        return hash((FunctionType, id(self.func_like)))

    def size(self) -> int:
        raise RuntimeError("FunctionType has no size")

    def align(self) -> int:
        raise RuntimeError("FunctionType has no align")


class Use:
    value: 'Node'
    user: 'Node'

    def __init__(self, value: 'Node', user: 'Node') -> None:
        self.value = value
        self.user = user


class UseList:
    uses: List[Use]
    user_to_value: Dict['Node', 'Node']
    value_to_user: Dict['Node', 'Node']

    def __init__(self) -> None:
        self.uses = []
        self.user_to_value = {}
        self.value_to_user = {}

    def append(self, use: Use) -> None:
        self.uses.append(use)
        self.user_to_value[use.user] = use.value
        self.value_to_user[use.value] = use.user


def rebuild_usedef_chain(roots: List['Node']) -> None:
    # first find all reachable nodes
    def find_reachable() -> List['Node']:
        reachable = []
        stack = list(roots)
        while stack:
            node = stack.pop()
            if node in reachable:
                continue
            reachable.append(node)
            stack.extend(node.children())
        return reachable
    # clear all uses
    for node in find_reachable():
        node.uses = []
    # rebuild all uses
    for node in find_reachable():
        for child in node.children():
            node.uses.append(Use(child, node))


class Node:
    """
    Base class for all nodes in the HIR. A node could be a value, a reference, or a statement.
    Nodes equality is based on their identity.
    """
    uses: List[Use]
    span: Optional[Span]

    def __init__(self) -> None:
        self.uses = []
        self.span = None

    def replace_child(self, old: 'Node', new: 'Node') -> None:
        pass

    def children(self) -> List['Node']:
        """Return a list of children nodes."""
        return []

    def __eq__(self, value: object) -> bool:
        return value is self

    def __hash__(self) -> int:
        return id(self)

    def replace_uses_with(self, new: 'Node') -> None:
        for use in self.uses:
            use.user.replace_child(self, new)


class TypedNode(Node):
    """
    A node with a type, which can either be values or references.
    """
    type: Optional[Type]

    def __init__(
        self, type: Optional[Type] = None, span: Optional[Span] = None
    ) -> None:
        super().__init__()
        self.type = type
        self.span = span


class Ref(TypedNode):
    pass


class Value(TypedNode):
    pass


class SymbolicConstant(Value):
    name: str

    def __init__(
        self, name: str, type: Optional[Type] = None, span: Optional[Span] = None
    ) -> None:
        super().__init__(type, span)
        self.name = name


class ValueRef(Ref):
    value: Value

    def __init__(self, value: Value) -> None:
        super().__init__(value.type, value.span)
        self.value = value

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        assert isinstance(new, Value)
        if old is self.value:
            self.value = new

    @override
    def children(self) -> List[Node]:
        return [self.value]


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


class Member(Ref):
    base: Ref
    field: str

    def __init__(self, base: Ref, field: str, span: Optional[Span]) -> None:
        super().__init__(None, span)
        self.base = base
        self.field = field

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        assert isinstance(new, Ref)
        if old is self.base:
            self.base = new

    @override
    def children(self) -> List[Node]:
        return [self.base]


class Index(Ref):
    base: Ref
    index: Value

    def __init__(self, base: Ref, index: Value, span: Optional[Span]) -> None:
        super().__init__(None, span)
        self.base = base
        self.index = index

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        if old is self.index:
            assert isinstance(new, Value)
            self.index = new
        elif old is self.base:
            assert isinstance(new, Ref)
            self.base = new

    @override
    def children(self) -> List[Node]:
        return [self.base, self.index]


class Load(Value):
    ref: Ref

    def __init__(self, ref: Ref) -> None:
        super().__init__(ref.type, ref.span)
        self.ref = ref

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        assert isinstance(new, Ref)
        if old is self.ref:
            self.ref = new

    @override
    def children(self) -> List[Node]:
        return [self.ref]


class CallOpKind(Enum):
    FUNC = auto()
    BINARY_OP = auto()
    UNARY_OP = auto()


class Constant(Value):
    value: Any

    def __init__(self, value: Any, span: Optional[Span] = None) -> None:
        super().__init__(None, span)
        self.value = value


class Call(Value):
    op: Value | str
    args: List[Value]
    kind: CallOpKind
    resolved: bool

    def __init__(
        self,
        op: Value | str,
        args: List[Value],
        kind: CallOpKind,
        resolved: bool,
        span: Optional[Span] = None,
    ) -> None:
        super().__init__(op.type if isinstance(op, Value) else None, span)
        self.op = op
        self.args = args
        self.kind = kind
        self.resolved = resolved

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        assert isinstance(new, Value)
        if old is self.op:
            self.op = new
        else:
            for i, arg in enumerate(self.args):
                if old is arg:
                    self.args[i] = new

    @override
    def children(self) -> List[Node]:
        lst = []
        if isinstance(self.op, Value):
            lst.append(self.op)
        lst.extend(self.args)
        return cast(List[Node], lst)


class TypeInferenceError(Exception):
    pass


class TypeRule(ABC):
    @abstractmethod
    def infer(self, args: List[Type]) -> Type:
        pass

    @staticmethod
    def from_fn(fn: Callable[[List[Type]], Type]) -> "TypeRule":
        return TypeRuleFn(fn)


class TypeRuleFn(TypeRule):
    fn: Callable[[List[Type]], Type]

    def __init__(self, fn: Callable[[List[Type]], Type]) -> None:
        self.fn = fn

    def infer(self, args: List[Type]) -> Type:
        return self.fn(args)


class BuiltinFunction:
    name: str
    type_rule: TypeRule

    def __init__(self, name: str, type_rule: TypeRule) -> None:
        self.name = name
        self.type_rule = type_rule


class Stmt(Node):
    def __init__(self, span: Optional[Span] = None) -> None:
        super().__init__()
        self.span = span


class VarDecl(Stmt):
    var: Var
    expected_type: Type

    def __init__(self, var: Var, expected_type: Type, span: Optional[Span] = None) -> None:
        super().__init__(span)
        self.var = var
        self.expected_type = expected_type

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        assert isinstance(new, Var)
        if old is self.var:
            self.var = new


class Assign(Stmt):
    ref: Ref
    value: Value
    expected_type: Optional[Type]

    def __init__(self, ref: Ref, expected_type: Optional[Type], value: Value, span: Optional[Span] = None) -> None:
        super().__init__(span)
        self.ref = ref
        self.value = value
        self.expected_type = expected_type

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        if old is self.ref:
            assert isinstance(new, Ref)
            self.ref = new
        elif old is self.value:
            assert isinstance(new, Value)
            self.value = new

    @override
    def children(self) -> List[Node]:
        return [self.ref, self.value]


class Return(Stmt):
    value: Optional[Value]

    def __init__(self, value: Optional[Value], span: Optional[Span] = None) -> None:
        super().__init__(span)
        self.value = value

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        if old is self.value:
            assert isinstance(new, Value)
            self.value = new

    @override
    def children(self) -> List[Node]:
        return [self.value] if self.value is not None else []


class Function:
    name: str
    params: List[Var]
    return_type: Type
    body: List[Stmt]
    builtin: bool
    export: bool
    locals: List[Var]
    fully_typed: bool

    def __init__(
        self,
        name: str,
        params: List[Var],
        return_type: Type,
        body: List[Stmt],
        locals: List[Var],
        builtin: bool = False,
        export: bool = False,
    ) -> None:
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.builtin = builtin
        self.export = export
        self.locals = locals
        self.fully_typed = False

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

    def rebuild_usedef_chain(self) -> None:
        roots: Set[Node] = set()
        for param in self.params:
            roots.add(param)
        for stmt in self.body:
            roots.add(stmt)
        for local in self.locals:
            roots.add(local)
        rebuild_usedef_chain(list(roots))


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
    # deferred: List[Callable[[], None]]

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
        # self.deferred = []

    # def flush(self) -> None:
    #     for fn in self.deferred:
    #         fn()
    #     self.deferred = []


class FuncMetadata:
    pass


class StructMetadata:
    pass


def get_dsl_func(func: Callable[..., Any]) -> Optional[Function]:
    func_ = GlobalContext.get().functions.get(func)
    success = func_ is not None
    if not func_:
        # check if __luisa_func__ is set
        luisa_func = getattr(func, "__luisa_func__", None)
        if luisa_func:
            func_ = GlobalContext.get().functions.get(luisa_func)
            success = func_ is not None
    if not success:
        return None
    assert func_
    return func_
