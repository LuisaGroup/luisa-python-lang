"""
Runtime support for DSL
"""

from abc import abstractmethod
import typing

from luisa_lang.utils import IdentityDict, is_generic_class
import luisa_lang.hir as hir
from hir import PyTreeStructure
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Union, cast


class Scope:
    parent: Optional["Scope"]
    bb: hir.BasicBlock
    local_refs: Dict[str, hir.Var]

    def __init__(self, parent: Optional["Scope"], span: Optional[hir.Span] = None):
        self.parent = parent
        self.bb = hir.BasicBlock(span)
        self.local_refs = {}

    def is_local_ref_defined(self, name: str) -> bool:
        if name in self.local_refs:
            return True
        if self.parent is not None:
            return self.parent.is_local_ref_defined(name)
        return False


# class PyVarRecord:
#     obj: Optional['JitVar']
#     ty: hir.Type

#     def __init__(self, obj: Optional['JitVar'], ty: hir.Type):
#         self.obj = obj
#         self.ty = ty


class FuncTracer:
    py_locals: Dict[str, Union["JitVar", object]]
    locals: List[hir.Var]
    params: List[hir.Var]
    scopes: List[Scope]
    ret_type: hir.Type | None
    func_globals: Dict[str, Any]
    name: str

    def __init__(self, name:str, func_globals: Dict[str, Any]):
        self.locals = []
        self.py_locals = {}
        self.params = []
        self.scopes = [Scope(None)]
        self.ret_type = None
        self.func_globals = func_globals
        self.name = name

    def push_scope(self) -> Scope:
        self.scopes.append(Scope(self.scopes[-1]))
        return self.scopes[-1]

    def pop_scope(self) -> Scope:
        return self.scopes.pop()

    def create_var(self, name: str, ty: hir.Type, is_param: bool) -> hir.Var:
        if self.scopes[-1].is_local_ref_defined(name):
            raise ValueError(f"Local reference {name} already defined in current scope")
        if name in self.py_locals:
            raise ValueError(f"Variable {name} already defined in current function")
        var = hir.Var(name, ty, None, hir.ParameterSemantic.BYVAL)
        self.locals.append(var)
        if is_param:
            self.params.append(var)
        return var


    def add_py_var(self, name: str, obj: object):
        assert not isinstance(obj, JitVar)
        if name in self.py_locals:
            raise ValueError(f"Variable {name} already defined in current function")
        self.py_locals[name] = obj

    def get_var(self, key: str) -> Any:
        if key in self.py_locals:
            return self.py_locals[key]
        else:
            if key in self.func_globals:
                # TODO: validate return values
                return self.func_globals[key]
            else:
                raise ValueError(f"Variable {key} not found in current function")

    def set_var(self, key: str, value: Any) -> None:
        if key not in self.py_locals:
            if key in self.func_globals:
                assert not isinstance(
                    value, JitVar
                ), "attempting to assign DSL variable to global variable"
                self.func_globals[key] = value
                return
            if not isinstance(value, JitVar):
                self.py_locals[key] = value
                return
            else:
                ty = type(value)
                ir_ty = value._symbolic_type()
                ir_var = self.create_var(key, ir_ty, False)
                var = ty.from_hir_node(hir.VarRef(ir_var))
                self.py_locals[key] = var
        local = self.py_locals[key]
        if isinstance(local, JitVar):
            assert isinstance(
                value, JitVar
            ), "Attempting to assign normal python value to DSL variable"
            assign(local, value)
        else:
            self.py_locals[key] = value

    def check_return_type(self, ty:hir.Type):
        if self.ret_type is None:
            self.ret_type = ty
        else:
            if not self.ret_type != ty:
                raise ValueError(
                    f"Return type mismatch: expected {self.ret_type}, got {ty}"
                )

    def cur_bb(self) -> hir.BasicBlock:
        return self.scopes[-1].bb

    def finalize(self) -> hir.Function:
        assert len(self.scopes) == 1
        entry_bb = self.scopes[0].bb
        assert self.ret_type is not None
        return hir.Function(self.name, self.params, self.locals, entry_bb, self.ret_type)


FUNC_STACK: List[FuncTracer] = []


