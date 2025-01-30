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
    Set,
    Tuple,
    Dict,
    Union,
)
import typing
from typing_extensions import override
from luisa_lang import classinfo
from luisa_lang.utils import Span, round_to_align, unwrap
from abc import ABC, abstractmethod

PATH_PREFIX = "luisa_lang"


# @dataclass
# class FunctionTemplateResolveResult:
#     func: Optional[Function]
#     matched: bool


FunctionTemplateResolvingArgs = List[Tuple[str,
                                           Union['Type', Any]]]
"""
[Function parameter name, Type or Value].
The reason for using parameter name instead of GenericParameter is that python supports passing type[T] as a parameter,
"""


FunctionTemplateResolvingFunc = Callable[[
    FunctionTemplateResolvingArgs], Union['Function', 'TemplateMatchingError']]


class FuncProperties:
    inline: bool | Literal["never", "always"]
    export: bool

    def __init__(self):
        self.inline = False
        self.export = False


class FunctionTemplate:
    """
    Contains a delegate that can be resolved to a function.
    This is to support generic functions as well as meta-programming.
    Since each time the function is called in DSL, user meta-programming code in the function body
    will be called, we need to keep the AST of the function.

    """
    parsing_func: FunctionTemplateResolvingFunc
    _resolved: Dict[Tuple[Tuple[str,
                                Union['Type', Any]], ...], "Function"]
    is_generic: bool
    name: str
    params: List[str]
    props: Optional[FuncProperties]
    """Function parameters (NOT type parameters)"""

    def __init__(self, name: str, params: List[str], parsing_func: FunctionTemplateResolvingFunc, is_generic: bool) -> None:
        self.parsing_func = parsing_func
        self._resolved = {}
        self.params = params
        self.is_generic = is_generic
        self.name = name
        self.props = None

    def resolve(self, args: FunctionTemplateResolvingArgs | None) -> Union["Function", 'TemplateMatchingError']:
        args = args or []
        if not self.is_generic:
            key = tuple(args)
        else:
            key = tuple()
        if key in self._resolved:
            return self._resolved[key]
        func = self.parsing_func(args)
        if isinstance(func, TemplateMatchingError):
            return func
        self._resolved[key] = func
        return func

    def reset(self) -> None:
        self._resolved = {}

    def inline_hint(self) -> bool | Literal['always', 'never']:
        if self.props is None:
            return False
        return self.props.inline


class DynamicIndex:
    pass


