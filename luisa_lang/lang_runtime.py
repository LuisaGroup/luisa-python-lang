"""
Runtime support for DSL
"""

import luisa_lang.hir as hir
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, cast


class Scope:
    parent: Optional['Scope']
    bb: hir.BasicBlock
    local_refs: Dict[str, hir.Var]

    def __init__(self, parent: Optional['Scope'], span: Optional[hir.Span] = None):
        self.parent = parent
        self.bb = hir.BasicBlock(span)

    def is_local_ref_defined(self, name: str) -> bool:
        if name in self.local_refs:
            return True
        if self.parent is not None:
            return self.parent.is_local_ref_defined(name)
        return False


class FuncTracer:
    locals: Dict[str, hir.Var]
    params: List[hir.Var]
    scopes: List[Scope]
    ret_type: hir.Type | None

    def __init__(self):
        self.locals = {}
        self.params = []
        self.scopes = []
        self.ret_type = None

    def push_scope(self) -> Scope:
        self.scopes.append(Scope(self.scopes[-1]))
        return self.scopes[-1]

    def pop_scope(self) -> Scope:
        return self.scopes.pop()

    def add_param(self, name: str, ty: hir.Type) -> hir.Value:
        return self._create_var(name, ty, True)

    def create_var(self, name: str, ty: hir.Type | None) -> hir.Value:
        return self._create_var(name, ty, False)

    def _create_var(self, name: str, ty: hir.Type | None, is_param: bool) -> hir.Value:
        if name != '':
            if self.scopes[-1].is_local_ref_defined(name):
                raise ValueError(
                    f'Local reference {name} already defined in current scope')
            if name in self.locals:
                raise ValueError(
                    f'Variable {name} already defined in current function')
        var = hir.Var(name, ty, None, hir.ParameterSemantic.BYVAL)
        self.locals[name] = var
        if is_param:
            self.params.append(var)
        return hir.VarRef(var, None)

    def cur_bb(self) -> hir.BasicBlock:
        return self.scopes[-1].bb

    def finalize(self) -> hir.Function:
        assert len(self.scopes) == 1
        entry_bb = self.scopes[0].bb
        assert self.ret_type is not None
        return hir.Function(self.params, list(self.locals.values()), entry_bb, self.ret_type)


FUNC_STACK: List[FuncTracer] = []


def current_func() -> FuncTracer:
    """
    Get the current function tracer
    """
    return FUNC_STACK[-1]


def push_to_current_bb[T:hir.Node](node: T) -> T:
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


class JitVar:
    """
    The base class for all dsl types. Each dsl variable can either store a symbolic representation or the actual value
    """
    __symbolic__: Optional[Symbolic]
    dtype: type[Any]

    def __init__(self, dtype=type[Any]):
        """
        Zero-initialize a variable with given data type
        """
        self.dtype = dtype
        if is_jit():
            self._init_symbolic()
        else:
            self.__symbolic__ = None

    def _init_symbolic(self):
        dsl_type = hir.get_dsl_type(self.dtype)
        if dsl_type is None:
            raise ValueError(f'{self.dtype} is not a valid DSL type')
        self.__symbolic__ = Symbolic(
            current_func().create_var('', dsl_type.default()))

    def _destroy_symbolic(self):
        self.__symbolic__ = None

    def _symbolic_type(self) -> hir.Type:
        return hir.get_dsl_type(self.dtype).default()

    @classmethod
    def from_hir_node[T:JitVar](cls: type[T], node: hir.Value) -> T:
        """
        Create a variable directly from a typed HIR node
        """
        instance = cls.__new__(cls)
        instance.__symbolic__ = Symbolic(node)
        return instance

    def symbolic(self) -> Symbolic:
        """
        Retrieve the internal symbolic representation of the variable. This is used for internal DSL code generation.
        """
        assert self.__symbolic__ is not None, "Attempting to access symbolic representation of a non-symbolic variable"
        return self.__symbolic__

    def is_symbolic(self) -> bool:
        """
        Check if the variable is symbolic
        """
        return self.__symbolic__ is not None


def create_constant_node(value: Any, dtype: hir.Type) -> hir.Constant:
    """
    Create a constant node given a python value
    """
    return push_to_current_bb(hir.Constant(value, dtype))


def type_of(value: type) -> hir.Type:
    return hir.get_dsl_type(value).default()