def current_func() -> FuncTracer:
    """
    Get the current function tracer
    """
    return FUNC_STACK[-1]


def push_to_current_bb[T: hir.Node](node: T) -> T:
    return current_func().cur_bb().append(node)


class Symbolic:
    node: hir.Value
    scope: Scope

    def __init__(self, node: hir.Value, scope: Scope | None = None):
        self.node = node
        if scope is None:
            self.scope = current_func().scopes[-1]
        else:
            self.scope = scope


class FlattenedTree:
    metadata: Tuple[type, Tuple[Any], Any]  # (type, type_args, Any)
    children: List["FlattenedTree"]

    def __init__(
        self, metadata: Tuple[type, Tuple[Any], Any], children: List["FlattenedTree"]
    ):
        self.metadata = metadata
        self.children = children

    @staticmethod
    def equivalence(a: "FlattenedTree", b: "FlattenedTree") -> bool:
        typ_a = a.metadata[0]
        typ_b = b.metadata[0]
        if typ_a != typ_b:
            return False
        if isinstance(typ_a, JitVar):
            assert len(a.children) == 0
            assert len(b.children) == 0
            return True
        if len(a.children) != len(b.children):
            return False
        if a.metadata[1] != b.metadata[1]:
            return False
        for i in range(len(a.children)):
            if not FlattenedTree.equivalence(a.children[i], b.children[i]):
                return False
        return True

    def structure(self) -> hir.PyTreeStructure:
        typ = self.metadata[0]
        if issubclass(typ, JitVar):
            assert len(self.children) == 0
            node = self.metadata[2]
            assert isinstance(node, JitVar)
            return hir.PyTreeStructure((typ, self.metadata[1], node._symbolic_type()))
        else:
            children = [c.structure() for c in self.children]
            return hir.PyTreeStructure(
                (typ, self.metadata[1], self.metadata[2]), children
            )
        
    def collect_jitvars(self) -> List['JitVar']:
        """
        Collect all JitVar instances from the flattened tree
        """
        jit_vars = []
        if issubclass(self.metadata[0], JitVar):
            assert len(self.children) == 0
            jit_vars.append(self.metadata[2])
        else:
            for child in self.children:
                jit_vars.extend(child.collect_jitvars())
        return jit_vars

    @staticmethod
    def unstructure(
        s: PyTreeStructure, mapping: IdentityDict[hir.PyTreeStructure, "JitVar"]
    ) -> "FlattenedTree":
        assert s.metadata is not None
        if s in mapping:
            v = mapping[s]

            typ, type_args, _ = s.metadata
            return FlattenedTree((typ, type_args, v), [])
        else:
            typ, type_args, other = s.metadata
            assert not issubclass(typ, JitVar)
            children = [FlattenedTree.unstructure(c, mapping) for c in s.children]
            return FlattenedTree((typ, type_args, other), children)


class PyTree:
    """
    A pytree is a tree-like container for both DSL and non-DSL objects.
    """

    @abstractmethod
    def _flatten(self) -> FlattenedTree:
        """
        Flatten the pytree into a tree of DSL objects
        """
        pass

    @classmethod
    def _unflatten(cls, tree: FlattenedTree) -> "PyTree":
        """
        Unflatten the pytree from a tree of DSL objects
        """
        raise NotImplementedError(
            f"Unflattening not implemented for {cls.__name__}. Please implement _unflatten method in the class."
        )