class Type(ABC):
    methods: Dict[str, Union["Function", FunctionTemplate]]
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
            return FunctionType(m, None)
        return None

    def method(self, name: str) -> Optional[Union["Function", FunctionTemplate]]:
        m = self.methods.get(name)
        if m:
            return m
        return None

    def is_concrete(self) -> bool:
        return True

    def __len__(self) -> int:
        return 1

    def remove_ref(self) -> 'Type':
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
        assert not isinstance(element, RefType)
        self.element = element
        self.methods = element.methods

    def size(self) -> int:
        raise RuntimeError("RefTypes are logical and thus do not have a size")

    def align(self) -> int:
        raise RuntimeError(
            "RefTypes are logical and thus do not have an align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, RefType) and value.element == self.element

    def __hash__(self) -> int:
        return hash((RefType, self.element))

    def __str__(self) -> str:
        return f"Ref[{self.element}]"

    @override
    def member(self, field: Any) -> Optional['Type']:
        ty = self.element.member(field)
        if ty is None:
            return None

        return RefType(ty)


class LiteralType(Type):
    value: Any

    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value = value

    def size(self) -> int:
        raise RuntimeError("LiteralType has no size")

    def align(self) -> int:
        raise RuntimeError("LiteralType has no align")

    def is_concrete(self) -> bool:
        return False

    def __eq__(self, value: object) -> bool:
        return isinstance(value, LiteralType) and value.value == self.value

    def __hash__(self) -> int:
        return hash((LiteralType, self.value))


class AnyType(Type):
    def size(self) -> int:
        raise RuntimeError("AnyType has no size")

    def align(self) -> int:
        raise RuntimeError("AnyType has no align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, AnyType)

    def __hash__(self) -> int:
        return hash(AnyType)

    def __str__(self) -> str:
        return "AnyType"


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

    @override
    def is_concrete(self) -> bool:
        return False


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

    @override
    def is_concrete(self) -> bool:
        return False


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
        self._size = round_to_align(
            self.element.size() * self.count, self._align)

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
    def member(self, field: Any) -> Optional['Type']:
        comps = 'xyzw'[:self.count]
        if isinstance(field, str) and field in comps:
            return self.element
        return Type.member(self, field)

    def __len__(self) -> int:
        return self.count


class MatrixType(Type):
    pass


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

    def __init__(self, name: str, display_name: str, fields: List[Tuple[str, Type]]) -> None:
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
    @abstractmethod
    def satisfied_by(self, ty: Type) -> bool:
        pass


class AnyBound(TypeBound):
    @override
    def satisfied_by(self, ty: Type) -> bool:
        return True


class SubtypeBound(TypeBound):
    super_type: Type
    exact_match: bool

    def __init__(self, super_type: Type, exact_match: bool) -> None:
        self.super_type = super_type
        self.exact_match = exact_match

    def __repr__(self) -> str:
        return f"SubtypeBound({self.super_type})"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, SubtypeBound) and value.super_type == self.super_type

    @override
    def satisfied_by(self, ty: Type) -> bool:
        if self.exact_match:
            return is_type_compatible_to(ty, self.super_type)
        else:
            raise NotImplementedError()


class UnionBound(TypeBound):
    bounds: List[SubtypeBound]

    def __init__(self, bounds: List[SubtypeBound]) -> None:
        self.bounds = bounds

    def __repr__(self) -> str:
        return f"UnionBound({self.bounds})"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, UnionBound) and value.bounds == self.bounds

    @override
    def satisfied_by(self, ty: Type) -> bool:
        return any(b.satisfied_by(ty) for b in self.bounds)


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
        return isinstance(value, OpaqueType) and value.name == self.name and value.extra_args == self.extra_args

    def __hash__(self) -> int:
        return hash((OpaqueType, self.name, tuple(self.extra_args)))

    def __str__(self) -> str:
        return self.name

    @override
    def is_concrete(self) -> bool:
        return False


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


MonomorphizationFunc = Callable[[List[Type]], Type]


class ParametricType(Type):
    """
    The definition of a parametric type, e.g. class Foo[T]: ...
    """
    params: List[GenericParameter]
    body: Type
    monomorphification_cache: Dict[Tuple[Union['Type', Any], ...], 'Type']
    monomorphification_func: Optional[MonomorphizationFunc]

    def __init__(self, params: List[GenericParameter],
                 body: Type,
                 monomorphification_func: MonomorphizationFunc | None = None) -> None:
        super().__init__()
        self.params = params
        self.body = body
        self.monomorphification_func = monomorphification_func
        self.monomorphification_cache = {}

    def instantiate(self, args: List[Union[Type, Any]]) -> 'Type':
        keys = tuple(args)
        if keys in self.monomorphification_cache:
            return self.monomorphification_cache[keys]
        if self.monomorphification_func is not None:
            ty = self.monomorphification_func(args)
            self.monomorphification_cache[keys] = ty
            return ty
        raise RuntimeError("monomorphification_func is not set")

    def size(self) -> int:
        raise RuntimeError("ParametricType has no size")

    def align(self) -> int:
        raise RuntimeError("ParametricType has no align")

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, ParametricType)
            and value.params == self.params
            and value.body == self.body
        )

    def __hash__(self) -> int:
        return hash((ParametricType, tuple(self.params), self.body))


