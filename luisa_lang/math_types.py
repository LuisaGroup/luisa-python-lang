# fmt: off
import typing as tp
from luisa_lang._builtin_decor import _builtin, _builtin_type, _intrinsic_impl
from luisa_lang._classinfo import _register_class
import luisa_lang.hir as _hir
_ctx = _hir.GlobalContext.get()
_ctx.types[bool] = _hir.BoolType()
FLOAT_TYPES: tp.Final[tp.List[str]] = ["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
FloatType = tp.Union["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
_F = tp.TypeVar("_F")
_F1 = tp.TypeVar("_F1", "f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4")
class FloatBuiltin(tp.Generic[_F]):
    def abs(self: _F) -> _F: return _intrinsic_impl()
    def acos(self: _F) -> _F: return _intrinsic_impl()
    def acosh(self: _F) -> _F: return _intrinsic_impl()
    def asin(self: _F) -> _F: return _intrinsic_impl()
    def asinh(self: _F) -> _F: return _intrinsic_impl()
    def atan(self: _F) -> _F: return _intrinsic_impl()
    def atanh(self: _F) -> _F: return _intrinsic_impl()
    def ceil(self: _F) -> _F: return _intrinsic_impl()
    def cos(self: _F) -> _F: return _intrinsic_impl()
    def cosh(self: _F) -> _F: return _intrinsic_impl()
    def exp(self: _F) -> _F: return _intrinsic_impl()
    def floor(self: _F) -> _F: return _intrinsic_impl()
    def log(self: _F) -> _F: return _intrinsic_impl()
    def log10(self: _F) -> _F: return _intrinsic_impl()
    def log2(self: _F) -> _F: return _intrinsic_impl()
    def sin(self: _F) -> _F: return _intrinsic_impl()
    def sinh(self: _F) -> _F: return _intrinsic_impl()
    def sqrt(self: _F) -> _F: return _intrinsic_impl()
    def tan(self: _F) -> _F: return _intrinsic_impl()
    def tanh(self: _F) -> _F: return _intrinsic_impl()
    def trunc(self: _F) -> _F: return _intrinsic_impl()
    def atan2(self: _F, _other: _F) -> _F: return _intrinsic_impl()
    def copysign(self: _F, _other: _F) -> _F: return _intrinsic_impl()

@_builtin
def abs(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def acos(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def acosh(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def asin(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def asinh(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def atan(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def atanh(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def ceil(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def cos(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def cosh(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def exp(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def floor(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def log(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def log10(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def log2(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def sin(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def sinh(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def sqrt(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def tan(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def tanh(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def trunc(x: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def atan2(x: _F1, y: _F1) -> _F1: return _intrinsic_impl()
@_builtin
def copysign(x: _F1, y: _F1) -> _F1: return _intrinsic_impl()
_register_class(FloatBuiltin)
@_builtin_type(_hir.FloatType(32))
class f32(FloatBuiltin['f32']):
    def __init__(self, _value: tp.Union['f32', float]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['f32', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['f32', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['f32', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['f32', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['f32', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['f32', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()

@_builtin_type(_hir.FloatType(64))
class f64(FloatBuiltin['f64']):
    def __init__(self, _value: tp.Union['f64', float]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['f64', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['f64', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['f64', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['f64', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['f64', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['f64', float]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()

@_builtin_type(_hir.IntType(8, True))
class i8:
    def __init__(self, _value: tp.Union['i8', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['i8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['i8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['i8', int]) -> 'i8': return _intrinsic_impl()

@_builtin_type(_hir.IntType(8, False))
class u8:
    def __init__(self, _value: tp.Union['u8', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['u8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['u8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u8', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['u8', int]) -> 'u8': return _intrinsic_impl()

@_builtin_type(_hir.IntType(16, True))
class i16:
    def __init__(self, _value: tp.Union['i16', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['i16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['i16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['i16', int]) -> 'i16': return _intrinsic_impl()

@_builtin_type(_hir.IntType(16, False))
class u16:
    def __init__(self, _value: tp.Union['u16', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['u16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['u16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u16', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['u16', int]) -> 'u16': return _intrinsic_impl()

@_builtin_type(_hir.IntType(32, True))
class i32:
    def __init__(self, _value: tp.Union['i32', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['i32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['i32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['i32', int]) -> 'i32': return _intrinsic_impl()

@_builtin_type(_hir.IntType(32, False))
class u32:
    def __init__(self, _value: tp.Union['u32', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['u32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['u32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u32', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['u32', int]) -> 'u32': return _intrinsic_impl()

@_builtin_type(_hir.IntType(64, True))
class i64:
    def __init__(self, _value: tp.Union['i64', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['i64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['i64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['i64', int]) -> 'i64': return _intrinsic_impl()

@_builtin_type(_hir.IntType(64, False))
class u64:
    def __init__(self, _value: tp.Union['u64', int]) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['u64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['u64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u64', int]) -> 'bool': return _intrinsic_impl() # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __ifloordiv__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __lshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rlshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __ilshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rrshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __irshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __and__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rand__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __iand__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __or__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __ror__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __ior__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __xor__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __rxor__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()
    def __ixor__(self, _other:  tp.Union['u64', int]) -> 'u64': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[bool]), 2))
class bool2:
    x: bool
    y: bool
    def __init__(self, x: tp.Union['bool', bool] = False, y: tp.Union['bool', bool] = False) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32]), 2))
class float2:
    x: f32
    y: f32
    def __init__(self, x: tp.Union['f32', float] = 0.0, y: tp.Union['f32', float] = 0.0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64]), 2))
class double2:
    x: f64
    y: f64
    def __init__(self, x: tp.Union['f64', float] = 0.0, y: tp.Union['f64', float] = 0.0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8]), 2))
class byte2:
    x: i8
    y: i8
    def __init__(self, x: tp.Union['i8', int] = 0, y: tp.Union['i8', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8]), 2))
class ubyte2:
    x: u8
    y: u8
    def __init__(self, x: tp.Union['u8', int] = 0, y: tp.Union['u8', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16]), 2))
class short2:
    x: i16
    y: i16
    def __init__(self, x: tp.Union['i16', int] = 0, y: tp.Union['i16', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16]), 2))
class ushort2:
    x: u16
    y: u16
    def __init__(self, x: tp.Union['u16', int] = 0, y: tp.Union['u16', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32]), 2))
class int2:
    x: i32
    y: i32
    def __init__(self, x: tp.Union['i32', int] = 0, y: tp.Union['i32', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32]), 2))
class uint2:
    x: u32
    y: u32
    def __init__(self, x: tp.Union['u32', int] = 0, y: tp.Union['u32', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64]), 2))
class long2:
    x: i64
    y: i64
    def __init__(self, x: tp.Union['i64', int] = 0, y: tp.Union['i64', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64]), 2))
class ulong2:
    x: u64
    y: u64
    def __init__(self, x: tp.Union['u64', int] = 0, y: tp.Union['u64', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[bool]), 3))
class bool3:
    x: bool
    y: bool
    z: bool
    def __init__(self, x: tp.Union['bool', bool] = False, y: tp.Union['bool', bool] = False, z: tp.Union['bool', bool] = False) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32]), 3))
class float3:
    x: f32
    y: f32
    z: f32
    def __init__(self, x: tp.Union['f32', float] = 0.0, y: tp.Union['f32', float] = 0.0, z: tp.Union['f32', float] = 0.0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64]), 3))
class double3:
    x: f64
    y: f64
    z: f64
    def __init__(self, x: tp.Union['f64', float] = 0.0, y: tp.Union['f64', float] = 0.0, z: tp.Union['f64', float] = 0.0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8]), 3))
class byte3:
    x: i8
    y: i8
    z: i8
    def __init__(self, x: tp.Union['i8', int] = 0, y: tp.Union['i8', int] = 0, z: tp.Union['i8', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8]), 3))
class ubyte3:
    x: u8
    y: u8
    z: u8
    def __init__(self, x: tp.Union['u8', int] = 0, y: tp.Union['u8', int] = 0, z: tp.Union['u8', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16]), 3))
class short3:
    x: i16
    y: i16
    z: i16
    def __init__(self, x: tp.Union['i16', int] = 0, y: tp.Union['i16', int] = 0, z: tp.Union['i16', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16]), 3))
class ushort3:
    x: u16
    y: u16
    z: u16
    def __init__(self, x: tp.Union['u16', int] = 0, y: tp.Union['u16', int] = 0, z: tp.Union['u16', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32]), 3))
class int3:
    x: i32
    y: i32
    z: i32
    def __init__(self, x: tp.Union['i32', int] = 0, y: tp.Union['i32', int] = 0, z: tp.Union['i32', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32]), 3))
class uint3:
    x: u32
    y: u32
    z: u32
    def __init__(self, x: tp.Union['u32', int] = 0, y: tp.Union['u32', int] = 0, z: tp.Union['u32', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64]), 3))
class long3:
    x: i64
    y: i64
    z: i64
    def __init__(self, x: tp.Union['i64', int] = 0, y: tp.Union['i64', int] = 0, z: tp.Union['i64', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64]), 3))
class ulong3:
    x: u64
    y: u64
    z: u64
    def __init__(self, x: tp.Union['u64', int] = 0, y: tp.Union['u64', int] = 0, z: tp.Union['u64', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[bool]), 4))
class bool4:
    x: bool
    y: bool
    z: bool
    w: bool
    def __init__(self, x: tp.Union['bool', bool] = False, y: tp.Union['bool', bool] = False, z: tp.Union['bool', bool] = False, w: tp.Union['bool', bool] = False) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32]), 4))