class JitVar:
    """
    The base class for all dsl types. Each dsl variable can either store a symbolic representation or the actual value
    """

    __symbolic__: Optional[Symbolic]
    dtype: type[Any]

    def __init__(self, dtype:type[Any]):
        """
        Zero-initialize a variable with given data type
        """
        self.dtype = dtype
        if is_jit():
            self._init_symbolic()
        else:
            self.__symbolic__ = None

    def _type_args(self) -> Tuple[Any, ...]:
        # self.__orig_class__.__args__
        if hasattr(self, "__orig_class__"):
            return tuple(getattr(self, "__orig_class__").__args__)
        return tuple()

    def _init_symbolic(self):
        dsl_type = hir.get_dsl_type(self.dtype)
        if dsl_type is None:
            raise ValueError(f"{self.dtype} is not a valid DSL type")
        self.__symbolic__ = Symbolic(
            hir.VarRef(current_func().create_var("", dsl_type.default(), False))
        )

    def _destroy_symbolic(self):
        self.__symbolic__ = None

    def _symbolic_type(self) -> hir.Type:
        # TODO: check _type_args
        return hir.get_dsl_type(self.dtype).default()

    @classmethod
    def from_hir_node[T: JitVar](cls: type[T], node: hir.Value) -> T:
        """
        Create a variable directly from a typed HIR node
        """
        instance = cls.__new__(cls)
        instance.__symbolic__ = Symbolic(node)
        instance.dtype = cls
        return instance

    def symbolic(self) -> Symbolic:
        """
        Retrieve the internal symbolic representation of the variable. This is used for internal DSL code generation.
        """
        assert (
            self.__symbolic__ is not None
        ), "Attempting to access symbolic representation of a non-symbolic variable"
        return self.__symbolic__

    def is_symbolic(self) -> bool:
        """
        Check if the variable is symbolic
        """
        return self.__symbolic__ is not None


type PyTreeFlattenFunc = Callable[[Any], FlattenedTree]
type PyTreeUnflattenFunc = Callable[[FlattenedTree], Any]


def tree_flatten(obj: Any, allow_non_pytree_objects: bool) -> FlattenedTree:
    if isinstance(obj, JitVar):
        return FlattenedTree((type(obj), obj._type_args(), obj), [])
    if isinstance(obj, PyTree):
        return obj._flatten()
    if allow_non_pytree_objects and not PyTreeRegistry.is_registered(type(obj)):
        return FlattenedTree((type(obj), tuple(), obj), [])
    flatten_func, _ = PyTreeRegistry.get(type(obj))
    return flatten_func(obj)


def tree_unflatten(obj: FlattenedTree, allow_non_pytree_objects: bool) -> Any:
    typ = obj.metadata[0]
    if issubclass(typ, JitVar):
        _type_args, v = obj.metadata[1:]
        assert isinstance(v, JitVar)
        return v
    if issubclass(typ, PyTree):
        return typ._unflatten(obj)
    if allow_non_pytree_objects and not PyTreeRegistry.is_registered(typ):
        return typ(obj.metadata[1])
    _, unflatten_func = PyTreeRegistry.get(typ)
    return unflatten_func(obj)


