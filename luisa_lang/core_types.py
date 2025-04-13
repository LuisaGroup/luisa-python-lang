import luisa_lang.hir as hir
from luisa_lang.lang_runtime import assign, current_span, intrinsic, Var, push_to_current_bb
import typing
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeAlias,
    TypeVar,
    Union,
    Generic,
    Literal,
    overload,
    Any,
)

class Ref[T:Var](Var):
    value_type: type[T]

    def __init__(self, value: T):
        self.value_type = type(value)
        value_node = value.symbolic().node
        if not isinstance(value_node, hir.Var):
            raise hir.TypeCheckError(
                current_span(), "cannot create a reference to a non-variable expression")
        self.symbolic().node = hir.VarRef(value_node, current_span())

    @property
    def value(self) -> T:
        return intrinsic("ref.read",  self.value_type, self.symbolic().node)

    @value.setter
    def value(self, value: T) -> None:
        assign(self.value, value)