class float4:
    x: f32
    y: f32
    z: f32
    w: f32
    def __init__(self, x: tp.Union['f32', float] = 0.0, y: tp.Union['f32', float] = 0.0, z: tp.Union['f32', float] = 0.0, w: tp.Union['f32', float] = 0.0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64]), 4))
class double4:
    x: f64
    y: f64
    z: f64
    w: f64
    def __init__(self, x: tp.Union['f64', float] = 0.0, y: tp.Union['f64', float] = 0.0, z: tp.Union['f64', float] = 0.0, w: tp.Union['f64', float] = 0.0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8]), 4))
class byte4:
    x: i8
    y: i8
    z: i8
    w: i8
    def __init__(self, x: tp.Union['i8', int] = 0, y: tp.Union['i8', int] = 0, z: tp.Union['i8', int] = 0, w: tp.Union['i8', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8]), 4))
class ubyte4:
    x: u8
    y: u8
    z: u8
    w: u8
    def __init__(self, x: tp.Union['u8', int] = 0, y: tp.Union['u8', int] = 0, z: tp.Union['u8', int] = 0, w: tp.Union['u8', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16]), 4))
class short4:
    x: i16
    y: i16
    z: i16
    w: i16
    def __init__(self, x: tp.Union['i16', int] = 0, y: tp.Union['i16', int] = 0, z: tp.Union['i16', int] = 0, w: tp.Union['i16', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16]), 4))