class PyTreeRegistry:
    """
    A registry for pytree that are not subclassed from PyTree
    """

    funcs: Dict[type, Tuple[PyTreeFlattenFunc, PyTreeUnflattenFunc]]

    _instance: Optional["PyTreeRegistry"] = None

    @classmethod
    def instance(cls) -> "PyTreeRegistry":
        if cls._instance is None:
            cls._instance = cls()
            cls.__register_default_types()
        return cls._instance

    def __init__(self):
        self.funcs = {}

    @staticmethod
    def register(
        typ: type, flatten_func: PyTreeFlattenFunc, unflatten_func: PyTreeUnflattenFunc
    ) -> None:
        """
        Register a PyTree type with its flatten and unflatten functions.
        """
        PyTreeRegistry.instance().funcs[typ] = (flatten_func, unflatten_func)

    @staticmethod
    def get(typ: type) -> Tuple[PyTreeFlattenFunc, PyTreeUnflattenFunc]:
        """
        Get the flatten and unflatten functions for a PyTree type.
        """
        funcs = PyTreeRegistry.instance().funcs.get(typ)
        if funcs is None:
            raise ValueError(f"No flatten/unflatten functions registered for {typ}")
        return funcs

    @staticmethod
    def is_registered(typ: type) -> bool:
        """
        Check if a PyTree type is registered.
        """
        return typ in PyTreeRegistry.instance().funcs

    @staticmethod
    def __register_default_types() -> None:
        def flatten_primitive(obj: Any) -> FlattenedTree:
            return FlattenedTree((type(obj), tuple(), obj), [])

        def unflatten_primitive(tree: FlattenedTree) -> Any:
            assert len(tree.children) == 0
            return tree.metadata[1]

        PyTreeRegistry.register(int, flatten_primitive, unflatten_primitive)
        PyTreeRegistry.register(float, flatten_primitive, unflatten_primitive)
        PyTreeRegistry.register(str, flatten_primitive, unflatten_primitive)
        PyTreeRegistry.register(bool, flatten_primitive, unflatten_primitive)
        PyTreeRegistry.register(type(None), flatten_primitive, unflatten_primitive)

        def flatten_list(obj: List[Any]) -> FlattenedTree:
            return FlattenedTree(
                (list, tuple(), None), [tree_flatten(o, True) for o in obj]
            )

        def unflatten_list(tree: FlattenedTree) -> List[Any]:
            assert tree.metadata[0] is list
            assert len(tree.children) == tree.metadata[1]
            return [tree_unflatten(c, True) for c in tree.children]

        PyTreeRegistry.register(list, flatten_list, unflatten_list)

        def flatten_tuple(obj: Tuple[Any, ...]) -> FlattenedTree:
            return FlattenedTree(
                (tuple, tuple(), None), [tree_flatten(o, True) for o in obj]
            )

        def unflatten_tuple(tree: FlattenedTree) -> Tuple[Any, ...]:
            assert tree.metadata[0] is tuple
            assert len(tree.children) == tree.metadata[1]
            return tuple(tree_unflatten(c, True) for c in tree.children)

        PyTreeRegistry.register(tuple, flatten_tuple, unflatten_tuple)

        def flatten_dict(obj: Dict[Any, Any]) -> FlattenedTree:
            return FlattenedTree(
                (dict, tuple(), (len(obj.keys()))),
                [tree_flatten(k, True) for k in obj.keys()]
                + [tree_flatten(v, True) for v in obj.values()],
            )

        def unflatten_dict(tree: FlattenedTree) -> Dict[Any, Any]:
            assert tree.metadata[0] is dict
            length = tree.metadata[1]
            assert len(tree.children) == length * 2
            keys = tree.children[:length]
            values = tree.children[length:]
            return {
                tree_unflatten(k, True): tree_unflatten(v, True)
                for k, v in zip(keys, values)
            }

        PyTreeRegistry.register(dict, flatten_dict, unflatten_dict)


def create_constant_node(value: Any, dtype: hir.Type) -> hir.Constant:
    """
    Create a constant node given a python value
    """
    return push_to_current_bb(hir.Constant(value, dtype))


def type_of(value: type) -> hir.Type:
    return hir.get_dsl_type(value).default()


def create_intrinsic_node[T: JitVar](
    name: str, ret_type: type[T] | None, *args
) -> hir.Value:
    """
    Call an intrinsic function
    """
    nodes: List[hir.Value] = []
    for i, a in enumerate(args):
        if isinstance(a, JitVar):
            nodes.append(a.symbolic().node)
        elif isinstance(a, hir.Value):
            nodes.append(a)
        else:
            raise ValueError(f"Argument {i} is not a valid DSL variable or HIR node")
    if ret_type is not None:
        ret_dsl_type = hir.get_dsl_type(ret_type).default()
        if ret_dsl_type is None:
            raise ValueError(f"{ret_type} is not a valid DSL type")
    else:
        ret_dsl_type = hir.UnitType()
    return push_to_current_bb(hir.Intrinsic(name, nodes, ret_dsl_type))


def __intrinsic__[T](name: str, ret_type: type[T], *args) -> T:
    """
    Call an intrinsic function
    """
    assert issubclass(
        ret_type, JitVar
    ), f"Return type {ret_type} is not a valid DSL type"
    return cast(T, ret_type.from_hir_node(create_intrinsic_node(name, ret_type, *args)))


def assign(dst: Any, src: Any) -> None:
    """
    Assign the value of `src` to `dst`
    """
    assert isinstance(dst, JitVar), "dst is not a DSL variable"
    assert isinstance(
        src, JitVar
    ), "Attempting to assign normal python value to DSL variable"
    push_to_current_bb(hir.Assign(dst.symbolic().node, src.symbolic().node))


def is_jit() -> bool:
    """
    Check if current context is during DSL JIT compilation
    """
    return FUNC_STACK != []


