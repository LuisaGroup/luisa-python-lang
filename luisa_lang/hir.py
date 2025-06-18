import ast
from dataclasses import dataclass
from enum import Enum, auto
import os
import sys
from typing import (
    Any,
    Callable,
    List,
    Literal,
    Optional,
    Protocol,
    Set,
    Tuple,
    Dict,
    Union,
    ClassVar,
)
import typing
from typing_extensions import override
from luisa_lang import classinfo
from luisa_lang.utils import Span, round_to_align, unwrap
from abc import ABC, abstractmethod

PATH_PREFIX = "luisa_lang"


class Type(ABC):
    methods: Dict[str, "FunctionTemplate"]

    def __init__(self):
        self.methods = {}

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

    def member(self, field: Any) -> Optional["Type"]:
        return None

    def is_concrete(self) -> bool:
        return True

    def is_addressable(self) -> bool:
        return True

    def __len__(self) -> int:
        return 1

    def remove_ref(self) -> "Type":
        if isinstance(self, RefType):
            return self.element
        return self


class RefType(Type):
    """
    A logical reference type. Cannot be returned from functions/stored in aggregates.
    """

    element: Type

    def __init__(self, element: Type) -> None:
        super().__init__()
        assert (
            element.is_addressable()
        ), f"RefType element {
            element} is not addressable"
        assert not isinstance(element, (OpaqueType, RefType))
        self.element = element

    def size(self) -> int:
        raise RuntimeError("RefTypes are logical and thus do not have a size")

    def align(self) -> int:
        raise RuntimeError("RefTypes are logical and thus do not have an align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, RefType) and value.element == self.element

    def __hash__(self) -> int:
        return hash((RefType, self.element))

    def __str__(self) -> str:
        return f"Ref[{self.element}]"

    @override
    def member(self, field: Any) -> Optional["Type"]:
        ty = self.element.member(field)
        if ty is None:
            return None
        return RefType(ty)

    @override
    def is_addressable(self) -> bool:
        return False


class LiteralType(Type):
    value: Any

    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value = value

    def size(self) -> int:
        raise RuntimeError("LiteralType has no size")

    def align(self) -> int:
        raise RuntimeError("LiteralType has no align")

    @override
    def is_concrete(self) -> bool:
        return False

    @override
    def is_addressable(self) -> bool:
        return False

    def __eq__(self, value: object) -> bool:
        return isinstance(value, LiteralType) and value.value == self.value

    def __hash__(self) -> int:
        return hash((LiteralType, self.value))


class UnitType(Type):
    def size(self) -> int:
        return 0

    def align(self) -> int:
        return 1

    def __eq__(self, value: object) -> bool:
        return isinstance(value, UnitType)

    def __hash__(self) -> int:
        return hash(UnitType)

    def __str__(self) -> str:
        return "UnitType"


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
    _align: int
    _size: int

    def __init__(self, element: Type, count: int, align: int | None = None) -> None:
        super().__init__()
        if align is None:
            align = element.align()
        self.element = element
        self.count = count
        self._align = align
        assert (self.element.size() * self.count) % self._align == 0
        self._size = round_to_align(self.element.size() * self.count, self._align)

    def size(self) -> int:
        return self._size

    def align(self) -> int:
        return self._align

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
    def member(self, field: Any) -> Optional["Type"]:
        comps = "xyzw"[: self.count]
        if isinstance(field, str) and field in comps:
            return self.element
        return Type.member(self, field)

    def __len__(self) -> int:
        return self.count


class MatrixType(Type):
    pass


class ArrayType(Type):
    element: Type
    count: int

    def __init__(self, element: Type, count: int) -> None:
        super().__init__()
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
        return self is value or (
            isinstance(value, TupleType) and value.elements == self.elements
        )

    def __repr__(self) -> str:
        return f"TupleType({self.elements})"

    def __hash__(self) -> int:
        return hash((TupleType, tuple(self.elements)))

    def __str__(self) -> str:
        return f"({', '.join(str(e) for e in self.elements)})"

    @override
    def member(self, field: Any) -> Optional["Type"]:
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

    def __init__(
        self, name: str, display_name: str, fields: List[Tuple[str, Type]]
    ) -> None:
        super().__init__()
        self.name = name
        self._fields = fields
        self.display_name = display_name
        self._field_dict = {name: ty for name, ty in fields}

    @property
    def fields(self) -> List[Tuple[str, Type]]:
        return self._fields

    @fields.setter
    def fields(self, value: List[Tuple[str, Type]]) -> None:
        self._fields = value
        self._field_dict = {name: ty for name, ty in value}

    def size(self) -> int:
        return sum(field.size() for _, field in self.fields)

    def align(self) -> int:
        return max(field.align() for _, field in self.fields)

    def __str__(self) -> str:
        return self.display_name

    @override
    def __eq__(self, value: object) -> bool:
        return value is self or (
            isinstance(value, StructType)
            and value.fields == self.fields
            and value.name == self.name
        )

    @override
    def member(self, field: Any) -> Optional["Type"]:
        if isinstance(field, str):
            if field in self._field_dict:
                return self._field_dict[field]
        return Type.member(self, field)

    @override
    def __hash__(self) -> int:
        return hash((StructType, tuple(self.fields), self.name))


class OpaqueType(Type):
    name: str
    extra_args: List[Any]

    def __init__(self, name: str, extra: List[Any] | None = None) -> None:
        super().__init__()
        self.name = name
        self.extra_args = extra or []

    def size(self) -> int:
        raise RuntimeError("OpaqueType has no size")

    def align(self) -> int:
        raise RuntimeError("OpaqueType has no align")

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, OpaqueType)
            and value.name == self.name
            and value.extra_args == self.extra_args
        )

    def __hash__(self) -> int:
        return hash((OpaqueType, self.name, tuple(self.extra_args)))

    def __str__(self) -> str:
        return self.name

    @override
    def is_concrete(self) -> bool:
        return False

    @override
    def is_addressable(self) -> bool:
        return False


