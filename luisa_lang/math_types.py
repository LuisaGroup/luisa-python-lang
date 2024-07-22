# fmt: off
import typing as tp
from luisa_lang._markers import _builtin, _builtin_type, _intrinsic_impl
FLOAT_TYPES: tp.Final[tp.List[str]] = ["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
FloatType = tp.Union["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
_F = tp.TypeVar("_F")
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
    def log2sin(self: _F) -> _F: return _intrinsic_impl()
    def sinh(self: _F) -> _F: return _intrinsic_impl()
    def sqrt(self: _F) -> _F: return _intrinsic_impl()
    def tan(self: _F) -> _F: return _intrinsic_impl()
    def tanh(self: _F) -> _F: return _intrinsic_impl()
    def trunc(self: _F) -> _F: return _intrinsic_impl()
    def atan2(self: _F, _other: _F) -> _F: return _intrinsic_impl()
    def copysign(self: _F, _other: _F) -> _F: return _intrinsic_impl()

@_builtin
def abs(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def acos(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def acosh(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def asin(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def asinh(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def atan(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def atanh(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def ceil(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def cos(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def cosh(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def exp(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def floor(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def log(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def log10(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def log2sin(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def sinh(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def sqrt(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def tan(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def tanh(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def trunc(x: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def atan2(x: FloatType, y: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin
def copysign(x: FloatType, y: FloatType) -> FloatType: return _intrinsic_impl()
@_builtin_type
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
    def __truediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': return _intrinsic_impl()

@_builtin_type
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
    def __truediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': return _intrinsic_impl()

@_builtin_type
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

@_builtin_type
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

@_builtin_type
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

@_builtin_type
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

@_builtin_type
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

@_builtin_type
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

@_builtin_type
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

@_builtin_type
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

@_builtin_type
class bool2:
    x: bool
    y: bool
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
    def __truediv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return _intrinsic_impl()

@_builtin_type
class float2:
    x: f32
    y: f32
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
    def __truediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return _intrinsic_impl()

@_builtin_type
class double2:
    x: f64
    y: f64
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
    def __truediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return _intrinsic_impl()

@_builtin_type
class byte2:
    x: i8
    y: i8
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
    def __truediv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return _intrinsic_impl()

@_builtin_type
class ubyte2:
    x: u8
    y: u8
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
    def __truediv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return _intrinsic_impl()

@_builtin_type
class short2:
    x: i16
    y: i16
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
    def __truediv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return _intrinsic_impl()

@_builtin_type
class ushort2:
    x: u16
    y: u16
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
    def __truediv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return _intrinsic_impl()

@_builtin_type
class int2:
    x: i32
    y: i32
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
    def __truediv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return _intrinsic_impl()

@_builtin_type
class uint2:
    x: u32
    y: u32
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
    def __truediv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return _intrinsic_impl()

@_builtin_type
class long2:
    x: i64
    y: i64
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
    def __truediv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return _intrinsic_impl()

@_builtin_type
class ulong2:
    x: u64
    y: u64
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
    def __truediv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return _intrinsic_impl()

@_builtin_type
class bool3:
    x: bool
    y: bool
    z: bool
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
    def __truediv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return _intrinsic_impl()

@_builtin_type
class float3:
    x: f32
    y: f32
    z: f32
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
    def __truediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return _intrinsic_impl()

@_builtin_type
class double3:
    x: f64
    y: f64
    z: f64
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
    def __truediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return _intrinsic_impl()

@_builtin_type
class byte3:
    x: i8
    y: i8
    z: i8
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
    def __truediv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return _intrinsic_impl()

@_builtin_type
class ubyte3:
    x: u8
    y: u8
    z: u8
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
    def __truediv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return _intrinsic_impl()

@_builtin_type
class short3:
    x: i16
    y: i16
    z: i16
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
    def __truediv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return _intrinsic_impl()

@_builtin_type
class ushort3:
    x: u16
    y: u16
    z: u16
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
    def __truediv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return _intrinsic_impl()

@_builtin_type
class int3:
    x: i32
    y: i32
    z: i32
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
    def __truediv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return _intrinsic_impl()

@_builtin_type
class uint3:
    x: u32
    y: u32
    z: u32
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
    def __truediv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return _intrinsic_impl()

@_builtin_type
class long3:
    x: i64
    y: i64
    z: i64
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
    def __truediv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return _intrinsic_impl()

@_builtin_type
class ulong3:
    x: u64
    y: u64
    z: u64
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
    def __truediv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return _intrinsic_impl()

@_builtin_type
class bool4:
    x: bool
    y: bool
    z: bool
    w: bool
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
    def __truediv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return _intrinsic_impl()

@_builtin_type
class float4:
    x: f32
    y: f32
    z: f32
    w: f32
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
    def __truediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return _intrinsic_impl()

@_builtin_type
class double4:
    x: f64
    y: f64
    z: f64
    w: f64
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
    def __truediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return _intrinsic_impl()

@_builtin_type
class byte4:
    x: i8
    y: i8
    z: i8
    w: i8
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
    def __truediv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return _intrinsic_impl()

@_builtin_type
class ubyte4:
    x: u8
    y: u8
    z: u8
    w: u8
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
    def __truediv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return _intrinsic_impl()

@_builtin_type
class short4:
    x: i16
    y: i16
    z: i16
    w: i16
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
    def __truediv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return _intrinsic_impl()

@_builtin_type
class ushort4:
    x: u16
    y: u16
    z: u16
    w: u16
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
    def __truediv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return _intrinsic_impl()

@_builtin_type
class int4:
    x: i32
    y: i32
    z: i32
    w: i32
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
    def __truediv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return _intrinsic_impl()

@_builtin_type
class uint4:
    x: u32
    y: u32
    z: u32
    w: u32
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
    def __truediv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return _intrinsic_impl()

@_builtin_type
class long4:
    x: i64
    y: i64
    z: i64
    w: i64
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
    def __truediv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return _intrinsic_impl()

@_builtin_type
class ulong4:
    x: u64
    y: u64
    z: u64
    w: u64
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
    def __truediv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rtruediv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __itruediv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __pow__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rpow__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __ipow__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __floordiv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()
    def __rfloordiv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return _intrinsic_impl()

