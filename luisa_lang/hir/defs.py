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


# @dataclass
# class FunctionTemplateResolveResult:
#     func: Optional[FunctionLike]
#     matched: bool


FunctionTemplateResolvingArgs = List[Tuple[str, Union['Type', 'Value']]]
"""
[Function parameter name, Type or Value].
The reason for using parameter name instead of GenericParameter is that python supports passing type[T] as a parameter,
"""

FunctionTemplateResolvingFunc = Callable[[
    FunctionTemplateResolvingArgs], FunctionLike]


class FunctionTemplate:
    """
    Contains a delegate that can be resolved to a function.
    This is to support generic functions as well as meta-programming.
    Since each time the function is called in DSL, user meta-programming code in the function body
    will be called, we need to keep the AST of the function.

    """
    parsing_func: FunctionTemplateResolvingFunc
    __resolved: Dict[Tuple[Tuple[str,
                                 Union['Type', 'Value']], ...], FunctionLike]
    is_generic: bool
    name: str
    params: List[str]
    """Function parameters (NOT type parameters)"""

    def __init__(self, name: str, params: List[str], parsing_func: FunctionTemplateResolvingFunc, is_generic: bool) -> None:
        self.parsing_func = parsing_func
        self.__resolved = {}
        self.params = params
        self.is_generic = is_generic
        self.name = name

    def resolve(self, args: FunctionTemplateResolvingArgs | None) -> FunctionLike:
        args = args or []
        if not self.is_generic:
            key = tuple(args)
        else:
            key = tuple()
        if key in self.__resolved:
            return self.__resolved[key]
        func = self.parsing_func(args)
        self.__resolved[key] = func
        return func

    def reset(self) -> None:
        self.__resolved = {}


def resolve_function(f: FunctionTemplate | FunctionLike, args: FunctionTemplateResolvingArgs | None) -> FunctionLike:
    if isinstance(f, FunctionTemplate):
        return f.resolve(args)
    return f


class Type(ABC):
    methods: Dict[str, Union[FunctionTemplate, "BuiltinFunction"]]
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

    def resolved_method(self, name: str, args: FunctionTemplateResolvingArgs | None) -> Optional[FunctionLike]:
        m = self.methods.get(name)
        if m:
            return resolve_function(m, args)
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

    def __str__(self) -> str:
        return "bool"


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

    def __str__(self) -> str:
        return f"{'i' if self.signed else 'u'}{self.bits}"


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

    @override
    def __repr__(self) -> str:
        return f"GenericFloatType()"

    @override
    def __str__(self) -> str:
        return "float"


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

    @override
    def __repr__(self) -> str:
        return f"GenericIntType()"

    @override
    def __str__(self) -> str:
        return "int"


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

    def __str__(self) -> str:
        return f"f{self.bits}"


class VectorType(Type):
    element: Type
    count: int

    def __init__(self, element: Type, count: int) -> None:
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

    def __str__(self) -> str:
        return f"<{self.count} x {self.element}>"

    @override
    def member(self, field: Any) -> Optional['Type']:
        comps = 'xyzw'[:self.count]
        if isinstance(field, str) and field in comps:
            return self.element
        return Type.member(self, field)


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

    def __str__(self) -> str:
        return f"[{self.count} x {self.element}]"


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

    def __str__(self) -> str:
        return f"*{self.element}"


class TupleType(Type):
    elements: List[Type]

    def __init__(self, elements: List[Type]) -> None:
        super().__init__()
        self.elements = elements

    def size(self) -> int:
        return sum(element.size() for element in self.elements)

    def align(self) -> int:
        return max(element.align() for element in self.elements)

    def __eq__(self, value: object) -> bool:
        return self is value or (isinstance(value, TupleType) and value.elements == self.elements)

    def __repr__(self) -> str:
        return f"TupleType({self.elements})"

    def __hash__(self) -> int:
        return hash((TupleType, tuple(self.elements)))

    def __str__(self) -> str:
        return f"({', '.join(str(e) for e in self.elements)})"

    @override
    def member(self, field: Any) -> Optional['Type']:
        if isinstance(field, int):
            if field < len(self.elements):
                return self.elements[field]
        return Type.member(self, field)