class BoundType(Type):
    """
    An instance of a parametric type, e.g. Foo[int]
    """
    generic: ParametricType
    args: List[Union[Type,  Any]]
    instantiated: Optional[Type]

    def __init__(self, generic: ParametricType, args: List[Union[Type,  Any]], instantiated: Optional[Type] = None) -> None:
        super().__init__()
        self.generic = generic
        self.args = args
        self.instantiated = instantiated

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

    def __hash__(self):
        return hash((BoundType, self.generic, tuple(self.args)))

    @override
    def member(self, field) -> Optional['Type']:
        if self.instantiated is not None:
            return self.instantiated.member(field)
        else:
            raise RuntimeError("member access on uninstantiated BoundType")

    @override
    def method(self, name) -> Optional[Union["Function", FunctionTemplate]]:
        if self.instantiated is not None:
            return self.instantiated.method(name)
        else:
            raise RuntimeError("method access on uninstantiated BoundType")


class TypeConstructorType(Type):
    inner: Type

    def __init__(self, inner: Type) -> None:
        super().__init__()
        self.inner = inner

    def size(self) -> int:
        raise RuntimeError("TypeConstructorType has no size")

    def align(self) -> int:
        raise RuntimeError("TypeConstructorType has no align")

    def __eq__(self, value: object) -> bool:
        return isinstance(value, TypeConstructorType) and value.inner == self.inner

    def __hash__(self) -> int:
        return hash((TypeConstructorType, self.inner))


class FunctionType(Type):
    func_like: Union["Function", FunctionTemplate]
    bound_object: Optional['Value']

    def __init__(self, func_like: Union["Function", FunctionTemplate], bound_object: Optional['Value']) -> None:
        super().__init__()
        self.func_like = func_like
        self.bound_object = bound_object

    def __eq__(self, value: object) -> bool:
        if self.bound_object is not None:
            return value is self
        return isinstance(value, FunctionType) and value.func_like is self.func_like and value.bound_object is None

    def __hash__(self) -> int:
        return hash((FunctionType, id(self.func_like), id(self.bound_object)))

    def size(self) -> int:
        raise RuntimeError("FunctionType has no size")

    def align(self) -> int:
        raise RuntimeError("FunctionType has no align")


class Node:
    """
    Base class for all nodes in the HIR. A node could be a value, a reference, or a statement.
    Nodes equality is based on their identity.
    """
    span: Optional[Span]

    def __init__(self, span: Optional[Span] = None) -> None:
        self.span = None

    def __eq__(self, value: object) -> bool:
        return value is self

    def __hash__(self) -> int:
        return id(self)


NodeT = typing.TypeVar("NodeT", bound=Node)


class BasicBlock(Node):
    nodes: List[Node]
    terminated: bool

    def __init__(self, span: Optional[Span] = None) -> None:
        self.nodes = []
        self.terminated = False
        self.span = span

    def append(self, node: NodeT) -> NodeT:
        if isinstance(node, Terminator):
            assert not self.terminated
            self.terminated = True
        self.nodes.append(node)
        return node


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


class SymbolicConstant(Value):
    generic: GenericParameter

    def __init__(
        self, generic: GenericParameter, type: Optional[Type] = None, span: Optional[Span] = None
    ) -> None:
        super().__init__(type, span)
        self.generic = generic


class ParameterSemantic(Enum):
    BYVAL = auto()
    BYREF = auto()


class Var(TypedNode):
    name: str
    semantic: ParameterSemantic

    def __init__(
        self, name: str, type: Optional[Type], span: Optional[Span], semantic: ParameterSemantic = ParameterSemantic.BYVAL
    ) -> None:
        assert not isinstance(type, RefType)
        super().__init__(type, span)
        self.name = name
        self.semantic = semantic


class VarRef(Value):
    var: Var

    def __init__(
        self, var: Var, span: Optional[Span]
    ) -> None:
        assert var.type is not None
        super().__init__(RefType(var.type), span)
        self.var = var


class Member(Value):
    base: Value
    field: str

    def __init__(self, base: Value, field: str, type: Type, span: Optional[Span]) -> None:
        super().__init__(type, span)
        self.base = base
        self.field = field