class TemplateArgs(Protocol):
    pass


class Template[T, Args: TemplateArgs]:
    cache: Dict[Args, T]
    instantiation_func: Callable[[Args], T]
    arg_type: type[Args]

    def __init__(
        self, arg_type: type[Args], instantiation_func: Callable[[Args], T]
    ) -> None:
        self.cache = {}
        self.instantiation_func = instantiation_func
        self.arg_type = arg_type

    def instantiate(self, args: Args) -> T:
        if args in self.cache:
            return self.cache[args]
        func = self.instantiation_func(args)
        self.cache[args] = func
        return func

    def default(self) -> T:
        return self.instantiate(self.arg_type())

    def clear_instantiations(self) -> None:
        self.cache = {}


type TypeTemplateArgs = Tuple[classinfo.VarType, ...]


class TypeTemplate(Template[Type, TypeTemplateArgs]):
    pass


class PyTreeStructure: # TODO: refactor this into another file
    metadata: (
        Tuple[type, Tuple[Any], Any] | None
    )  # for JitVars, this is (type, type_args, hir.Type), for other types, this is (type, (), Any)
    children: List["PyTreeStructure"]

    def __init__(
        self,
        metadata: Tuple[type, Tuple[Any], Any] | None = None,
        children: List["PyTreeStructure"] | None = None,
    ) -> None:
        self.metadata = metadata
        self.children = children or []

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, PyTreeStructure):
            return False
        if self.metadata != value.metadata:
            return False
        if len(self.children) != len(value.children):
            return False
        for a, b in zip(self.children, value.children):
            if a != b:
                return False
        return True

    def __hash__(self) -> int:
        h = hash(PyTreeStructure)
        if self.metadata is not None:
            h ^= hash(self.metadata[0])
            for arg in self.metadata[1]:
                h ^= hash(arg)
            h ^= hash(self.metadata[2])
        for child in self.children:
            h ^= hash(child)
        return h