class StructType(Type):
    name: str
    display_name: str
    _fields: List[Tuple[str, Type]]
    _field_dict: Dict[str, Type]
    # _monomorphification_cache: Dict[Tuple['GenericParameter', Type | 'Value'], Type]

    def __init__(self, name: str,   display_name: str, fields: List[Tuple[str, Type]]) -> None:
        super().__init__()
        self.name = name
        self._fields = fields
        self.display_name = display_name
        self._field_dict = {name: ty for name, ty in fields}

    @property
    def fields(self) -> List[Tuple[str, Type]]:
        return self._fields

    def size(self) -> int:
        return sum(field.size() for _, field in self.fields)

    def align(self) -> int:
        return max(field.align() for _, field in self.fields)

    def __str__(self) -> str:
        return self.display_name

    @override
    def __eq__(self, value: object) -> bool:
        return value is self or (
            isinstance(
                value, StructType) and value.fields == self.fields and value.name == self.name
        )

    @override
    def member(self, field: Any) -> Optional['Type']:
        if isinstance(field, str):
            if field in self._field_dict:
                return self._field_dict[field]
        return Type.member(self, field)

    @override
    def __hash__(self) -> int:
        return hash((StructType, tuple(self.fields), self.name))


class TypeBound:
    pass


class AnyBound(TypeBound):
    pass


class SubtypeBound(TypeBound):
    super_type: Type

    def __init__(self, super_type: Type) -> None:
        self.super_type = super_type

    def __repr__(self) -> str:
        return f"SubtypeBound({self.super_type})"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, SubtypeBound) and value.super_type == self.super_type


class UnionBound(TypeBound):
    bounds: List[SubtypeBound]

    def __init__(self, bounds: List[SubtypeBound]) -> None:
        self.bounds = bounds

    def __repr__(self) -> str:
        return f"UnionBound({self.bounds})"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, UnionBound) and value.bounds == self.bounds


class GenericParameter:
    """
    A GenericParameter contains three parts:
        name@ctx_name: bound
    """
    name: str
    """ name of the generic parameter in source code, e.g. 'T'"""
    ctx_name: str
    """ a string describing the context (where the generic parameter is defined), e.g. 'some_function' """
    bound: TypeBound | None

    def __init__(
        self, name: str, ctx_name: str, bound: TypeBound | None = None
    ) -> None:
        self.name = name
        self.ctx_name = ctx_name
        self.bound = bound

    def __eq__(self, value: object) -> bool:
        return (
            value is self or (
                isinstance(value, GenericParameter)
                and value.name == self.name
                and value.ctx_name == self.ctx_name)
        )

    def __hash__(self) -> int:
        return hash((GenericParameter, self.name, self.ctx_name))

    def __repr__(self) -> str:
        bound_str = f" : {self.bound}" if self.bound else ""
        return f"GenericParameter({self.name}, {self.ctx_name}, {bound_str})"


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

    def __str__(self) -> str:
        return self.name


class SymbolicType(Type):
    param: GenericParameter

    def __init__(self, param: GenericParameter) -> None:
        super().__init__()
        self.param = param

    def size(self) -> int:
        raise RuntimeError("SymbolicType has no size")

    def align(self) -> int:
        raise RuntimeError("SymbolicType has no align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, SymbolicType) and value.param == self.param

    def __hash__(self) -> int:
        return hash((SymbolicType, self.param))

    def __str__(self) -> str:
        return f'~{self.param.name}@{self.param.ctx_name}'

    def __repr__(self) -> str:
        return f"SymbolicType({self.param})"


class ParametricType(Type):
    """
    The definition of a parametric type, e.g. class Foo[T]: ...
    """
    params: List[GenericParameter]
    body: Type

    def __init__(self, params: List[GenericParameter], body: Type) -> None:
        super().__init__()
        self.params = params
        self.body = body

    def size(self) -> int:
        raise RuntimeError("ParametricType has no size")

    def align(self) -> int:
        raise RuntimeError("ParametricType has no align")

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, ParametricType)
            and value.params == self.params
        )

    def __hash__(self) -> int:
        return hash((ParametricType, tuple(self.params)))