class Index(Value):
    base: Value
    index: Value

    def __init__(self, base: Value, index: Value, type: Type, span: Optional[Span]) -> None:
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

    def __init__(self, value: Any, type: Type | None = None, span: Optional[Span] = None) -> None:
        super().__init__(type, span)
        self.value = value

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Constant) and type(value.value) == type(self.value) and value.value == self.value

    def __hash__(self) -> int:
        return hash((Constant, self.value))


class TypeValue(Value):
    def __init__(self, ty: Type, span: Optional[Span] = None) -> None:
        super().__init__(TypeConstructorType(ty), span)

    def inner_type(self) -> Type:
        assert isinstance(self.type, TypeConstructorType)
        return self.type.inner


class FunctionValue(Value):
    def __init__(self, ty: FunctionType, span: Optional[Span] = None) -> None:
        super().__init__(ty, span)


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

    def __init__(self, args: List[Value], type: Type, span: Optional[Span] = None) -> None:
        super().__init__(type, span)
        self.args = args


class Intrinsic(Value):
    name: str
    args: List[Value]

    def __init__(self, name: str, args: List[Value], type: Type, span: Optional[Span] = None) -> None:
        super().__init__(type, span)
        self.name = name
        self.args = args

    def __str__(self) -> str:
        return f'Intrinsic({self.name}, {self.args})'

    def __repr__(self) -> str:
        return f'Intrinsic({self.name}, {self.args})'


class Call(Value):
    op: "Function"
    """After type inference, op should be a Value."""

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


class TemplateMatchingError(Exception):
    span: Span | None
    message: str

    def __init__(self, node: Node | Span | None, message: str) -> None:
        if node is not None:
            if isinstance(node, Node):
                self.span = node.span
            else:
                self.span = node
        else:
            self.span = None
        self.message = message

    def __str__(self) -> str:
        if self.span is None:
            return f"Template matching error:\n\t{self.message}"
        return f"Template matching error at {self.span}:\n\t{self.message}"


class SpannedError(Exception):
    span: Span | None
    message: str

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


class ParsingError(SpannedError):
    def __str__(self) -> str:
        if self.span is None:
            return f"Parsing error:\n\t{self.message}"
        return f"Parsing error at {self.span}:\n\t{self.message}"


class InlineError(SpannedError):
    def __str__(self) -> str:
        if self.span is None:
            return f"Inline error:\n\t{self.message}"
        return f"Inline error at {self.span}:\n\t{self.message}"


class TypeInferenceError(SpannedError):
    def __str__(self) -> str:
        if self.span is None:
            return f"Type inference error:\n\t{self.message}"
        return f"Type inference error at {self.span}:\n\t{self.message}"


class Assign(Node):
    ref: Value
    value: Value

    def __init__(self, ref: Value, value: Value, span: Optional[Span] = None) -> None:
        assert not isinstance(value.type, (FunctionType, TypeConstructorType))
        if not isinstance(ref.type, RefType):
            raise ParsingError(
                ref, f"cannot assign to a non-reference variable")
        super().__init__(span)
        self.ref = ref
        self.value = value


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

    def __init__(self, start: Value, stop: Value, step: Value, span: Optional[Span] = None) -> None:
        super().__init__(None, span)
        self.start = start
        self.stop = stop
        self.step = step

    def value_type(self) -> Type:
        types = [self.start.type, self.stop.type, self.step.type]
        for ty in types:
            if not isinstance(ty, GenericIntType):
                return unwrap(ty)
        return unwrap(types[0])


class ComptimeValue:
    value: Any
    update_func: Optional[Callable[[Any], None]]

    def __init__(self, value: Any, update_func: Callable[[Any], None] | None) -> None:
        self.value = value
        self.update_func = update_func

    def update(self, value: Any) -> None:
        if self.update_func is not None:
            self.update_func(value)
        else:
            raise RuntimeError("unable to update comptime value")

    def __str__(self) -> str:
        return f"ComptimeValue({self.value})"


class FunctionSignature:
    params: List[Var]
    return_type: Type | None
    generic_params: List[GenericParameter]

    def __init__(self,  generic_params: List[GenericParameter], params: List[Var], return_type: Type | None) -> None:
        self.params = params
        self.return_type = return_type
        self.generic_params = generic_params