def create_intrinsic_node[T:JitVar](name: str, ret_type: type[T] | None, *args) -> hir.Value:
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
            raise ValueError(
                f'Argument {i} is not a valid DSL variable or HIR node')
    if ret_type is not None:
        ret_dsl_type = hir.get_dsl_type(ret_type).default()
        if ret_dsl_type is None:
            raise ValueError(f'{ret_type} is not a valid DSL type')
    else:
        ret_dsl_type = hir.UnitType()
    return push_to_current_bb(
        hir.Intrinsic(name, nodes, ret_dsl_type))


def intrinsic[T](name: str, ret_type: type[T], *args) -> T:
    """
    Call an intrinsic function
    """
    assert issubclass(
        ret_type, JitVar), f"Return type {ret_type} is not a valid DSL type"
    return cast(T, ret_type.from_hir_node(create_intrinsic_node(name, ret_type, *args)))


def assign(dst: Any, src: Any) -> None:
    """
    Assign the value of `src` to `dst`
    """
    assert isinstance(dst, JitVar), "dst is not a DSL variable"
    assert isinstance(
        src, JitVar), "Attempting to assign normal python value to DSL variable"
    push_to_current_bb(hir.Assign(
        dst.symbolic().node, src.symbolic().node))


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
    parent: Optional['ControlFlowFrame']
    is_static: bool

    def __init__(self, parent: Optional['ControlFlowFrame']):
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


class ControlFrameGuard[T:ControlFlowFrame]:
    cf_type: type[T]
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    cf_frame: T
    ctx: 'TraceContext'

    def __init__(self, ctx: 'TraceContext', cf_type: type[T], *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.cf_type = cf_type
        self.cf_frame = self.cf_type(
            *self.args, **self.kwargs, parent=ctx.cf_frame)
        self.ctx = ctx

    def __enter__(self) -> T:
        self.ctx.cf_frame = self.cf_frame
        return self.cf_frame

    def __exit__(self, exc_type, exc_val, exc_tb):
        parent = self.ctx.cf_frame.parent
        assert parent is not None
        self.ctx.cf_frame = parent


class TraceContext:
    cf_frame: ControlFlowFrame

    def __init__(self):
        self.cf_frame = ControlFlowFrame(None)

    def is_parent_static(self) -> bool:
        return self.cf_frame.is_static

    def if_(self, cond: Any) -> ControlFrameGuard[IfFrame]:
        return ControlFrameGuard(self, IfFrame, cond)

    def return_(self, expr: JitVar) -> None:
        """
        Return a value from the current function
        """
        push_to_current_bb(hir.Return(expr.symbolic().node))

    def redirect_binary(self, op, x, y):
        print(op, x, y)
        raise NotImplementedError('TODO')
    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Assign a value to a local variable
        """
        func = current_func()
        raise NotImplementedError('TODO')
    
    def __getitem__(self, key: str) -> Any:
        """
        Retrieve a value from a local variable
        """
        raise NotImplementedError('TODO')


# def redirect_name_lookup(name: str) -> Any:
#     """
#     In DSL code, `name` is rewritten to `redirect_name_lookup(name)`
#     """
#     raise NotImplementedError('TODO')


# def redirect_assign(dst: Any, src: Any, expected_type: type | None = None) -> Any:
#     """
#     In DSL code, `dst = src` is rewritten to `dst = redirect_assign(dst, src)`
#     """
#     if isinstance(dst, Var):
#         assert isinstance(
#             src, Var), "Attempting to assign normal python value to DSL variable"
#         push_to_current_bb(hir.Assign(
#             dst.get_internal().node, src.get_internal().node))
#         return dst
#     else:
#         return src


# def redirect_aug_assign(dst: Any, method: str, src: Any) -> Any:
#     pass

def _invoke_function_tracer(mode: Literal['trace', 'func'], f: Callable[..., Any], args: List[JitVar | object], kwargs: Dict[str, JitVar | object]) -> Any:
    trace_ctx = TraceContext()
    if mode == 'func':
        func_tracer = FuncTracer()
        FUNC_STACK.append(func_tracer)
        try:
            ret = f(trace_ctx, *args, **kwargs)
            assert isinstance(ret, (JitVar, tuple))
            # TODO:
        finally:
            FUNC_STACK.pop()
    else:
        ret = f(trace_ctx, *args, **kwargs)
    return ret


class KernelTracer:
    top_level_tracer: FuncTracer

    def __init__(self):
        self.top_level_tracer = FuncTracer()

    def __enter__(self) -> FuncTracer:
        FUNC_STACK.append(self.top_level_tracer)
        return self.top_level_tracer

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert FUNC_STACK.pop() is self.top_level_tracer
        assert len(FUNC_STACK) == 0


__all__: List[str] = [
    'JitVar',
    'is_jit',
    'TraceContext',
    'intrinsic',
    'KernelTracer'
]