type FunctionTemplateArg = PyTreeStructure


class FunctionTemplateArgs:
    __args: List[FunctionTemplateArg]
    __kwargs: Dict[str, FunctionTemplateArg]

    def __init__(
        self,
        args: List[FunctionTemplateArg] | None = None,
        kwargs: Dict[str, FunctionTemplateArg] | None = None,
    ) -> None:
        self.__args = args or []
        self.__kwargs = kwargs or {}

    @property
    def args(self) -> List[FunctionTemplateArg]:
        return self.__args

    @property
    def kwargs(self) -> Dict[str, FunctionTemplateArg]:
        return self.__kwargs

    def __eq__(self, other) -> bool:
        if not isinstance(other, FunctionTemplateArgs):
            return False
        other_args = other.args
        other_kwargs = other.kwargs

        return (
            len(self.__args) == len(other_args)
            and all(a == b for a, b in zip(self.__args, other_args))
            and len(self.__kwargs) == len(other_kwargs)
            and all(
                k in self.__kwargs and self.__kwargs[k] == v
                for k, v in other_kwargs.items()
            )
        )

    def __hash__(self) -> int:
        h = hash(FunctionTemplateArgs)
        h ^= hash(len(self.__args))
        for a in self.__args:
            h ^= hash(a)
        h ^= hash(len(self.__kwargs))
        for k, v in self.__kwargs.items():
            h ^= hash(k)
            h ^= hash(v)
        return h


class FunctionTemplate(Template["Function", FunctionTemplateArgs]):
    pass


class Function:
    name: str
    params: List["Var"]
    locals: List["Var"]
    body: "BasicBlock"
    return_jitvar_type: typing.Type['Any']
    return_type: Type

    def __init__(
        self,
        name: str,
        params: List["Var"],
        locals: List["Var"],
        body: "BasicBlock",
        return_jitvar_type: typing.Type['Any'],
        return_type: Type
    ) -> None:
        self.name = name
        self.params = params
        self.locals = locals
        self.body = body
        self.return_type = return_type
        self.return_jitvar_type = return_jitvar_type


class Node:
    """
    Base class for all nodes in the HIR. A node could be a value, a reference, or a statement.
    Nodes equality is based on their identity.
    """

    span: Optional[Span]
    prev: Optional["Node"]
    next: Optional["Node"]
    block: Optional["BasicBlock"]
    func: Optional[Function]

    def __init__(self, span: Optional[Span] = None) -> None:
        self.span = span
        self.prev = None
        self.next = None
        self.block = None
        self.func = None

    def __eq__(self, value: object) -> bool:
        return value is self

    def __hash__(self) -> int:
        return id(self)

    def append(self, node: "Node") -> "Node":
        assert node.next is None
        assert node.prev is None
        if node.block is not None:
            assert node.block is self.block
        else:
            node.block = self.block
        if self.next is not None:
            self.next.prev = node
        node.prev = self
        node.next = self.next
        self.next = node
        if self.block:
            if self.block.tail is self:
                self.block.tail = node
        return node

    def prepend(self, node: "Node") -> "Node":
        assert node.next is None
        assert node.prev is None
        if node.block is not None:
            assert node.block is self
        else:
            node.block = self.block
        if self.prev is not None:
            self.prev.next = node
        node.next = self
        node.prev = self.prev
        self.prev = node
        if self.block:
            if self.block.head is self:
                self.block.head = node
        return node

    def remove(self) -> None:
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev
        self.prev = None
        self.next = None


class SpannedError(Exception):
    span: Span | None
    message: str
    stack_trace: str | None

    def __init__(self, node: Node | Span | ast.AST | None, message: str) -> None:
        if node is not None:
            match node:
                case Node():
                    self.span = node.span
                case Span():
                    self.span = node
                case ast.AST():
                    self.span = Span.from_ast(node)
        else:
            self.span = None
        self.message = message
        self.stack_trace = None


class TypeCheckError(SpannedError):
    pass