class Function:
    name: str
    params: List[Var]
    return_type: Type | None
    body: Optional[BasicBlock]
    export: bool
    locals: List[Var]
    complete: bool
    is_method: bool
    inline_hint: bool | Literal['always', 'never']

    def __init__(
        self,
        name: str,
        params: List[Var],
        return_type: Type | None,
        is_method: bool,
    ) -> None:
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = None
        self.export = False
        self.locals = []
        self.complete = False
        self.is_method = is_method
        self.inline_hint = False


def match_template_args(
        template: List[Tuple[str, Type]],
        args: List[Type]) -> Dict[GenericParameter, Type] | TypeInferenceError:
    mapping: Dict[GenericParameter, Type] = {}

    def unify(a: Type, b: Type):
        """
        Perform unification on two types or values, only a could contain generic parameters.
        """
        if a is b:
            return

        # unify type
        match a:
            case SymbolicType():
                if a.param.name in mapping:
                    return unify(mapping[a.param], b)
                if a.param.bound is None:
                    if isinstance(b, GenericFloatType) or isinstance(b, GenericIntType):
                        raise TypeInferenceError(None,
                                                 f"float/int literal cannot be used to infer generic type for `{a.param.name}` directly, wrap it with a concrete type")
                else:
                    if not a.param.bound.satisfied_by(b):
                        raise TypeInferenceError(
                            None, f"{b} does not satisfy bound {a.param.bound}")
                    if isinstance(a.param.bound, UnionBound):
                        for bound in a.param.bound.bounds:
                            if bound.satisfied_by(b) and bound.super_type.is_concrete():
                                mapping[a.param] = bound.super_type
                                return
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
                def do() -> None:
                    if not isinstance(b, TupleType):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
                    if len(a.elements) != len(b.elements):
                        raise TypeInferenceError(
                            None, f"expected {a}, got {b}")
                    for ea, eb in zip(a.elements, b.elements):
                        unify(ea, eb)
                do()
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
                def do() -> None:
                    if not isinstance(b, BoundType):
                        if isinstance(b, TypeConstructorType) and isinstance(a.generic.body, TypeConstructorType):
                            assert len(a.args) == 1
                            unify(a.args[0], b.inner)
                            return

                        raise TypeInferenceError(
                            None, f"{b} is not a BoundType")
                    if len(a.args) != len(b.args):
                        raise TypeInferenceError(
                            None, f"expected {len(a.args)} arguments, got {len(b.args)}")
                    for ea, eb in zip(a.args, b.args):
                        unify(ea, eb)
                    unify(a.generic.body, b.generic.body)
                do()
            case ParametricType():
                raise RuntimeError(
                    "ParametricType should not appear in match_template_args")
            case _:
                if not is_type_compatible_to(b, a):
                    raise TypeInferenceError(
                        None, f"expected {a}, got {b}")
        return False
    try:
        if len(template) != len(args):
            return TypeInferenceError(None, f"expected {len(template)} arguments, got {len(args)}")
        for i in range(len(template)):
            unify(template[i][1], args[i])
        return mapping
    except TypeInferenceError as e:
        return e


def match_func_template_args(sig: FunctionSignature, args: FunctionTemplateResolvingArgs) -> Dict[GenericParameter, Type] | TypeInferenceError:
    if len(sig.params) != len(args):
        return TypeInferenceError(
            None, f"expected {len(sig.params)} arguments, got {len(args)}")

    template_args: List[Tuple[str, Type]] = []
    for param in sig.params:
        assert param.type is not None
        template_args.append((param.name, param.type))
    matching_args = [arg[1] for arg in args]
    return match_template_args(template_args, matching_args)


_global_context: Optional["GlobalContext"] = None