class BoundType(Type):
    """
    An instance of a parametric type, e.g. Foo[int]
    """
    generic: ParametricType
    args: List[Union[Type, 'SymbolicConstant']]

    def __init__(self, generic: ParametricType, args: List[Union[Type, 'SymbolicConstant']]) -> None:
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
    func_like: FunctionLike | FunctionTemplate

    def __init__(self, func_like: FunctionLike | FunctionTemplate) -> None:
        super().__init__()
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
    generic: GenericParameter

    def __init__(
        self, generic: GenericParameter, type: Optional[Type] = None, span: Optional[Span] = None
    ) -> None:
        super().__init__(type, span)
        self.generic = generic


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
    base: Ref | Value
    field: str

    def __init__(self, base: Ref | Value, field: str, span: Optional[Span]) -> None:
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
    base: Ref | Value
    index: Value

    def __init__(self, base: Ref | Value, index: Value, span: Optional[Span]) -> None:
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

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Constant) and value.value == self.value

    def __hash__(self) -> int:
        return hash(self.value)


class Call(Value):
    op: Value | str
    """After type inference, op should be a Value."""

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
    node: Node | None
    message: str

    def __init__(self, node: Node | None, message: str) -> None:
        self.node = node
        self.message = message

    def __str__(self) -> str:
        if self.node is None:
            return f"Type inference error:\n\t{self.message}"
        return f"Type inference error at {self.node.span}:\n\t{self.message}"


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


class If(Stmt):
    cond: Value
    then_body: List[Stmt]
    else_body: List[Stmt]

    def __init__(
        self, cond: Value, then_body: List[Stmt], else_body: List[Stmt], span: Optional[Span] = None
    ) -> None:
        super().__init__(span)
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

    @override
    def replace_child(self, old: Node, new: Node) -> None:
        if old is self.cond:
            assert isinstance(new, Value)
            self.cond = new
        for i, stmt in enumerate(self.then_body):
            if old is stmt:
                assert isinstance(new, Stmt)
                self.then_body[i] = new
            else:
                stmt.replace_child(old, new)

        for i, stmt in enumerate(self.else_body):
            if old is stmt:
                assert isinstance(new, Stmt)
                self.else_body[i] = new
            else:
                stmt.replace_child(old, new)

    @override
    def children(self) -> List[Node]:
        c = self.cond.children()
        for s in self.then_body:
            c.extend(s.children())
        for s in self.else_body:
            c.extend(s.children())
        return c


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


class BuiltinFunction:
    name: str
    type_rule: TypeRule

    def __init__(self, name: str, type_rule: TypeRule) -> None:
        self.name = name
        self.type_rule = type_rule


class Function:
    name: str
    generic_params: Dict[str, GenericParameter]
    params: List[Var]
    return_type: Type
    body: List[Stmt]
    builtin: bool
    export: bool
    locals: List[Var]
    fully_typed: bool
    complete: bool

    def __init__(
        self,
        name: str,
        generic_params: Dict[str, GenericParameter],
        params: List[Var],
        return_type: Type,
        body: List[Stmt],
        locals: List[Var],
        builtin: bool = False,
        export: bool = False,
        complete: bool = False,
    ) -> None:
        self.name = name
        self.generic_params = generic_params
        self.params = params
        self.return_type = return_type
        self.body = body
        self.builtin = builtin
        self.export = export
        self.locals = locals
        self.fully_typed = False
        self.complete = complete

    @property
    def is_generic(self) -> bool:
        return len(self.generic_params) > 0

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