class BasicBlock(Node):
    head: Node | None
    tail: Node | None
    terminated: bool

    def __init__(self, span: Optional[Span] = None) -> None:
        self.head = None
        self.tail = None
        self.terminated = False
        self.span = span

    def append[T: Node](self, node: T) -> T:
        assert node.block is None
        node.block = self
        if isinstance(node, Terminator):
            assert not self.terminated
            self.terminated = True
        if self.tail is not None:
            self.tail = self.tail.append(node)
        else:
            self.head = node
            self.tail = node
        return node

    def nodes(self) -> List[Node]:
        nodes = []
        node = self.head
        while node is not None:
            nodes.append(node)
            node = node.next
        return nodes


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


class Value(TypedNode):
    def is_ref(self) -> bool:
        assert self.type is not None
        return isinstance(self.type, RefType)


class Unit(Value):
    def __init__(self) -> None:
        super().__init__(UnitType())


class ParameterSemantic(Enum):
    BYVAL = auto()
    BYREF = auto()


class Var(TypedNode):
    name: str
    semantic: ParameterSemantic

    def __init__(
        self,
        name: str,
        type: Optional[Type],
        span: Optional[Span],
        semantic: ParameterSemantic = ParameterSemantic.BYVAL,
    ) -> None:
        assert not isinstance(type, RefType)
        super().__init__(type, span)
        self.name = name
        self.semantic = semantic


class VarValue(Value):
    var: Var

    def __init__(self, var: Var, span: Optional[Span]) -> None:
        super().__init__(var.type, span)
        self.var = var


class VarRef(Value):
    var: Var

    def __init__(self, var: Var, span: Optional[Span] = None) -> None:
        # assert var.type is not None
        if var.type is not None:
            super().__init__(RefType(var.type), span)
        else:
            super().__init__(None, span)
        self.var = var


class Member(Value):
    base: Value
    field: str

    def __init__(
        self, base: Value, field: str, type: Type, span: Optional[Span]
    ) -> None:
        super().__init__(type, span)
        self.base = base
        self.field = field


class Index(Value):
    base: Value
    index: Value

    def __init__(
        self, base: Value, index: Value, type: Type, span: Optional[Span]
    ) -> None:
        super().__init__(type, span)
        self.base = base
        self.index = index


class Load(Value):
    ref: Value

    def __init__(self, ref: Value) -> None:
        assert isinstance(ref.type, RefType)
        super().__init__(ref.type.remove_ref(), ref.span)
        self.ref = ref


class Constant(Value):
    value: Any

    def __init__(
        self, value: Any, type: Type | None = None, span: Optional[Span] = None
    ) -> None:
        super().__init__(type, span)
        self.value = value

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, Constant)
            and type(value.value) == type(self.value)
            and value.value == self.value
        )

    def __hash__(self) -> int:
        return hash((Constant, self.value))


class Alloca(Value):
    """
    A temporary variable
    """

    def __init__(self, ty: Type, span: Optional[Span] = None) -> None:
        # assert isinstance(ty, RefType), f"expected a RefType but got {ty}"
        super().__init__(RefType(ty), span)


# class Init(Value):
#     init_call: 'Call'

#     def __init__(self, init_call: 'Call', ty: Type,  span: Optional[Span] = None) -> None:
#         super().__init__(ty, span)
#         self.init_call = init_call


class AggregateInit(Value):
    args: List[Value]

    def __init__(
        self, args: List[Value], type: Type, span: Optional[Span] = None
    ) -> None:
        super().__init__(type, span)
        self.args = args


class Intrinsic(Value):
    name: str
    args: List[Value]

    def __init__(
        self, name: str, args: List[Value], type: Type, span: Optional[Span] = None
    ) -> None:
        super().__init__(type, span)
        self.name = name
        self.args = args

    def __str__(self) -> str:
        return f"Intrinsic({self.name}, {self.args})"

    def __repr__(self) -> str:
        return f"Intrinsic({self.name}, {self.args})"