class GlobalContext:
    types: Dict[type, Type]
    functions: Dict[Callable[..., Any], FunctionTemplate]

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
    if ty == target or isinstance(ty, AnyType):
        return True
    if isinstance(ty, RefType):
        return is_type_compatible_to(ty.element, target)
    if isinstance(target, FloatType):
        return isinstance(ty, GenericFloatType)
    if isinstance(target, IntType):
        return isinstance(ty, GenericIntType)
    return False


class FunctionInliner:
    mapping: Dict[Var | Value, Value]
    ret: Value | None

    def __init__(self, func: Function, args: List[Value], body: BasicBlock, span: Optional[Span] = None) -> None:
        self.mapping = {}
        self.ret = None
        for param, arg in zip(func.params, args):
            self.mapping[param] = arg
        assert func.body
        self.do_inline(func.body, body)

    def do_inline(self, func_body: BasicBlock, body: BasicBlock) -> None:
        for node in func_body.nodes:
            assert node not in self.mapping

            match node:
                case Var():
                    assert node.type
                    assert node.semantic == ParameterSemantic.BYVAL
                    self.mapping[node] = Alloca(node.type, node.span)
                case Load():
                    mapped_var = self.mapping[node.ref]
                    if isinstance(node.ref.type, RefType) and isinstance(mapped_var, Value):
                        self.mapping[node] = mapped_var
                    else:
                        assert isinstance(mapped_var.type, RefType)
                        self.mapping[node] = body.append(Load(mapped_var))
                case Index():
                    base = self.mapping.get(node.base)
                    assert isinstance(base, Value)
                    index = self.mapping.get(node.index)
                    assert isinstance(index, Value)
                    assert node.type
                    self.mapping[node] = body.append(
                        Index(base, index, node.type, node.span))
                case Member():
                    base = self.mapping.get(node.base)
                    assert isinstance(base, Value)
                    assert node.type
                    self.mapping[node] = body.append(Member(
                        base, node.field, node.type, node.span))
                case Call() as call:
                    def do():
                        args: List[Value] = []
                        for arg in call.args:
                            mapped_arg = self.mapping.get(arg)
                            if mapped_arg is None:
                                raise InlineError(
                                    node, "unable to inline call")
                            args.append(mapped_arg)
                        assert call.type
                        self.mapping[call] = body.append(
                            Call(call.op, args, call.type, node.span))
                    do()
                case Intrinsic() as intrin:
                    def do():
                        args: List[Value] = []
                        for arg in intrin.args:
                            mapped_arg = self.mapping.get(arg)
                            if mapped_arg is None:
                                raise InlineError(
                                    node, "unable to inline intrinsic")
                            args.append(mapped_arg)
                        assert intrin.type
                        self.mapping[intrin] = body.append(
                            Intrinsic(intrin.name, args, intrin.type, node.span))
                    do()
                case Return():
                    if self.ret is not None:
                        raise InlineError(node, "multiple return statement")
                    assert node.value is not None
                    mapped_value = self.mapping.get(node.value)
                    if mapped_value is None:
                        raise InlineError(node, "unable to inline return")
                    self.ret = mapped_value
                case _:
                    raise ParsingError(node, f"invalid node {
                                       node} for inlining")

    @staticmethod
    def inline(func: Function, args: List[Value], body: BasicBlock, span: Optional[Span] = None) -> Value:
        inliner = FunctionInliner(func, args, body, span)
        assert inliner.ret
        return inliner.ret


def register_dsl_type_alias(target: type, alias: type):
    """
    Allow a type to be remapped to another type within DSL code.
    Parameters:
    target (type): The type to be remapped.
    alias (type): The type to which the target type will be remapped.
    Example:

    For example, 
    ```python
    @lc.struct
    class Foo:
        x: int
        y: int

    class SomeOtherFoo:
        components: List[int]

    register_dsl_type_alias(SomeOtherFoo, Foo)

    @lc.func
    def foo(f: SomeOtherFoo): # SomeOtherFoo is interpreted as Foo
        ...

    ```
    """
    ctx = GlobalContext.get()
    alias_ty = get_dsl_type(alias)
    assert alias_ty, f"alias type {alias} is not a DSL type"
    ctx.types[target] = alias_ty