class ushort4:
    x: u16
    y: u16
    z: u16
    w: u16
    def __init__(self, x: tp.Union['u16', int] = 0, y: tp.Union['u16', int] = 0, z: tp.Union['u16', int] = 0, w: tp.Union['u16', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32]), 4))
class int4:
    x: i32
    y: i32
    z: i32
    w: i32
    def __init__(self, x: tp.Union['i32', int] = 0, y: tp.Union['i32', int] = 0, z: tp.Union['i32', int] = 0, w: tp.Union['i32', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32]), 4))
class uint4:
    x: u32
    y: u32
    z: u32
    w: u32
    def __init__(self, x: tp.Union['u32', int] = 0, y: tp.Union['u32', int] = 0, z: tp.Union['u32', int] = 0, w: tp.Union['u32', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64]), 4))
class long4:
    x: i64
    y: i64
    z: i64
    w: i64
    def __init__(self, x: tp.Union['i64', int] = 0, y: tp.Union['i64', int] = 0, z: tp.Union['i64', int] = 0, w: tp.Union['i64', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()

@_builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64]), 4))
class ulong4:
    x: u64
    y: u64
    z: u64
    w: u64
    def __init__(self, x: tp.Union['u64', int] = 0, y: tp.Union['u64', int] = 0, z: tp.Union['u64', int] = 0, w: tp.Union['u64', int] = 0) -> None: return _intrinsic_impl()
    def __add__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __radd__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __iadd__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __sub__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rsub__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __isub__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __mul__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rmul__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __imul__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __mod__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rmod__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __imod__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __lt__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __le__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return _intrinsic_impl() # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()

__all__ = ['FLOAT_TYPES', 'FloatType', 'FloatBuiltin', 'abs', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh', 'ceil', 'cos', 'cosh', 'exp', 'floor', 'log', 'log10', 'log2', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc', 'atan2', 'copysign', 'f32', 'f64', 'i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'bool2', 'float2', 'double2', 'byte2', 'ubyte2', 'short2', 'ushort2', 'int2', 'uint2', 'long2', 'ulong2', 'bool3', 'float3', 'double3', 'byte3', 'ubyte3', 'short3', 'ushort3', 'int3', 'uint3', 'long3', 'ulong3', 'bool4', 'float4', 'double4', 'byte4', 'ubyte4', 'short4', 'ushort4', 'int4', 'uint4', 'long4', 'ulong4']