def is_dsl_var(obj: Any) -> bool:
    """
    Check if the object is a DSL variable
    """
    return isinstance(obj, JitVar)


def current_span() -> hir.Span | None:
    return None


class ControlFlowFrame:
    parent: Optional["ControlFlowFrame"]
    is_static: bool

    def __init__(self, parent: Optional["ControlFlowFrame"]):
        self.parent = parent
        self.is_static = False


class IfFrame(ControlFlowFrame):
    static_cond: Optional[bool]

    def __init__(self, parent: ControlFlowFrame, cond: Any):
        super().__init__(parent)
        self.cond = cond
        self.is_static = not isinstance(cond, JitVar)
        self.static_cond = bool(cond) if self.is_static else None

    def true_active(self) -> bool:
        if self.is_static:
            assert self.static_cond is not None
            return self.static_cond
        return True

    def false_active(self) -> bool:
        if self.is_static:
            assert self.static_cond is not None
            return not self.static_cond
        return True


class ControlFrameGuard[T: ControlFlowFrame]:
    cf_type: type[T]
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    cf_frame: T
    ctx: "TraceContext"

    def __init__(self, ctx: "TraceContext", cf_type: type[T], *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.cf_type = cf_type
        self.cf_frame = self.cf_type(*self.args, **self.kwargs, parent=ctx.cf_frame)
        self.ctx = ctx

    def __enter__(self) -> T:
        self.ctx.cf_frame = self.cf_frame
        return self.cf_frame

    def __exit__(self, exc_type, exc_val, exc_tb):
        parent = self.ctx.cf_frame.parent
        assert parent is not None
        self.ctx.cf_frame = parent


UNARY_OP_TO_METHOD_NAMES: Dict[str, str] = {
    "UAdd": "__pos__",
    "USub": "__neg__",
    "Not": "__not__",
    "Invert": "__invert__",
}

AUG_ASSIGN_TO_METHOD_NAMES: Dict[str, str] = {
    "Add": "__iadd__",
    "Sub": "__isub__",
    "Mult": "__imul__",
    "Div": "__idiv__",
    "FloorDiv": "__ifloordiv__",
    "Mod": "__imod__",
    "Pow": "__ipow__",
    "LShift": "__ilshift__",
    "RShift": "__irshift__",
    "BitAnd": "__iand__",
    "BitOr": "__ior__",
    "BitXor": "__ixor__",
}

BINOP_TO_METHOD_NAMES: Dict[str, List[str]] = {
    "Add": ["__add__", "__radd__"],
    "Sub": ["__sub__", "__rsub__"],
    "Mult": ["__mul__", "__rmul__"],
    "Div": ["__truediv__", "__rtruediv__"],
    "FloorDiv": ["__floordiv__", "__rfloordiv__"],
    "Mod": ["__mod__", "__rmod__"],
    "Eq": ["__eq__", "__eq__"],
    "NotEq": ["__ne__", "__ne__"],
    "Lt": ["__lt__", "__gt__"],
    "LtE": ["__le__", "__ge__"],
    "Gt": ["__gt__", "__lt__"],
    "GtE": ["__ge__", "__le__"],
    "BitAnd": ["__and__", "__rand__"],
    "BitOr": ["__or__", "__ror__"],
    "BitXor": ["__xor__", "__rxor__"],
    "LShift": ["__lshift__", "__rlshift__"],
    "RShift": ["__rshift__", "__rrshift__"],
    "Pow": ["__pow__", "__rpow__"],
}


class TraceContext:
    cf_frame: ControlFlowFrame
    is_top_level: bool
    top_level_func: Optional[hir.Function]

    def __init__(self, is_top_level):
        self.cf_frame = ControlFlowFrame(None)
        self.is_top_level = is_top_level
        self.top_level_func = None

    def is_parent_static(self) -> bool:
        return self.cf_frame.is_static

    def if_(self, cond: Any) -> ControlFrameGuard[IfFrame]:
        return ControlFrameGuard(self, IfFrame, cond)

    def return_(self, expr: JitVar) -> None:
        """
        Return a value from the current function
        """
        ty = expr._symbolic_type()
        current_func().check_return_type(ty)
        push_to_current_bb(hir.Return(expr.symbolic().node))

    def redirect_binary(self, op, x, y):
        print(op, x, y)
        op, rop = BINOP_TO_METHOD_NAMES[op]
        if hasattr(x, op):
            return getattr(x, op)(y, __lc_ctx__=self)
        elif hasattr(y, rop):
            return getattr(y, rop)(x, __lc_ctx__=self)
        else:
            raise ValueError(
                f"Binary operation {op} not supported for {type(x)} and {type(y)}"
            )

    def redirect_call(self, f, *args, **kwargs):
        return f(*args, **kwargs, __lc_ctx__=self) # TODO: shoould not always pass self

    def intrinsic(self, f, *args, **kwargs):
        return __intrinsic__(f, *args, **kwargs)

    def decl_arg(self, name: str, arg: Any):
        func = current_func()
        func.py_locals[name] = arg

        # if isinstance(arg, JitVar):
        #     # ty = type(arg)
        #     # ir_ty = arg._symbolic_type()
        #     # ir_var = func.create_var(name, ir_ty, True)
        #     # var = ty.from_hir_node(hir.VarRef(ir_var))
        #     func.py_locals[name] = arg
        # else:
        #     func.py_locals[name] = arg

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Assign a value to a local variable
        """
        func = current_func()
        func.set_var(key, value)

    def __getitem__(self, key: str) -> Union["JitVar", object]:
        """
        Retrieve a value from a local variable
        """
        return current_func().get_var(key)


def _encode_func_args(
    args: hir.FunctionTemplateArgs,
) -> Tuple[List[Any], Dict[str, Any], List[JitVar]]:
    jit_vars: List[JitVar] = []
    args_list: List[Any] = []
    kwargs_dict: Dict[str, Any] = {}
    mapping: IdentityDict[hir.PyTreeStructure, JitVar] = IdentityDict()

    def create_var(name: str, v: hir.PyTreeStructure):
        assert v.metadata
        typ = v.metadata[0]
        if issubclass(typ, JitVar):
            assert len(v.children) == 0
            ir_type = v.metadata[2]
            assert isinstance(ir_type, hir.Type)
            ir_var = current_func().create_var(name, ir_type, True)
            jit_v = typ.from_hir_node(hir.VarRef(ir_var))
            jit_vars.append(jit_v)
            mapping[v] = jit_v
        else:
            for i, c in enumerate(v.children):
                create_var(f"name_{i}", c)

    for i, a in enumerate(args.args):
        create_var(f"__arg_{i}", a)

    for k, v in args.kwargs.items():
        create_var(k, v)

    for a in args.args:
        args_list.append(tree_unflatten(FlattenedTree.unstructure(a, mapping), False))

    for k, v in args.kwargs.items():
        kwargs_dict[k] = tree_unflatten(FlattenedTree.unstructure(v, mapping), False)

    return args_list, kwargs_dict, jit_vars


def _invoke_function_tracer(
    f: Callable[..., Any], args: hir.FunctionTemplateArgs, globalns: Dict[str, Any]
) -> hir.Function:
    trace_ctx = TraceContext(False)

    # args is Type | object
    func_tracer = FuncTracer(f.__name__.replace('.','_'), globalns)
    FUNC_STACK.append(func_tracer)
    try:
        args_vars, kwargs_vars, jit_vars = _encode_func_args(args)
        ret = f(*args_vars, **kwargs_vars, __lc_ctx__=trace_ctx)
        assert ret is None
        return func_tracer.finalize()
    finally:
        FUNC_STACK.pop()


class KernelTracer:
    top_level_tracer: FuncTracer

    def __init__(self, func_globals: Dict[str, Any]):
        self.top_level_tracer = FuncTracer('__kernel__', func_globals)

    def __enter__(self) -> FuncTracer:
        FUNC_STACK.append(self.top_level_tracer)
        return self.top_level_tracer

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert FUNC_STACK.pop() is self.top_level_tracer
        assert len(FUNC_STACK) == 0


__all__: List[str] = [
    "JitVar",
    "is_jit",
    "TraceContext",
    "KernelTracer",
    "PyTreeStructure",
]