class Call(Value):
    op: "Function"

    args: List[Value]

    def __init__(
        self,
        op: "Function",
        args: List[Value],
        type: Type,
        span: Optional[Span] = None,
    ) -> None:
        super().__init__(type, span)
        self.op = op
        self.args = args


class Assign(Node):
    ref: Value
    value: Value

    def __init__(self, ref: Value, value: Value, span: Optional[Span] = None) -> None:
        assert not isinstance(value.type, (RefType))
        if not isinstance(ref.type, RefType):
            raise TypeCheckError(ref, f"cannot assign to a non-reference variable")
        super().__init__(span)
        self.ref = ref
        self.value = value


class Assert(Node):
    cond: Value
    msg: List[Union[Value, str]]

    def __init__(
        self, cond: Value, msg: List[Union[Value, str]], span: Optional[Span] = None
    ) -> None:
        super().__init__(span)
        self.cond = cond
        self.msg = msg


class Print(Node):
    args: List[Union[Value, str]]

    def __init__(
        self, args: List[Union[Value, str]], span: Optional[Span] = None
    ) -> None:
        super().__init__(span)
        self.args = args


class Terminator(Node):
    pass


class Loop(Terminator):
    prepare: BasicBlock
    cond: Optional[Value]
    body: BasicBlock
    update: Optional[BasicBlock]
    merge: BasicBlock

    def __init__(
        self,
        prepare: BasicBlock,
        cond: Optional[Value],
        body: BasicBlock,
        update: Optional[BasicBlock],
        merge: BasicBlock,
        span: Optional[Span] = None,
    ) -> None:
        super().__init__(span)
        self.prepare = prepare
        self.cond = cond
        self.body = body
        self.update = update
        self.merge = merge


class Break(Terminator):
    target: Loop | None

    def __init__(self, target: Loop | None, span: Optional[Span] = None) -> None:
        super().__init__(span)
        self.target = target


class Continue(Terminator):
    target: Loop | None

    def __init__(self, target: Loop | None, span: Optional[Span] = None) -> None:
        super().__init__(span)
        self.target = target


class If(Terminator):
    cond: Value
    then_body: BasicBlock
    else_body: Optional[BasicBlock]
    merge: BasicBlock

    def __init__(
        self,
        cond: Value,
        then_body: BasicBlock,
        else_body: Optional[BasicBlock],
        merge: BasicBlock,
        span: Optional[Span] = None,
    ) -> None:
        super().__init__(span)
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body
        self.merge = merge


class Return(Terminator):
    value: Optional[Value]

    def __init__(self, value: Optional[Value], span: Optional[Span] = None) -> None:
        super().__init__(span)
        self.value = value


class Range(Value):
    start: Value
    step: Value
    stop: Value

    def __init__(
        self, start: Value, stop: Value, step: Value, span: Optional[Span] = None
    ) -> None:
        super().__init__(None, span)
        self.start = start
        self.stop = stop
        self.step = step

    def value_type(self) -> Type:
        types = [self.start.type, self.stop.type, self.step.type]
        return unwrap(types[0])


class GlobalContext:
    types: Dict[type, TypeTemplate]
    functions: Dict[Callable[..., Any], FunctionTemplate]
    _instance: ClassVar["GlobalContext"]

    @staticmethod
    def get() -> "GlobalContext":
        if not hasattr(GlobalContext, "_instance"):
            GlobalContext._instance = GlobalContext.__new__(GlobalContext)
            GlobalContext._instance.types = {}
            GlobalContext._instance.functions = {}
        return GlobalContext._instance

    def clear_all_instantiations(self) -> None:
        for ty in self.types.values():
            ty.clear_instantiations()
        for func in self.functions.values():
            func.clear_instantiations()


def get_dsl_type(target: type) -> TypeTemplate:
    """
    Get the inner DSL type representation of a type
    """
    ctx = GlobalContext.get()
    ty = ctx.types.get(target)
    assert ty, f"no DSL type for {target} (id: {id(target)})"
    return ty
