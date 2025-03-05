"""
Runtime support for DSL
"""

import luisa_lang.hir as hir
from typing import Any, Dict, List, Optional, cast


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
    scopes: List[Scope]

    def push_scope(self) -> Scope:
        self.scopes.append(Scope(self.scopes[-1]))
        return self.scopes[-1]

    def pop_scope(self) -> Scope:
        return self.scopes.pop()

    def create_var(self, name: str, ty: hir.Type | None) -> hir.Value:
        if name != '':
            if self.scopes[-1].is_local_ref_defined(name):
                raise ValueError(
                    f'Variable {name} already defined in current scope')
            if name in self.locals:
                raise ValueError(
                    f'Variable {name} already defined in current function')
        var = hir.Var(name, ty, None, hir.ParameterSemantic.BYVAL)
        self.locals[name] = var
        return hir.VarRef(var, None)

    def cur_bb(self) -> hir.BasicBlock:
        return self.scopes[-1].bb


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


class Var:
    """
    The base class for all dsl types. Each dsl variable can either store a symbolic representation or the actual value
    """
    __symbolic__: Optional[Symbolic]

    def __init__(self, dtype=type[Any]):
        """
        Zero-initialize a variable with given data type
        """
        dsl_type = hir.get_dsl_type(dtype)
        if dsl_type is None:
            raise ValueError(f'{dtype} is not a valid DSL type')
        self.__symbolic__ = Symbolic(
            current_func().create_var('', dsl_type.default()))

    @classmethod
    def from_hir_node[T:Var](cls: type[T], node: hir.Value) -> T:
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


def intrinsic[T:Var](name: str, ret_type: type[T] | None, *args) -> hir.Value:
    """
    Call an intrinsic function
    """
    nodes: List[hir.Value] = []
    for i, a in enumerate(args):
        if isinstance(a, Var):
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


def assign(dst: Var, src: Var) -> None:
    """
    Assign the value of `src` to `dst`
    """
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
    return isinstance(obj, Var)


def current_span() -> hir.Span | None:
    return None



class TraceContext:
    pass

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


__all__: List[str] = [
    'Var',
    'is_jit',
    'TraceContext',
    'intrinsic',
]