def match_template_args(
        template: List[Tuple[str, Union[Type, Value]]],
        args: List[Type | Value]) -> Dict[GenericParameter, Type | Value]:
    mapping: Dict[GenericParameter, Type | Value] = {}

    def unify(a: Type | Value, b: Type | Value):
        """
        Perform unification on two types or values, only a could contain generic parameters.
        """
        if a is b:
            return
        if (isinstance(a, Type) and isinstance(b, Value)) or (isinstance(b, Type) and isinstance(a, Value)):
            return TypeInferenceError(None, "type and value cannot be unified")
        if isinstance(a, Type) and isinstance(b, Type):
            # unify type
            match a:
                case SymbolicType():
                    if a.param.name in mapping:
                        return unify(mapping[a.param], b)
                    if isinstance(b, GenericFloatType) or isinstance(b, GenericIntType):
                        raise TypeInferenceError(None,
                                                 "float/int literal cannot be used to infer generic type directly, wrap it with a concrete type")
                    mapping[a.param] = b
                    return
                case VectorType():
                    if not isinstance(b, VectorType):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
                    if a.count != b.count:
                        raise TypeInferenceError(
                            None, f"vector length mismach, expected {a}, got {b}")
                    unify(a.element, b.element)
                case ArrayType():
                    if not isinstance(b, ArrayType):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
                    # TODO: handle generic array length
                    if a.count != b.count:
                        raise TypeInferenceError(
                            None, f"array length mismach, expected {a}, got {b}")
                    unify(a.element, b.element)
                case PointerType():
                    if not isinstance(b, PointerType):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
                    unify(a.element, b.element)
                case TupleType():
                    if not isinstance(b, TupleType):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
                    if len(a.elements) != len(b.elements):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
                    for ea, eb in zip(a.elements, b.elements):
                        unify(ea, eb)
                case StructType():
                    raise RuntimeError(
                        "StructType should not appear in match_template_args")
                    # if not isinstance(b, StructType):
                    #     raise TypeInferenceError(
                    #         None, f"expected {a}, got {b}")
                    # if len(a.fields) != len(b.fields):
                    #     raise TypeInferenceError(
                    #         None, f"field cound mismatch, expected {a}, got {b}")
                    # for (fa, ta), (fb, tb) in zip(a.fields, b.fields):
                    #     if fa != fb:
                    #         raise TypeInferenceError(
                    #             None, f"field name mismatch,expected {a}, got {b}")
                    #     unify(ta, tb)
                case BoundType():
                    raise NotImplementedError()
                case ParametricType():
                    raise RuntimeError(
                        "ParametricType should not appear in match_template_args")
                case _:
                    if not is_type_compatible_to(b, a):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
        if isinstance(a, Value) and isinstance(b, Value):
            raise NotImplementedError()
        return False
    assert len(template) == len(args)
    for i in range(len(template)):
        unify(template[i][1], args[i])
    return mapping


def match_func_template_args(sig: Function, args: FunctionTemplateResolvingArgs) -> Dict[GenericParameter, Type | Value]:
    if len(sig.params) != len(args):
        raise TypeInferenceError(
            None, f"expected {len(sig.params)} arguments, got {len(args)}")

    template_args: List[Tuple[str, Union[Type, Value]]] = []
    for param in sig.params:
        assert param.type is not None
        template_args.append((param.name, param.type))
    matching_args = [arg[1] for arg in args]
    return match_template_args(template_args, matching_args)
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
    functions: Dict[Callable[..., Any], FunctionTemplate]
    # deferred: List[Callable[[], None]]

    @staticmethod
    def get() -> "GlobalContext":
        global _global_context
        if _global_context is None:
            _global_context = GlobalContext()
        return _global_context

    def __init__(self) -> None:
        assert _global_context is None, "GlobalContext should be a singleton"
        self.types = {
            type(None): UnitType(),
            int: GenericIntType(),
            float: GenericFloatType(),
            bool: BoolType(),
        }
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


def get_dsl_func(func: Callable[..., Any]) -> Optional[FunctionTemplate]:
    func_ = GlobalContext.get().functions.get(func)
    # print(func, GlobalContext.get().functions)
    if not func_:
        # check if __luisa_func__ is set
        luisa_func = getattr(func, "__luisa_func__", None)
        if luisa_func and isinstance(luisa_func, FunctionTemplate):
            func_ = luisa_func
    return func_


def get_dsl_type(cls: type) -> Optional[Type]:
    return GlobalContext.get().types.get(cls)


def is_type_compatible_to(ty: Type, target: Type) -> bool:
    if ty == target:
        return True
    if isinstance(target, FloatType):
        return isinstance(ty, GenericFloatType)
    if isinstance(target, IntType):
        return isinstance(ty, GenericIntType)
    return False
