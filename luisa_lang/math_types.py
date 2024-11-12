# fmt: off
import typing as tp
from luisa_lang._builtin_decor import intrinsic, func, builtin_type
from luisa_lang.classinfo import register_class
import luisa_lang.hir as _hir
_ctx = _hir.GlobalContext.get()
FLOAT_TYPES: tp.Final[tp.List[str]] = ["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
FloatType = tp.Union["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
_F = tp.TypeVar("_F")
_F1 = tp.TypeVar("_F1", "f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4")
class FloatBuiltin(tp.Generic[_F]):
    def abs(self: _F) -> _F: return intrinsic('math.abs', _F) # type: ignore
    def acos(self: _F) -> _F: return intrinsic('math.acos', _F) # type: ignore
    def acosh(self: _F) -> _F: return intrinsic('math.acosh', _F) # type: ignore
    def asin(self: _F) -> _F: return intrinsic('math.asin', _F) # type: ignore
    def asinh(self: _F) -> _F: return intrinsic('math.asinh', _F) # type: ignore
    def atan(self: _F) -> _F: return intrinsic('math.atan', _F) # type: ignore
    def atanh(self: _F) -> _F: return intrinsic('math.atanh', _F) # type: ignore
    def ceil(self: _F) -> _F: return intrinsic('math.ceil', _F) # type: ignore
    def cos(self: _F) -> _F: return intrinsic('math.cos', _F) # type: ignore
    def cosh(self: _F) -> _F: return intrinsic('math.cosh', _F) # type: ignore
    def exp(self: _F) -> _F: return intrinsic('math.exp', _F) # type: ignore
    def floor(self: _F) -> _F: return intrinsic('math.floor', _F) # type: ignore
    def log(self: _F) -> _F: return intrinsic('math.log', _F) # type: ignore
    def log10(self: _F) -> _F: return intrinsic('math.log10', _F) # type: ignore
    def log2(self: _F) -> _F: return intrinsic('math.log2', _F) # type: ignore
    def sin(self: _F) -> _F: return intrinsic('math.sin', _F) # type: ignore
    def sinh(self: _F) -> _F: return intrinsic('math.sinh', _F) # type: ignore
    def sqrt(self: _F) -> _F: return intrinsic('math.sqrt', _F) # type: ignore
    def tan(self: _F) -> _F: return intrinsic('math.tan', _F) # type: ignore
    def tanh(self: _F) -> _F: return intrinsic('math.tanh', _F) # type: ignore
    def trunc(self: _F) -> _F: return intrinsic('math.trunc', _F) # type: ignore
    def atan2(self: _F, _other: _F) -> _F: return intrinsic('math.atan2', _F) # type: ignore
    def copysign(self: _F, _other: _F) -> _F: return intrinsic('math.copysign', _F) # type: ignore

@func
def abs(x: _F1) -> _F1: return x.abs()
@func
def acos(x: _F1) -> _F1: return x.acos()
@func
def acosh(x: _F1) -> _F1: return x.acosh()
@func
def asin(x: _F1) -> _F1: return x.asin()
@func
def asinh(x: _F1) -> _F1: return x.asinh()
@func
def atan(x: _F1) -> _F1: return x.atan()
@func
def atanh(x: _F1) -> _F1: return x.atanh()
@func
def ceil(x: _F1) -> _F1: return x.ceil()
@func
def cos(x: _F1) -> _F1: return x.cos()
@func
def cosh(x: _F1) -> _F1: return x.cosh()
@func
def exp(x: _F1) -> _F1: return x.exp()
@func
def floor(x: _F1) -> _F1: return x.floor()
@func
def log(x: _F1) -> _F1: return x.log()
@func
def log10(x: _F1) -> _F1: return x.log10()
@func
def log2(x: _F1) -> _F1: return x.log2()
@func
def sin(x: _F1) -> _F1: return x.sin()
@func
def sinh(x: _F1) -> _F1: return x.sinh()
@func
def sqrt(x: _F1) -> _F1: return x.sqrt()
@func
def tan(x: _F1) -> _F1: return x.tan()
@func
def tanh(x: _F1) -> _F1: return x.tanh()
@func
def trunc(x: _F1) -> _F1: return x.trunc()
@func
def atan2(x: _F1, y: _F1) -> _F1: return x.atan2(y)
@func
def copysign(x: _F1, y: _F1) -> _F1: return x.copysign(y)
register_class(FloatBuiltin)
@builtin_type(_hir.FloatType(32))
class f32(FloatBuiltin['f32']):
    def __init__(self, _value: tp.Union['f32', float]) -> None:
        self = intrinsic("init.f32",  f32,  _value)
    def __add__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__add__.f32",  f32,  _other)
    def __radd__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__radd__.f32",  f32,  _other)
    def __iadd__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__iadd__.f32",  f32,  _other)
    def __sub__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__sub__.f32",  f32,  _other)
    def __rsub__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__rsub__.f32",  f32,  _other)
    def __isub__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__isub__.f32",  f32,  _other)
    def __mul__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__mul__.f32",  f32,  _other)
    def __rmul__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__rmul__.f32",  f32,  _other)
    def __imul__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__imul__.f32",  f32,  _other)
    def __mod__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__mod__.f32",  f32,  _other)
    def __rmod__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__rmod__.f32",  f32,  _other)
    def __imod__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__imod__.f32",  f32,  _other)
    def __lt__(self, _other:  tp.Union['f32', float]) -> 'bool': return intrinsic("cmp.__lt__.f32",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['f32', float]) -> 'bool': return intrinsic("cmp.__le__.f32",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['f32', float]) -> 'bool': return intrinsic("cmp.__gt__.f32",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['f32', float]) -> 'bool': return intrinsic("cmp.__ge__.f32",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['f32', float]) -> 'bool': return intrinsic("cmp.__eq__.f32",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['f32', float]) -> 'bool': return intrinsic("cmp.__ne__.f32",  bool,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__truediv__.f32",  f32,  _other)
    def __rtruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__rtruediv__.f32",  f32,  _other)
    def __itruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__itruediv__.f32",  f32,  _other)
    def __pow__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__pow__.f32",  f32,  _other)
    def __rpow__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__rpow__.f32",  f32,  _other)
    def __ipow__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__ipow__.f32",  f32,  _other)
    def __floordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__floordiv__.f32",  f32,  _other)
    def __rfloordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': return intrinsic("binop.__rfloordiv__.f32",  f32,  _other)
    def __neg__(self) -> 'f32': return intrinsic("unary.neg.f32",  f32)
    def __pos__(self) -> 'f32': return intrinsic("unary.pos.f32",  f32)

@builtin_type(_hir.FloatType(64))
class f64(FloatBuiltin['f64']):
    def __init__(self, _value: tp.Union['f64', float]) -> None:
        self = intrinsic("init.f64",  f64,  _value)
    def __add__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__add__.f64",  f64,  _other)
    def __radd__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__radd__.f64",  f64,  _other)
    def __iadd__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__iadd__.f64",  f64,  _other)
    def __sub__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__sub__.f64",  f64,  _other)
    def __rsub__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__rsub__.f64",  f64,  _other)
    def __isub__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__isub__.f64",  f64,  _other)
    def __mul__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__mul__.f64",  f64,  _other)
    def __rmul__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__rmul__.f64",  f64,  _other)
    def __imul__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__imul__.f64",  f64,  _other)
    def __mod__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__mod__.f64",  f64,  _other)
    def __rmod__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__rmod__.f64",  f64,  _other)
    def __imod__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__imod__.f64",  f64,  _other)
    def __lt__(self, _other:  tp.Union['f64', float]) -> 'bool': return intrinsic("cmp.__lt__.f64",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['f64', float]) -> 'bool': return intrinsic("cmp.__le__.f64",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['f64', float]) -> 'bool': return intrinsic("cmp.__gt__.f64",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['f64', float]) -> 'bool': return intrinsic("cmp.__ge__.f64",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['f64', float]) -> 'bool': return intrinsic("cmp.__eq__.f64",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['f64', float]) -> 'bool': return intrinsic("cmp.__ne__.f64",  bool,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__truediv__.f64",  f64,  _other)
    def __rtruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__rtruediv__.f64",  f64,  _other)
    def __itruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__itruediv__.f64",  f64,  _other)
    def __pow__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__pow__.f64",  f64,  _other)
    def __rpow__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__rpow__.f64",  f64,  _other)
    def __ipow__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__ipow__.f64",  f64,  _other)
    def __floordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__floordiv__.f64",  f64,  _other)
    def __rfloordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': return intrinsic("binop.__rfloordiv__.f64",  f64,  _other)
    def __neg__(self) -> 'f64': return intrinsic("unary.neg.f64",  f64)
    def __pos__(self) -> 'f64': return intrinsic("unary.pos.f64",  f64)

@builtin_type(_hir.IntType(8, True))
class i8:
    def __init__(self, _value: tp.Union['i8', int]) -> None:
        self = intrinsic("init.i8",  i8,  _value)
    def __add__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__add__.i8",  i8,  _other)
    def __radd__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__radd__.i8",  i8,  _other)
    def __iadd__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__iadd__.i8",  i8,  _other)
    def __sub__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__sub__.i8",  i8,  _other)
    def __rsub__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rsub__.i8",  i8,  _other)
    def __isub__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__isub__.i8",  i8,  _other)
    def __mul__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__mul__.i8",  i8,  _other)
    def __rmul__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rmul__.i8",  i8,  _other)
    def __imul__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__imul__.i8",  i8,  _other)
    def __mod__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__mod__.i8",  i8,  _other)
    def __rmod__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rmod__.i8",  i8,  _other)
    def __imod__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__imod__.i8",  i8,  _other)
    def __lt__(self, _other:  tp.Union['i8', int]) -> 'bool': return intrinsic("cmp.__lt__.i8",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['i8', int]) -> 'bool': return intrinsic("cmp.__le__.i8",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i8', int]) -> 'bool': return intrinsic("cmp.__gt__.i8",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i8', int]) -> 'bool': return intrinsic("cmp.__ge__.i8",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i8', int]) -> 'bool': return intrinsic("cmp.__eq__.i8",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i8', int]) -> 'bool': return intrinsic("cmp.__ne__.i8",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__floordiv__.i8",  i8,  _other)
    def __rfloordiv__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rfloordiv__.i8",  i8,  _other)
    def __ifloordiv__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__ifloordiv__.i8",  i8,  _other)
    def __lshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__lshift__.i8",  i8,  _other)
    def __rlshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rlshift__.i8",  i8,  _other)
    def __ilshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__ilshift__.i8",  i8,  _other)
    def __rshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rshift__.i8",  i8,  _other)
    def __rrshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rrshift__.i8",  i8,  _other)
    def __irshift__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__irshift__.i8",  i8,  _other)
    def __and__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__and__.i8",  i8,  _other)
    def __rand__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rand__.i8",  i8,  _other)
    def __iand__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__iand__.i8",  i8,  _other)
    def __or__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__or__.i8",  i8,  _other)
    def __ror__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__ror__.i8",  i8,  _other)
    def __ior__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__ior__.i8",  i8,  _other)
    def __xor__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__xor__.i8",  i8,  _other)
    def __rxor__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__rxor__.i8",  i8,  _other)
    def __ixor__(self, _other:  tp.Union['i8', int]) -> 'i8': return intrinsic("binop.__ixor__.i8",  i8,  _other)
    def __neg__(self) -> 'i8': return intrinsic("unary.neg.i8",  i8)
    def __pos__(self) -> 'i8': return intrinsic("unary.pos.i8",  i8)
    def __invert__(self) -> 'i8': return intrinsic("unary.invert.i8",  i8)

@builtin_type(_hir.IntType(8, False))
class u8:
    def __init__(self, _value: tp.Union['u8', int]) -> None:
        self = intrinsic("init.u8",  u8,  _value)
    def __add__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__add__.u8",  u8,  _other)
    def __radd__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__radd__.u8",  u8,  _other)
    def __iadd__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__iadd__.u8",  u8,  _other)
    def __sub__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__sub__.u8",  u8,  _other)
    def __rsub__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rsub__.u8",  u8,  _other)
    def __isub__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__isub__.u8",  u8,  _other)
    def __mul__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__mul__.u8",  u8,  _other)
    def __rmul__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rmul__.u8",  u8,  _other)
    def __imul__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__imul__.u8",  u8,  _other)
    def __mod__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__mod__.u8",  u8,  _other)
    def __rmod__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rmod__.u8",  u8,  _other)
    def __imod__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__imod__.u8",  u8,  _other)
    def __lt__(self, _other:  tp.Union['u8', int]) -> 'bool': return intrinsic("cmp.__lt__.u8",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['u8', int]) -> 'bool': return intrinsic("cmp.__le__.u8",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u8', int]) -> 'bool': return intrinsic("cmp.__gt__.u8",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u8', int]) -> 'bool': return intrinsic("cmp.__ge__.u8",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u8', int]) -> 'bool': return intrinsic("cmp.__eq__.u8",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u8', int]) -> 'bool': return intrinsic("cmp.__ne__.u8",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__floordiv__.u8",  u8,  _other)
    def __rfloordiv__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rfloordiv__.u8",  u8,  _other)
    def __ifloordiv__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__ifloordiv__.u8",  u8,  _other)
    def __lshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__lshift__.u8",  u8,  _other)
    def __rlshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rlshift__.u8",  u8,  _other)
    def __ilshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__ilshift__.u8",  u8,  _other)
    def __rshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rshift__.u8",  u8,  _other)
    def __rrshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rrshift__.u8",  u8,  _other)
    def __irshift__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__irshift__.u8",  u8,  _other)
    def __and__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__and__.u8",  u8,  _other)
    def __rand__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rand__.u8",  u8,  _other)
    def __iand__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__iand__.u8",  u8,  _other)
    def __or__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__or__.u8",  u8,  _other)
    def __ror__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__ror__.u8",  u8,  _other)
    def __ior__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__ior__.u8",  u8,  _other)
    def __xor__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__xor__.u8",  u8,  _other)
    def __rxor__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__rxor__.u8",  u8,  _other)
    def __ixor__(self, _other:  tp.Union['u8', int]) -> 'u8': return intrinsic("binop.__ixor__.u8",  u8,  _other)
    def __neg__(self) -> 'u8': return intrinsic("unary.neg.u8",  u8)
    def __pos__(self) -> 'u8': return intrinsic("unary.pos.u8",  u8)
    def __invert__(self) -> 'u8': return intrinsic("unary.invert.u8",  u8)

@builtin_type(_hir.IntType(16, True))
class i16:
    def __init__(self, _value: tp.Union['i16', int]) -> None:
        self = intrinsic("init.i16",  i16,  _value)
    def __add__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__add__.i16",  i16,  _other)
    def __radd__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__radd__.i16",  i16,  _other)
    def __iadd__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__iadd__.i16",  i16,  _other)
    def __sub__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__sub__.i16",  i16,  _other)
    def __rsub__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rsub__.i16",  i16,  _other)
    def __isub__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__isub__.i16",  i16,  _other)
    def __mul__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__mul__.i16",  i16,  _other)
    def __rmul__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rmul__.i16",  i16,  _other)
    def __imul__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__imul__.i16",  i16,  _other)
    def __mod__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__mod__.i16",  i16,  _other)
    def __rmod__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rmod__.i16",  i16,  _other)
    def __imod__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__imod__.i16",  i16,  _other)
    def __lt__(self, _other:  tp.Union['i16', int]) -> 'bool': return intrinsic("cmp.__lt__.i16",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['i16', int]) -> 'bool': return intrinsic("cmp.__le__.i16",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i16', int]) -> 'bool': return intrinsic("cmp.__gt__.i16",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i16', int]) -> 'bool': return intrinsic("cmp.__ge__.i16",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i16', int]) -> 'bool': return intrinsic("cmp.__eq__.i16",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i16', int]) -> 'bool': return intrinsic("cmp.__ne__.i16",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__floordiv__.i16",  i16,  _other)
    def __rfloordiv__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rfloordiv__.i16",  i16,  _other)
    def __ifloordiv__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__ifloordiv__.i16",  i16,  _other)
    def __lshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__lshift__.i16",  i16,  _other)
    def __rlshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rlshift__.i16",  i16,  _other)
    def __ilshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__ilshift__.i16",  i16,  _other)
    def __rshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rshift__.i16",  i16,  _other)
    def __rrshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rrshift__.i16",  i16,  _other)
    def __irshift__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__irshift__.i16",  i16,  _other)
    def __and__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__and__.i16",  i16,  _other)
    def __rand__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rand__.i16",  i16,  _other)
    def __iand__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__iand__.i16",  i16,  _other)
    def __or__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__or__.i16",  i16,  _other)
    def __ror__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__ror__.i16",  i16,  _other)
    def __ior__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__ior__.i16",  i16,  _other)
    def __xor__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__xor__.i16",  i16,  _other)
    def __rxor__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__rxor__.i16",  i16,  _other)
    def __ixor__(self, _other:  tp.Union['i16', int]) -> 'i16': return intrinsic("binop.__ixor__.i16",  i16,  _other)
    def __neg__(self) -> 'i16': return intrinsic("unary.neg.i16",  i16)
    def __pos__(self) -> 'i16': return intrinsic("unary.pos.i16",  i16)
    def __invert__(self) -> 'i16': return intrinsic("unary.invert.i16",  i16)

@builtin_type(_hir.IntType(16, False))
class u16:
    def __init__(self, _value: tp.Union['u16', int]) -> None:
        self = intrinsic("init.u16",  u16,  _value)
    def __add__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__add__.u16",  u16,  _other)
    def __radd__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__radd__.u16",  u16,  _other)
    def __iadd__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__iadd__.u16",  u16,  _other)
    def __sub__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__sub__.u16",  u16,  _other)
    def __rsub__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rsub__.u16",  u16,  _other)
    def __isub__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__isub__.u16",  u16,  _other)
    def __mul__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__mul__.u16",  u16,  _other)
    def __rmul__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rmul__.u16",  u16,  _other)
    def __imul__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__imul__.u16",  u16,  _other)
    def __mod__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__mod__.u16",  u16,  _other)
    def __rmod__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rmod__.u16",  u16,  _other)
    def __imod__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__imod__.u16",  u16,  _other)
    def __lt__(self, _other:  tp.Union['u16', int]) -> 'bool': return intrinsic("cmp.__lt__.u16",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['u16', int]) -> 'bool': return intrinsic("cmp.__le__.u16",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u16', int]) -> 'bool': return intrinsic("cmp.__gt__.u16",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u16', int]) -> 'bool': return intrinsic("cmp.__ge__.u16",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u16', int]) -> 'bool': return intrinsic("cmp.__eq__.u16",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u16', int]) -> 'bool': return intrinsic("cmp.__ne__.u16",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__floordiv__.u16",  u16,  _other)
    def __rfloordiv__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rfloordiv__.u16",  u16,  _other)
    def __ifloordiv__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__ifloordiv__.u16",  u16,  _other)
    def __lshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__lshift__.u16",  u16,  _other)
    def __rlshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rlshift__.u16",  u16,  _other)
    def __ilshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__ilshift__.u16",  u16,  _other)
    def __rshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rshift__.u16",  u16,  _other)
    def __rrshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rrshift__.u16",  u16,  _other)
    def __irshift__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__irshift__.u16",  u16,  _other)
    def __and__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__and__.u16",  u16,  _other)
    def __rand__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rand__.u16",  u16,  _other)
    def __iand__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__iand__.u16",  u16,  _other)
    def __or__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__or__.u16",  u16,  _other)
    def __ror__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__ror__.u16",  u16,  _other)
    def __ior__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__ior__.u16",  u16,  _other)
    def __xor__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__xor__.u16",  u16,  _other)
    def __rxor__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__rxor__.u16",  u16,  _other)
    def __ixor__(self, _other:  tp.Union['u16', int]) -> 'u16': return intrinsic("binop.__ixor__.u16",  u16,  _other)
    def __neg__(self) -> 'u16': return intrinsic("unary.neg.u16",  u16)
    def __pos__(self) -> 'u16': return intrinsic("unary.pos.u16",  u16)
    def __invert__(self) -> 'u16': return intrinsic("unary.invert.u16",  u16)

@builtin_type(_hir.IntType(32, True))
class i32:
    def __init__(self, _value: tp.Union['i32', int]) -> None:
        self = intrinsic("init.i32",  i32,  _value)
    def __add__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__add__.i32",  i32,  _other)
    def __radd__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__radd__.i32",  i32,  _other)
    def __iadd__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__iadd__.i32",  i32,  _other)
    def __sub__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__sub__.i32",  i32,  _other)
    def __rsub__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rsub__.i32",  i32,  _other)
    def __isub__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__isub__.i32",  i32,  _other)
    def __mul__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__mul__.i32",  i32,  _other)
    def __rmul__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rmul__.i32",  i32,  _other)
    def __imul__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__imul__.i32",  i32,  _other)
    def __mod__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__mod__.i32",  i32,  _other)
    def __rmod__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rmod__.i32",  i32,  _other)
    def __imod__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__imod__.i32",  i32,  _other)
    def __lt__(self, _other:  tp.Union['i32', int]) -> 'bool': return intrinsic("cmp.__lt__.i32",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['i32', int]) -> 'bool': return intrinsic("cmp.__le__.i32",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i32', int]) -> 'bool': return intrinsic("cmp.__gt__.i32",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i32', int]) -> 'bool': return intrinsic("cmp.__ge__.i32",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i32', int]) -> 'bool': return intrinsic("cmp.__eq__.i32",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i32', int]) -> 'bool': return intrinsic("cmp.__ne__.i32",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__floordiv__.i32",  i32,  _other)
    def __rfloordiv__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rfloordiv__.i32",  i32,  _other)
    def __ifloordiv__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__ifloordiv__.i32",  i32,  _other)
    def __lshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__lshift__.i32",  i32,  _other)
    def __rlshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rlshift__.i32",  i32,  _other)
    def __ilshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__ilshift__.i32",  i32,  _other)
    def __rshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rshift__.i32",  i32,  _other)
    def __rrshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rrshift__.i32",  i32,  _other)
    def __irshift__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__irshift__.i32",  i32,  _other)
    def __and__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__and__.i32",  i32,  _other)
    def __rand__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rand__.i32",  i32,  _other)
    def __iand__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__iand__.i32",  i32,  _other)
    def __or__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__or__.i32",  i32,  _other)
    def __ror__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__ror__.i32",  i32,  _other)
    def __ior__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__ior__.i32",  i32,  _other)
    def __xor__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__xor__.i32",  i32,  _other)
    def __rxor__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__rxor__.i32",  i32,  _other)
    def __ixor__(self, _other:  tp.Union['i32', int]) -> 'i32': return intrinsic("binop.__ixor__.i32",  i32,  _other)
    def __neg__(self) -> 'i32': return intrinsic("unary.neg.i32",  i32)
    def __pos__(self) -> 'i32': return intrinsic("unary.pos.i32",  i32)
    def __invert__(self) -> 'i32': return intrinsic("unary.invert.i32",  i32)

@builtin_type(_hir.IntType(32, False))
class u32:
    def __init__(self, _value: tp.Union['u32', int]) -> None:
        self = intrinsic("init.u32",  u32,  _value)
    def __add__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__add__.u32",  u32,  _other)
    def __radd__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__radd__.u32",  u32,  _other)
    def __iadd__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__iadd__.u32",  u32,  _other)
    def __sub__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__sub__.u32",  u32,  _other)
    def __rsub__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rsub__.u32",  u32,  _other)
    def __isub__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__isub__.u32",  u32,  _other)
    def __mul__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__mul__.u32",  u32,  _other)
    def __rmul__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rmul__.u32",  u32,  _other)
    def __imul__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__imul__.u32",  u32,  _other)
    def __mod__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__mod__.u32",  u32,  _other)
    def __rmod__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rmod__.u32",  u32,  _other)
    def __imod__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__imod__.u32",  u32,  _other)
    def __lt__(self, _other:  tp.Union['u32', int]) -> 'bool': return intrinsic("cmp.__lt__.u32",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['u32', int]) -> 'bool': return intrinsic("cmp.__le__.u32",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u32', int]) -> 'bool': return intrinsic("cmp.__gt__.u32",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u32', int]) -> 'bool': return intrinsic("cmp.__ge__.u32",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u32', int]) -> 'bool': return intrinsic("cmp.__eq__.u32",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u32', int]) -> 'bool': return intrinsic("cmp.__ne__.u32",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__floordiv__.u32",  u32,  _other)
    def __rfloordiv__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rfloordiv__.u32",  u32,  _other)
    def __ifloordiv__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__ifloordiv__.u32",  u32,  _other)
    def __lshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__lshift__.u32",  u32,  _other)
    def __rlshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rlshift__.u32",  u32,  _other)
    def __ilshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__ilshift__.u32",  u32,  _other)
    def __rshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rshift__.u32",  u32,  _other)
    def __rrshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rrshift__.u32",  u32,  _other)
    def __irshift__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__irshift__.u32",  u32,  _other)
    def __and__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__and__.u32",  u32,  _other)
    def __rand__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rand__.u32",  u32,  _other)
    def __iand__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__iand__.u32",  u32,  _other)
    def __or__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__or__.u32",  u32,  _other)
    def __ror__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__ror__.u32",  u32,  _other)
    def __ior__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__ior__.u32",  u32,  _other)
    def __xor__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__xor__.u32",  u32,  _other)
    def __rxor__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__rxor__.u32",  u32,  _other)
    def __ixor__(self, _other:  tp.Union['u32', int]) -> 'u32': return intrinsic("binop.__ixor__.u32",  u32,  _other)
    def __neg__(self) -> 'u32': return intrinsic("unary.neg.u32",  u32)
    def __pos__(self) -> 'u32': return intrinsic("unary.pos.u32",  u32)
    def __invert__(self) -> 'u32': return intrinsic("unary.invert.u32",  u32)

@builtin_type(_hir.IntType(64, True))
class i64:
    def __init__(self, _value: tp.Union['i64', int]) -> None:
        self = intrinsic("init.i64",  i64,  _value)
    def __add__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__add__.i64",  i64,  _other)
    def __radd__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__radd__.i64",  i64,  _other)
    def __iadd__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__iadd__.i64",  i64,  _other)
    def __sub__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__sub__.i64",  i64,  _other)
    def __rsub__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rsub__.i64",  i64,  _other)
    def __isub__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__isub__.i64",  i64,  _other)
    def __mul__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__mul__.i64",  i64,  _other)
    def __rmul__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rmul__.i64",  i64,  _other)
    def __imul__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__imul__.i64",  i64,  _other)
    def __mod__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__mod__.i64",  i64,  _other)
    def __rmod__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rmod__.i64",  i64,  _other)
    def __imod__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__imod__.i64",  i64,  _other)
    def __lt__(self, _other:  tp.Union['i64', int]) -> 'bool': return intrinsic("cmp.__lt__.i64",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['i64', int]) -> 'bool': return intrinsic("cmp.__le__.i64",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['i64', int]) -> 'bool': return intrinsic("cmp.__gt__.i64",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['i64', int]) -> 'bool': return intrinsic("cmp.__ge__.i64",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['i64', int]) -> 'bool': return intrinsic("cmp.__eq__.i64",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['i64', int]) -> 'bool': return intrinsic("cmp.__ne__.i64",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__floordiv__.i64",  i64,  _other)
    def __rfloordiv__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rfloordiv__.i64",  i64,  _other)
    def __ifloordiv__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__ifloordiv__.i64",  i64,  _other)
    def __lshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__lshift__.i64",  i64,  _other)
    def __rlshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rlshift__.i64",  i64,  _other)
    def __ilshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__ilshift__.i64",  i64,  _other)
    def __rshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rshift__.i64",  i64,  _other)
    def __rrshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rrshift__.i64",  i64,  _other)
    def __irshift__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__irshift__.i64",  i64,  _other)
    def __and__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__and__.i64",  i64,  _other)
    def __rand__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rand__.i64",  i64,  _other)
    def __iand__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__iand__.i64",  i64,  _other)
    def __or__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__or__.i64",  i64,  _other)
    def __ror__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__ror__.i64",  i64,  _other)
    def __ior__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__ior__.i64",  i64,  _other)
    def __xor__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__xor__.i64",  i64,  _other)
    def __rxor__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__rxor__.i64",  i64,  _other)
    def __ixor__(self, _other:  tp.Union['i64', int]) -> 'i64': return intrinsic("binop.__ixor__.i64",  i64,  _other)
    def __neg__(self) -> 'i64': return intrinsic("unary.neg.i64",  i64)
    def __pos__(self) -> 'i64': return intrinsic("unary.pos.i64",  i64)
    def __invert__(self) -> 'i64': return intrinsic("unary.invert.i64",  i64)

@builtin_type(_hir.IntType(64, False))
class u64:
    def __init__(self, _value: tp.Union['u64', int]) -> None:
        self = intrinsic("init.u64",  u64,  _value)
    def __add__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__add__.u64",  u64,  _other)
    def __radd__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__radd__.u64",  u64,  _other)
    def __iadd__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__iadd__.u64",  u64,  _other)
    def __sub__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__sub__.u64",  u64,  _other)
    def __rsub__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rsub__.u64",  u64,  _other)
    def __isub__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__isub__.u64",  u64,  _other)
    def __mul__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__mul__.u64",  u64,  _other)
    def __rmul__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rmul__.u64",  u64,  _other)
    def __imul__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__imul__.u64",  u64,  _other)
    def __mod__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__mod__.u64",  u64,  _other)
    def __rmod__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rmod__.u64",  u64,  _other)
    def __imod__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__imod__.u64",  u64,  _other)
    def __lt__(self, _other:  tp.Union['u64', int]) -> 'bool': return intrinsic("cmp.__lt__.u64",  bool,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['u64', int]) -> 'bool': return intrinsic("cmp.__le__.u64",  bool,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['u64', int]) -> 'bool': return intrinsic("cmp.__gt__.u64",  bool,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['u64', int]) -> 'bool': return intrinsic("cmp.__ge__.u64",  bool,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['u64', int]) -> 'bool': return intrinsic("cmp.__eq__.u64",  bool,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['u64', int]) -> 'bool': return intrinsic("cmp.__ne__.u64",  bool,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__floordiv__.u64",  u64,  _other)
    def __rfloordiv__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rfloordiv__.u64",  u64,  _other)
    def __ifloordiv__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__ifloordiv__.u64",  u64,  _other)
    def __lshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__lshift__.u64",  u64,  _other)
    def __rlshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rlshift__.u64",  u64,  _other)
    def __ilshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__ilshift__.u64",  u64,  _other)
    def __rshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rshift__.u64",  u64,  _other)
    def __rrshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rrshift__.u64",  u64,  _other)
    def __irshift__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__irshift__.u64",  u64,  _other)
    def __and__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__and__.u64",  u64,  _other)
    def __rand__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rand__.u64",  u64,  _other)
    def __iand__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__iand__.u64",  u64,  _other)
    def __or__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__or__.u64",  u64,  _other)
    def __ror__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__ror__.u64",  u64,  _other)
    def __ior__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__ior__.u64",  u64,  _other)
    def __xor__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__xor__.u64",  u64,  _other)
    def __rxor__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__rxor__.u64",  u64,  _other)
    def __ixor__(self, _other:  tp.Union['u64', int]) -> 'u64': return intrinsic("binop.__ixor__.u64",  u64,  _other)
    def __neg__(self) -> 'u64': return intrinsic("unary.neg.u64",  u64)
    def __pos__(self) -> 'u64': return intrinsic("unary.pos.u64",  u64)
    def __invert__(self) -> 'u64': return intrinsic("unary.invert.u64",  u64)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[bool]), 2))
class bool2:
    x: bool
    y: bool
    def __init__(self, x: tp.Union['bool', bool] = False, y: tp.Union['bool', bool] = False) -> None: self = intrinsic("init.bool2", bool2, x, y)
    def __eq__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("cmp.__eq__.bool2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("cmp.__ne__.bool2",  bool2,  _other) # type: ignore[override]
    def __and__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__and__.bool2",  bool2,  _other)
    def __rand__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__rand__.bool2",  bool2,  _other)
    def __iand__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__iand__.bool2",  bool2,  _other)
    def __or__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__or__.bool2",  bool2,  _other)
    def __ror__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__ror__.bool2",  bool2,  _other)
    def __ior__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__ior__.bool2",  bool2,  _other)
    def __xor__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__xor__.bool2",  bool2,  _other)
    def __rxor__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__rxor__.bool2",  bool2,  _other)
    def __ixor__(self, _other:  tp.Union['bool2', bool, bool]) -> 'bool2': return intrinsic("binop.__ixor__.bool2",  bool2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32]), 2))
class float2(FloatBuiltin['float2']):
    x: f32
    y: f32
    def __init__(self, x: tp.Union['f32', float] = 0.0, y: tp.Union['f32', float] = 0.0) -> None: self = intrinsic("init.float2", float2, x, y)
    def __add__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__add__.float2",  float2,  _other)
    def __radd__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__radd__.float2",  float2,  _other)
    def __iadd__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__iadd__.float2",  float2,  _other)
    def __sub__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__sub__.float2",  float2,  _other)
    def __rsub__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__rsub__.float2",  float2,  _other)
    def __isub__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__isub__.float2",  float2,  _other)
    def __mul__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__mul__.float2",  float2,  _other)
    def __rmul__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__rmul__.float2",  float2,  _other)
    def __imul__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__imul__.float2",  float2,  _other)
    def __mod__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__mod__.float2",  float2,  _other)
    def __rmod__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__rmod__.float2",  float2,  _other)
    def __imod__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__imod__.float2",  float2,  _other)
    def __lt__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return intrinsic("cmp.__lt__.float2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return intrinsic("cmp.__le__.float2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return intrinsic("cmp.__gt__.float2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return intrinsic("cmp.__ge__.float2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return intrinsic("cmp.__eq__.float2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['float2', f32, float]) -> 'bool2': return intrinsic("cmp.__ne__.float2",  bool2,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__truediv__.float2",  float2,  _other)
    def __rtruediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__rtruediv__.float2",  float2,  _other)
    def __itruediv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__itruediv__.float2",  float2,  _other)
    def __pow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__pow__.float2",  float2,  _other)
    def __rpow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__rpow__.float2",  float2,  _other)
    def __ipow__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__ipow__.float2",  float2,  _other)
    def __floordiv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__floordiv__.float2",  float2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['float2', f32, float]) -> 'float2': return intrinsic("binop.__rfloordiv__.float2",  float2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64]), 2))
class double2(FloatBuiltin['double2']):
    x: f64
    y: f64
    def __init__(self, x: tp.Union['f64', float] = 0.0, y: tp.Union['f64', float] = 0.0) -> None: self = intrinsic("init.double2", double2, x, y)
    def __add__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__add__.double2",  double2,  _other)
    def __radd__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__radd__.double2",  double2,  _other)
    def __iadd__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__iadd__.double2",  double2,  _other)
    def __sub__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__sub__.double2",  double2,  _other)
    def __rsub__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__rsub__.double2",  double2,  _other)
    def __isub__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__isub__.double2",  double2,  _other)
    def __mul__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__mul__.double2",  double2,  _other)
    def __rmul__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__rmul__.double2",  double2,  _other)
    def __imul__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__imul__.double2",  double2,  _other)
    def __mod__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__mod__.double2",  double2,  _other)
    def __rmod__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__rmod__.double2",  double2,  _other)
    def __imod__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__imod__.double2",  double2,  _other)
    def __lt__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return intrinsic("cmp.__lt__.double2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return intrinsic("cmp.__le__.double2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return intrinsic("cmp.__gt__.double2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return intrinsic("cmp.__ge__.double2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return intrinsic("cmp.__eq__.double2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['double2', f64, float]) -> 'bool2': return intrinsic("cmp.__ne__.double2",  bool2,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__truediv__.double2",  double2,  _other)
    def __rtruediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__rtruediv__.double2",  double2,  _other)
    def __itruediv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__itruediv__.double2",  double2,  _other)
    def __pow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__pow__.double2",  double2,  _other)
    def __rpow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__rpow__.double2",  double2,  _other)
    def __ipow__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__ipow__.double2",  double2,  _other)
    def __floordiv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__floordiv__.double2",  double2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['double2', f64, float]) -> 'double2': return intrinsic("binop.__rfloordiv__.double2",  double2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8]), 2))
class byte2:
    x: i8
    y: i8
    def __init__(self, x: tp.Union['i8', int] = 0, y: tp.Union['i8', int] = 0) -> None: self = intrinsic("init.byte2", byte2, x, y)
    def __add__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__add__.byte2",  byte2,  _other)
    def __radd__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__radd__.byte2",  byte2,  _other)
    def __iadd__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__iadd__.byte2",  byte2,  _other)
    def __sub__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__sub__.byte2",  byte2,  _other)
    def __rsub__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rsub__.byte2",  byte2,  _other)
    def __isub__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__isub__.byte2",  byte2,  _other)
    def __mul__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__mul__.byte2",  byte2,  _other)
    def __rmul__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rmul__.byte2",  byte2,  _other)
    def __imul__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__imul__.byte2",  byte2,  _other)
    def __mod__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__mod__.byte2",  byte2,  _other)
    def __rmod__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rmod__.byte2",  byte2,  _other)
    def __imod__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__imod__.byte2",  byte2,  _other)
    def __lt__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return intrinsic("cmp.__lt__.byte2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return intrinsic("cmp.__le__.byte2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return intrinsic("cmp.__gt__.byte2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return intrinsic("cmp.__ge__.byte2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return intrinsic("cmp.__eq__.byte2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['byte2', i8, int]) -> 'bool2': return intrinsic("cmp.__ne__.byte2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__floordiv__.byte2",  byte2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rfloordiv__.byte2",  byte2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__ifloordiv__.byte2",  byte2,  _other)
    def __lshift__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__lshift__.byte2",  byte2,  _other)
    def __rlshift__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rlshift__.byte2",  byte2,  _other)
    def __ilshift__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__ilshift__.byte2",  byte2,  _other)
    def __rshift__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rshift__.byte2",  byte2,  _other)
    def __rrshift__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rrshift__.byte2",  byte2,  _other)
    def __irshift__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__irshift__.byte2",  byte2,  _other)
    def __and__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__and__.byte2",  byte2,  _other)
    def __rand__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rand__.byte2",  byte2,  _other)
    def __iand__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__iand__.byte2",  byte2,  _other)
    def __or__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__or__.byte2",  byte2,  _other)
    def __ror__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__ror__.byte2",  byte2,  _other)
    def __ior__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__ior__.byte2",  byte2,  _other)
    def __xor__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__xor__.byte2",  byte2,  _other)
    def __rxor__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__rxor__.byte2",  byte2,  _other)
    def __ixor__(self, _other:  tp.Union['byte2', i8, int]) -> 'byte2': return intrinsic("binop.__ixor__.byte2",  byte2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8]), 2))
class ubyte2:
    x: u8
    y: u8
    def __init__(self, x: tp.Union['u8', int] = 0, y: tp.Union['u8', int] = 0) -> None: self = intrinsic("init.ubyte2", ubyte2, x, y)
    def __add__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__add__.ubyte2",  ubyte2,  _other)
    def __radd__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__radd__.ubyte2",  ubyte2,  _other)
    def __iadd__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__iadd__.ubyte2",  ubyte2,  _other)
    def __sub__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__sub__.ubyte2",  ubyte2,  _other)
    def __rsub__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rsub__.ubyte2",  ubyte2,  _other)
    def __isub__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__isub__.ubyte2",  ubyte2,  _other)
    def __mul__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__mul__.ubyte2",  ubyte2,  _other)
    def __rmul__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rmul__.ubyte2",  ubyte2,  _other)
    def __imul__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__imul__.ubyte2",  ubyte2,  _other)
    def __mod__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__mod__.ubyte2",  ubyte2,  _other)
    def __rmod__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rmod__.ubyte2",  ubyte2,  _other)
    def __imod__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__imod__.ubyte2",  ubyte2,  _other)
    def __lt__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return intrinsic("cmp.__lt__.ubyte2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return intrinsic("cmp.__le__.ubyte2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return intrinsic("cmp.__gt__.ubyte2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return intrinsic("cmp.__ge__.ubyte2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return intrinsic("cmp.__eq__.ubyte2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'bool2': return intrinsic("cmp.__ne__.ubyte2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__floordiv__.ubyte2",  ubyte2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rfloordiv__.ubyte2",  ubyte2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__ifloordiv__.ubyte2",  ubyte2,  _other)
    def __lshift__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__lshift__.ubyte2",  ubyte2,  _other)
    def __rlshift__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rlshift__.ubyte2",  ubyte2,  _other)
    def __ilshift__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__ilshift__.ubyte2",  ubyte2,  _other)
    def __rshift__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rshift__.ubyte2",  ubyte2,  _other)
    def __rrshift__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rrshift__.ubyte2",  ubyte2,  _other)
    def __irshift__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__irshift__.ubyte2",  ubyte2,  _other)
    def __and__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__and__.ubyte2",  ubyte2,  _other)
    def __rand__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rand__.ubyte2",  ubyte2,  _other)
    def __iand__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__iand__.ubyte2",  ubyte2,  _other)
    def __or__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__or__.ubyte2",  ubyte2,  _other)
    def __ror__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__ror__.ubyte2",  ubyte2,  _other)
    def __ior__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__ior__.ubyte2",  ubyte2,  _other)
    def __xor__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__xor__.ubyte2",  ubyte2,  _other)
    def __rxor__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__rxor__.ubyte2",  ubyte2,  _other)
    def __ixor__(self, _other:  tp.Union['ubyte2', u8, int]) -> 'ubyte2': return intrinsic("binop.__ixor__.ubyte2",  ubyte2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16]), 2))
class short2:
    x: i16
    y: i16
    def __init__(self, x: tp.Union['i16', int] = 0, y: tp.Union['i16', int] = 0) -> None: self = intrinsic("init.short2", short2, x, y)
    def __add__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__add__.short2",  short2,  _other)
    def __radd__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__radd__.short2",  short2,  _other)
    def __iadd__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__iadd__.short2",  short2,  _other)
    def __sub__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__sub__.short2",  short2,  _other)
    def __rsub__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rsub__.short2",  short2,  _other)
    def __isub__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__isub__.short2",  short2,  _other)
    def __mul__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__mul__.short2",  short2,  _other)
    def __rmul__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rmul__.short2",  short2,  _other)
    def __imul__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__imul__.short2",  short2,  _other)
    def __mod__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__mod__.short2",  short2,  _other)
    def __rmod__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rmod__.short2",  short2,  _other)
    def __imod__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__imod__.short2",  short2,  _other)
    def __lt__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return intrinsic("cmp.__lt__.short2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return intrinsic("cmp.__le__.short2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return intrinsic("cmp.__gt__.short2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return intrinsic("cmp.__ge__.short2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return intrinsic("cmp.__eq__.short2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['short2', i16, int]) -> 'bool2': return intrinsic("cmp.__ne__.short2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__floordiv__.short2",  short2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rfloordiv__.short2",  short2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__ifloordiv__.short2",  short2,  _other)
    def __lshift__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__lshift__.short2",  short2,  _other)
    def __rlshift__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rlshift__.short2",  short2,  _other)
    def __ilshift__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__ilshift__.short2",  short2,  _other)
    def __rshift__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rshift__.short2",  short2,  _other)
    def __rrshift__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rrshift__.short2",  short2,  _other)
    def __irshift__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__irshift__.short2",  short2,  _other)
    def __and__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__and__.short2",  short2,  _other)
    def __rand__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rand__.short2",  short2,  _other)
    def __iand__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__iand__.short2",  short2,  _other)
    def __or__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__or__.short2",  short2,  _other)
    def __ror__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__ror__.short2",  short2,  _other)
    def __ior__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__ior__.short2",  short2,  _other)
    def __xor__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__xor__.short2",  short2,  _other)
    def __rxor__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__rxor__.short2",  short2,  _other)
    def __ixor__(self, _other:  tp.Union['short2', i16, int]) -> 'short2': return intrinsic("binop.__ixor__.short2",  short2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16]), 2))
class ushort2:
    x: u16
    y: u16
    def __init__(self, x: tp.Union['u16', int] = 0, y: tp.Union['u16', int] = 0) -> None: self = intrinsic("init.ushort2", ushort2, x, y)
    def __add__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__add__.ushort2",  ushort2,  _other)
    def __radd__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__radd__.ushort2",  ushort2,  _other)
    def __iadd__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__iadd__.ushort2",  ushort2,  _other)
    def __sub__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__sub__.ushort2",  ushort2,  _other)
    def __rsub__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rsub__.ushort2",  ushort2,  _other)
    def __isub__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__isub__.ushort2",  ushort2,  _other)
    def __mul__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__mul__.ushort2",  ushort2,  _other)
    def __rmul__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rmul__.ushort2",  ushort2,  _other)
    def __imul__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__imul__.ushort2",  ushort2,  _other)
    def __mod__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__mod__.ushort2",  ushort2,  _other)
    def __rmod__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rmod__.ushort2",  ushort2,  _other)
    def __imod__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__imod__.ushort2",  ushort2,  _other)
    def __lt__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return intrinsic("cmp.__lt__.ushort2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return intrinsic("cmp.__le__.ushort2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return intrinsic("cmp.__gt__.ushort2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return intrinsic("cmp.__ge__.ushort2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return intrinsic("cmp.__eq__.ushort2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ushort2', u16, int]) -> 'bool2': return intrinsic("cmp.__ne__.ushort2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__floordiv__.ushort2",  ushort2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rfloordiv__.ushort2",  ushort2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__ifloordiv__.ushort2",  ushort2,  _other)
    def __lshift__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__lshift__.ushort2",  ushort2,  _other)
    def __rlshift__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rlshift__.ushort2",  ushort2,  _other)
    def __ilshift__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__ilshift__.ushort2",  ushort2,  _other)
    def __rshift__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rshift__.ushort2",  ushort2,  _other)
    def __rrshift__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rrshift__.ushort2",  ushort2,  _other)
    def __irshift__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__irshift__.ushort2",  ushort2,  _other)
    def __and__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__and__.ushort2",  ushort2,  _other)
    def __rand__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rand__.ushort2",  ushort2,  _other)
    def __iand__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__iand__.ushort2",  ushort2,  _other)
    def __or__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__or__.ushort2",  ushort2,  _other)
    def __ror__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__ror__.ushort2",  ushort2,  _other)
    def __ior__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__ior__.ushort2",  ushort2,  _other)
    def __xor__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__xor__.ushort2",  ushort2,  _other)
    def __rxor__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__rxor__.ushort2",  ushort2,  _other)
    def __ixor__(self, _other:  tp.Union['ushort2', u16, int]) -> 'ushort2': return intrinsic("binop.__ixor__.ushort2",  ushort2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32]), 2))
class int2:
    x: i32
    y: i32
    def __init__(self, x: tp.Union['i32', int] = 0, y: tp.Union['i32', int] = 0) -> None: self = intrinsic("init.int2", int2, x, y)
    def __add__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__add__.int2",  int2,  _other)
    def __radd__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__radd__.int2",  int2,  _other)
    def __iadd__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__iadd__.int2",  int2,  _other)
    def __sub__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__sub__.int2",  int2,  _other)
    def __rsub__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rsub__.int2",  int2,  _other)
    def __isub__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__isub__.int2",  int2,  _other)
    def __mul__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__mul__.int2",  int2,  _other)
    def __rmul__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rmul__.int2",  int2,  _other)
    def __imul__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__imul__.int2",  int2,  _other)
    def __mod__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__mod__.int2",  int2,  _other)
    def __rmod__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rmod__.int2",  int2,  _other)
    def __imod__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__imod__.int2",  int2,  _other)
    def __lt__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return intrinsic("cmp.__lt__.int2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return intrinsic("cmp.__le__.int2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return intrinsic("cmp.__gt__.int2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return intrinsic("cmp.__ge__.int2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return intrinsic("cmp.__eq__.int2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['int2', i32, int]) -> 'bool2': return intrinsic("cmp.__ne__.int2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__floordiv__.int2",  int2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rfloordiv__.int2",  int2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__ifloordiv__.int2",  int2,  _other)
    def __lshift__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__lshift__.int2",  int2,  _other)
    def __rlshift__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rlshift__.int2",  int2,  _other)
    def __ilshift__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__ilshift__.int2",  int2,  _other)
    def __rshift__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rshift__.int2",  int2,  _other)
    def __rrshift__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rrshift__.int2",  int2,  _other)
    def __irshift__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__irshift__.int2",  int2,  _other)
    def __and__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__and__.int2",  int2,  _other)
    def __rand__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rand__.int2",  int2,  _other)
    def __iand__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__iand__.int2",  int2,  _other)
    def __or__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__or__.int2",  int2,  _other)
    def __ror__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__ror__.int2",  int2,  _other)
    def __ior__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__ior__.int2",  int2,  _other)
    def __xor__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__xor__.int2",  int2,  _other)
    def __rxor__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__rxor__.int2",  int2,  _other)
    def __ixor__(self, _other:  tp.Union['int2', i32, int]) -> 'int2': return intrinsic("binop.__ixor__.int2",  int2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32]), 2))
class uint2:
    x: u32
    y: u32
    def __init__(self, x: tp.Union['u32', int] = 0, y: tp.Union['u32', int] = 0) -> None: self = intrinsic("init.uint2", uint2, x, y)
    def __add__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__add__.uint2",  uint2,  _other)
    def __radd__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__radd__.uint2",  uint2,  _other)
    def __iadd__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__iadd__.uint2",  uint2,  _other)
    def __sub__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__sub__.uint2",  uint2,  _other)
    def __rsub__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rsub__.uint2",  uint2,  _other)
    def __isub__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__isub__.uint2",  uint2,  _other)
    def __mul__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__mul__.uint2",  uint2,  _other)
    def __rmul__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rmul__.uint2",  uint2,  _other)
    def __imul__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__imul__.uint2",  uint2,  _other)
    def __mod__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__mod__.uint2",  uint2,  _other)
    def __rmod__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rmod__.uint2",  uint2,  _other)
    def __imod__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__imod__.uint2",  uint2,  _other)
    def __lt__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return intrinsic("cmp.__lt__.uint2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return intrinsic("cmp.__le__.uint2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return intrinsic("cmp.__gt__.uint2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return intrinsic("cmp.__ge__.uint2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return intrinsic("cmp.__eq__.uint2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['uint2', u32, int]) -> 'bool2': return intrinsic("cmp.__ne__.uint2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__floordiv__.uint2",  uint2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rfloordiv__.uint2",  uint2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__ifloordiv__.uint2",  uint2,  _other)
    def __lshift__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__lshift__.uint2",  uint2,  _other)
    def __rlshift__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rlshift__.uint2",  uint2,  _other)
    def __ilshift__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__ilshift__.uint2",  uint2,  _other)
    def __rshift__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rshift__.uint2",  uint2,  _other)
    def __rrshift__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rrshift__.uint2",  uint2,  _other)
    def __irshift__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__irshift__.uint2",  uint2,  _other)
    def __and__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__and__.uint2",  uint2,  _other)
    def __rand__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rand__.uint2",  uint2,  _other)
    def __iand__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__iand__.uint2",  uint2,  _other)
    def __or__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__or__.uint2",  uint2,  _other)
    def __ror__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__ror__.uint2",  uint2,  _other)
    def __ior__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__ior__.uint2",  uint2,  _other)
    def __xor__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__xor__.uint2",  uint2,  _other)
    def __rxor__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__rxor__.uint2",  uint2,  _other)
    def __ixor__(self, _other:  tp.Union['uint2', u32, int]) -> 'uint2': return intrinsic("binop.__ixor__.uint2",  uint2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64]), 2))
class long2:
    x: i64
    y: i64
    def __init__(self, x: tp.Union['i64', int] = 0, y: tp.Union['i64', int] = 0) -> None: self = intrinsic("init.long2", long2, x, y)
    def __add__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__add__.long2",  long2,  _other)
    def __radd__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__radd__.long2",  long2,  _other)
    def __iadd__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__iadd__.long2",  long2,  _other)
    def __sub__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__sub__.long2",  long2,  _other)
    def __rsub__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rsub__.long2",  long2,  _other)
    def __isub__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__isub__.long2",  long2,  _other)
    def __mul__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__mul__.long2",  long2,  _other)
    def __rmul__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rmul__.long2",  long2,  _other)
    def __imul__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__imul__.long2",  long2,  _other)
    def __mod__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__mod__.long2",  long2,  _other)
    def __rmod__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rmod__.long2",  long2,  _other)
    def __imod__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__imod__.long2",  long2,  _other)
    def __lt__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return intrinsic("cmp.__lt__.long2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return intrinsic("cmp.__le__.long2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return intrinsic("cmp.__gt__.long2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return intrinsic("cmp.__ge__.long2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return intrinsic("cmp.__eq__.long2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['long2', i64, int]) -> 'bool2': return intrinsic("cmp.__ne__.long2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__floordiv__.long2",  long2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rfloordiv__.long2",  long2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__ifloordiv__.long2",  long2,  _other)
    def __lshift__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__lshift__.long2",  long2,  _other)
    def __rlshift__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rlshift__.long2",  long2,  _other)
    def __ilshift__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__ilshift__.long2",  long2,  _other)
    def __rshift__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rshift__.long2",  long2,  _other)
    def __rrshift__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rrshift__.long2",  long2,  _other)
    def __irshift__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__irshift__.long2",  long2,  _other)
    def __and__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__and__.long2",  long2,  _other)
    def __rand__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rand__.long2",  long2,  _other)
    def __iand__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__iand__.long2",  long2,  _other)
    def __or__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__or__.long2",  long2,  _other)
    def __ror__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__ror__.long2",  long2,  _other)
    def __ior__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__ior__.long2",  long2,  _other)
    def __xor__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__xor__.long2",  long2,  _other)
    def __rxor__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__rxor__.long2",  long2,  _other)
    def __ixor__(self, _other:  tp.Union['long2', i64, int]) -> 'long2': return intrinsic("binop.__ixor__.long2",  long2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64]), 2))
class ulong2:
    x: u64
    y: u64
    def __init__(self, x: tp.Union['u64', int] = 0, y: tp.Union['u64', int] = 0) -> None: self = intrinsic("init.ulong2", ulong2, x, y)
    def __add__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__add__.ulong2",  ulong2,  _other)
    def __radd__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__radd__.ulong2",  ulong2,  _other)
    def __iadd__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__iadd__.ulong2",  ulong2,  _other)
    def __sub__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__sub__.ulong2",  ulong2,  _other)
    def __rsub__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rsub__.ulong2",  ulong2,  _other)
    def __isub__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__isub__.ulong2",  ulong2,  _other)
    def __mul__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__mul__.ulong2",  ulong2,  _other)
    def __rmul__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rmul__.ulong2",  ulong2,  _other)
    def __imul__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__imul__.ulong2",  ulong2,  _other)
    def __mod__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__mod__.ulong2",  ulong2,  _other)
    def __rmod__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rmod__.ulong2",  ulong2,  _other)
    def __imod__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__imod__.ulong2",  ulong2,  _other)
    def __lt__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return intrinsic("cmp.__lt__.ulong2",  bool2,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return intrinsic("cmp.__le__.ulong2",  bool2,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return intrinsic("cmp.__gt__.ulong2",  bool2,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return intrinsic("cmp.__ge__.ulong2",  bool2,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return intrinsic("cmp.__eq__.ulong2",  bool2,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ulong2', u64, int]) -> 'bool2': return intrinsic("cmp.__ne__.ulong2",  bool2,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__floordiv__.ulong2",  ulong2,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rfloordiv__.ulong2",  ulong2,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__ifloordiv__.ulong2",  ulong2,  _other)
    def __lshift__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__lshift__.ulong2",  ulong2,  _other)
    def __rlshift__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rlshift__.ulong2",  ulong2,  _other)
    def __ilshift__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__ilshift__.ulong2",  ulong2,  _other)
    def __rshift__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rshift__.ulong2",  ulong2,  _other)
    def __rrshift__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rrshift__.ulong2",  ulong2,  _other)
    def __irshift__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__irshift__.ulong2",  ulong2,  _other)
    def __and__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__and__.ulong2",  ulong2,  _other)
    def __rand__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rand__.ulong2",  ulong2,  _other)
    def __iand__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__iand__.ulong2",  ulong2,  _other)
    def __or__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__or__.ulong2",  ulong2,  _other)
    def __ror__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__ror__.ulong2",  ulong2,  _other)
    def __ior__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__ior__.ulong2",  ulong2,  _other)
    def __xor__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__xor__.ulong2",  ulong2,  _other)
    def __rxor__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__rxor__.ulong2",  ulong2,  _other)
    def __ixor__(self, _other:  tp.Union['ulong2', u64, int]) -> 'ulong2': return intrinsic("binop.__ixor__.ulong2",  ulong2,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[bool]), 3))
class bool3:
    x: bool
    y: bool
    z: bool
    def __init__(self, x: tp.Union['bool', bool] = False, y: tp.Union['bool', bool] = False, z: tp.Union['bool', bool] = False) -> None: self = intrinsic("init.bool3", bool3, x, y, z)
    def __eq__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("cmp.__eq__.bool3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("cmp.__ne__.bool3",  bool3,  _other) # type: ignore[override]
    def __and__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__and__.bool3",  bool3,  _other)
    def __rand__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__rand__.bool3",  bool3,  _other)
    def __iand__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__iand__.bool3",  bool3,  _other)
    def __or__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__or__.bool3",  bool3,  _other)
    def __ror__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__ror__.bool3",  bool3,  _other)
    def __ior__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__ior__.bool3",  bool3,  _other)
    def __xor__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__xor__.bool3",  bool3,  _other)
    def __rxor__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__rxor__.bool3",  bool3,  _other)
    def __ixor__(self, _other:  tp.Union['bool3', bool, bool]) -> 'bool3': return intrinsic("binop.__ixor__.bool3",  bool3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32]), 3))
class float3(FloatBuiltin['float3']):
    x: f32
    y: f32
    z: f32
    def __init__(self, x: tp.Union['f32', float] = 0.0, y: tp.Union['f32', float] = 0.0, z: tp.Union['f32', float] = 0.0) -> None: self = intrinsic("init.float3", float3, x, y, z)
    def __add__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__add__.float3",  float3,  _other)
    def __radd__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__radd__.float3",  float3,  _other)
    def __iadd__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__iadd__.float3",  float3,  _other)
    def __sub__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__sub__.float3",  float3,  _other)
    def __rsub__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__rsub__.float3",  float3,  _other)
    def __isub__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__isub__.float3",  float3,  _other)
    def __mul__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__mul__.float3",  float3,  _other)
    def __rmul__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__rmul__.float3",  float3,  _other)
    def __imul__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__imul__.float3",  float3,  _other)
    def __mod__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__mod__.float3",  float3,  _other)
    def __rmod__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__rmod__.float3",  float3,  _other)
    def __imod__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__imod__.float3",  float3,  _other)
    def __lt__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return intrinsic("cmp.__lt__.float3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return intrinsic("cmp.__le__.float3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return intrinsic("cmp.__gt__.float3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return intrinsic("cmp.__ge__.float3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return intrinsic("cmp.__eq__.float3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['float3', f32, float]) -> 'bool3': return intrinsic("cmp.__ne__.float3",  bool3,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__truediv__.float3",  float3,  _other)
    def __rtruediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__rtruediv__.float3",  float3,  _other)
    def __itruediv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__itruediv__.float3",  float3,  _other)
    def __pow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__pow__.float3",  float3,  _other)
    def __rpow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__rpow__.float3",  float3,  _other)
    def __ipow__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__ipow__.float3",  float3,  _other)
    def __floordiv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__floordiv__.float3",  float3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['float3', f32, float]) -> 'float3': return intrinsic("binop.__rfloordiv__.float3",  float3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64]), 3))
class double3(FloatBuiltin['double3']):
    x: f64
    y: f64
    z: f64
    def __init__(self, x: tp.Union['f64', float] = 0.0, y: tp.Union['f64', float] = 0.0, z: tp.Union['f64', float] = 0.0) -> None: self = intrinsic("init.double3", double3, x, y, z)
    def __add__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__add__.double3",  double3,  _other)
    def __radd__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__radd__.double3",  double3,  _other)
    def __iadd__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__iadd__.double3",  double3,  _other)
    def __sub__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__sub__.double3",  double3,  _other)
    def __rsub__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__rsub__.double3",  double3,  _other)
    def __isub__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__isub__.double3",  double3,  _other)
    def __mul__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__mul__.double3",  double3,  _other)
    def __rmul__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__rmul__.double3",  double3,  _other)
    def __imul__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__imul__.double3",  double3,  _other)
    def __mod__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__mod__.double3",  double3,  _other)
    def __rmod__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__rmod__.double3",  double3,  _other)
    def __imod__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__imod__.double3",  double3,  _other)
    def __lt__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return intrinsic("cmp.__lt__.double3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return intrinsic("cmp.__le__.double3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return intrinsic("cmp.__gt__.double3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return intrinsic("cmp.__ge__.double3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return intrinsic("cmp.__eq__.double3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['double3', f64, float]) -> 'bool3': return intrinsic("cmp.__ne__.double3",  bool3,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__truediv__.double3",  double3,  _other)
    def __rtruediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__rtruediv__.double3",  double3,  _other)
    def __itruediv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__itruediv__.double3",  double3,  _other)
    def __pow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__pow__.double3",  double3,  _other)
    def __rpow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__rpow__.double3",  double3,  _other)
    def __ipow__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__ipow__.double3",  double3,  _other)
    def __floordiv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__floordiv__.double3",  double3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['double3', f64, float]) -> 'double3': return intrinsic("binop.__rfloordiv__.double3",  double3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8]), 3))
class byte3:
    x: i8
    y: i8
    z: i8
    def __init__(self, x: tp.Union['i8', int] = 0, y: tp.Union['i8', int] = 0, z: tp.Union['i8', int] = 0) -> None: self = intrinsic("init.byte3", byte3, x, y, z)
    def __add__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__add__.byte3",  byte3,  _other)
    def __radd__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__radd__.byte3",  byte3,  _other)
    def __iadd__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__iadd__.byte3",  byte3,  _other)
    def __sub__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__sub__.byte3",  byte3,  _other)
    def __rsub__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rsub__.byte3",  byte3,  _other)
    def __isub__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__isub__.byte3",  byte3,  _other)
    def __mul__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__mul__.byte3",  byte3,  _other)
    def __rmul__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rmul__.byte3",  byte3,  _other)
    def __imul__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__imul__.byte3",  byte3,  _other)
    def __mod__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__mod__.byte3",  byte3,  _other)
    def __rmod__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rmod__.byte3",  byte3,  _other)
    def __imod__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__imod__.byte3",  byte3,  _other)
    def __lt__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return intrinsic("cmp.__lt__.byte3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return intrinsic("cmp.__le__.byte3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return intrinsic("cmp.__gt__.byte3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return intrinsic("cmp.__ge__.byte3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return intrinsic("cmp.__eq__.byte3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['byte3', i8, int]) -> 'bool3': return intrinsic("cmp.__ne__.byte3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__floordiv__.byte3",  byte3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rfloordiv__.byte3",  byte3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__ifloordiv__.byte3",  byte3,  _other)
    def __lshift__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__lshift__.byte3",  byte3,  _other)
    def __rlshift__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rlshift__.byte3",  byte3,  _other)
    def __ilshift__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__ilshift__.byte3",  byte3,  _other)
    def __rshift__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rshift__.byte3",  byte3,  _other)
    def __rrshift__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rrshift__.byte3",  byte3,  _other)
    def __irshift__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__irshift__.byte3",  byte3,  _other)
    def __and__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__and__.byte3",  byte3,  _other)
    def __rand__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rand__.byte3",  byte3,  _other)
    def __iand__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__iand__.byte3",  byte3,  _other)
    def __or__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__or__.byte3",  byte3,  _other)
    def __ror__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__ror__.byte3",  byte3,  _other)
    def __ior__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__ior__.byte3",  byte3,  _other)
    def __xor__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__xor__.byte3",  byte3,  _other)
    def __rxor__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__rxor__.byte3",  byte3,  _other)
    def __ixor__(self, _other:  tp.Union['byte3', i8, int]) -> 'byte3': return intrinsic("binop.__ixor__.byte3",  byte3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8]), 3))
class ubyte3:
    x: u8
    y: u8
    z: u8
    def __init__(self, x: tp.Union['u8', int] = 0, y: tp.Union['u8', int] = 0, z: tp.Union['u8', int] = 0) -> None: self = intrinsic("init.ubyte3", ubyte3, x, y, z)
    def __add__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__add__.ubyte3",  ubyte3,  _other)
    def __radd__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__radd__.ubyte3",  ubyte3,  _other)
    def __iadd__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__iadd__.ubyte3",  ubyte3,  _other)
    def __sub__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__sub__.ubyte3",  ubyte3,  _other)
    def __rsub__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rsub__.ubyte3",  ubyte3,  _other)
    def __isub__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__isub__.ubyte3",  ubyte3,  _other)
    def __mul__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__mul__.ubyte3",  ubyte3,  _other)
    def __rmul__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rmul__.ubyte3",  ubyte3,  _other)
    def __imul__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__imul__.ubyte3",  ubyte3,  _other)
    def __mod__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__mod__.ubyte3",  ubyte3,  _other)
    def __rmod__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rmod__.ubyte3",  ubyte3,  _other)
    def __imod__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__imod__.ubyte3",  ubyte3,  _other)
    def __lt__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return intrinsic("cmp.__lt__.ubyte3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return intrinsic("cmp.__le__.ubyte3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return intrinsic("cmp.__gt__.ubyte3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return intrinsic("cmp.__ge__.ubyte3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return intrinsic("cmp.__eq__.ubyte3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'bool3': return intrinsic("cmp.__ne__.ubyte3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__floordiv__.ubyte3",  ubyte3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rfloordiv__.ubyte3",  ubyte3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__ifloordiv__.ubyte3",  ubyte3,  _other)
    def __lshift__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__lshift__.ubyte3",  ubyte3,  _other)
    def __rlshift__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rlshift__.ubyte3",  ubyte3,  _other)
    def __ilshift__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__ilshift__.ubyte3",  ubyte3,  _other)
    def __rshift__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rshift__.ubyte3",  ubyte3,  _other)
    def __rrshift__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rrshift__.ubyte3",  ubyte3,  _other)
    def __irshift__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__irshift__.ubyte3",  ubyte3,  _other)
    def __and__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__and__.ubyte3",  ubyte3,  _other)
    def __rand__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rand__.ubyte3",  ubyte3,  _other)
    def __iand__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__iand__.ubyte3",  ubyte3,  _other)
    def __or__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__or__.ubyte3",  ubyte3,  _other)
    def __ror__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__ror__.ubyte3",  ubyte3,  _other)
    def __ior__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__ior__.ubyte3",  ubyte3,  _other)
    def __xor__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__xor__.ubyte3",  ubyte3,  _other)
    def __rxor__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__rxor__.ubyte3",  ubyte3,  _other)
    def __ixor__(self, _other:  tp.Union['ubyte3', u8, int]) -> 'ubyte3': return intrinsic("binop.__ixor__.ubyte3",  ubyte3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16]), 3))
class short3:
    x: i16
    y: i16
    z: i16
    def __init__(self, x: tp.Union['i16', int] = 0, y: tp.Union['i16', int] = 0, z: tp.Union['i16', int] = 0) -> None: self = intrinsic("init.short3", short3, x, y, z)
    def __add__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__add__.short3",  short3,  _other)
    def __radd__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__radd__.short3",  short3,  _other)
    def __iadd__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__iadd__.short3",  short3,  _other)
    def __sub__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__sub__.short3",  short3,  _other)
    def __rsub__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rsub__.short3",  short3,  _other)
    def __isub__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__isub__.short3",  short3,  _other)
    def __mul__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__mul__.short3",  short3,  _other)
    def __rmul__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rmul__.short3",  short3,  _other)
    def __imul__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__imul__.short3",  short3,  _other)
    def __mod__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__mod__.short3",  short3,  _other)
    def __rmod__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rmod__.short3",  short3,  _other)
    def __imod__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__imod__.short3",  short3,  _other)
    def __lt__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return intrinsic("cmp.__lt__.short3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return intrinsic("cmp.__le__.short3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return intrinsic("cmp.__gt__.short3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return intrinsic("cmp.__ge__.short3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return intrinsic("cmp.__eq__.short3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['short3', i16, int]) -> 'bool3': return intrinsic("cmp.__ne__.short3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__floordiv__.short3",  short3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rfloordiv__.short3",  short3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__ifloordiv__.short3",  short3,  _other)
    def __lshift__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__lshift__.short3",  short3,  _other)
    def __rlshift__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rlshift__.short3",  short3,  _other)
    def __ilshift__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__ilshift__.short3",  short3,  _other)
    def __rshift__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rshift__.short3",  short3,  _other)
    def __rrshift__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rrshift__.short3",  short3,  _other)
    def __irshift__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__irshift__.short3",  short3,  _other)
    def __and__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__and__.short3",  short3,  _other)
    def __rand__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rand__.short3",  short3,  _other)
    def __iand__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__iand__.short3",  short3,  _other)
    def __or__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__or__.short3",  short3,  _other)
    def __ror__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__ror__.short3",  short3,  _other)
    def __ior__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__ior__.short3",  short3,  _other)
    def __xor__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__xor__.short3",  short3,  _other)
    def __rxor__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__rxor__.short3",  short3,  _other)
    def __ixor__(self, _other:  tp.Union['short3', i16, int]) -> 'short3': return intrinsic("binop.__ixor__.short3",  short3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16]), 3))
class ushort3:
    x: u16
    y: u16
    z: u16
    def __init__(self, x: tp.Union['u16', int] = 0, y: tp.Union['u16', int] = 0, z: tp.Union['u16', int] = 0) -> None: self = intrinsic("init.ushort3", ushort3, x, y, z)
    def __add__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__add__.ushort3",  ushort3,  _other)
    def __radd__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__radd__.ushort3",  ushort3,  _other)
    def __iadd__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__iadd__.ushort3",  ushort3,  _other)
    def __sub__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__sub__.ushort3",  ushort3,  _other)
    def __rsub__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rsub__.ushort3",  ushort3,  _other)
    def __isub__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__isub__.ushort3",  ushort3,  _other)
    def __mul__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__mul__.ushort3",  ushort3,  _other)
    def __rmul__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rmul__.ushort3",  ushort3,  _other)
    def __imul__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__imul__.ushort3",  ushort3,  _other)
    def __mod__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__mod__.ushort3",  ushort3,  _other)
    def __rmod__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rmod__.ushort3",  ushort3,  _other)
    def __imod__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__imod__.ushort3",  ushort3,  _other)
    def __lt__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return intrinsic("cmp.__lt__.ushort3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return intrinsic("cmp.__le__.ushort3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return intrinsic("cmp.__gt__.ushort3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return intrinsic("cmp.__ge__.ushort3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return intrinsic("cmp.__eq__.ushort3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ushort3', u16, int]) -> 'bool3': return intrinsic("cmp.__ne__.ushort3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__floordiv__.ushort3",  ushort3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rfloordiv__.ushort3",  ushort3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__ifloordiv__.ushort3",  ushort3,  _other)
    def __lshift__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__lshift__.ushort3",  ushort3,  _other)
    def __rlshift__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rlshift__.ushort3",  ushort3,  _other)
    def __ilshift__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__ilshift__.ushort3",  ushort3,  _other)
    def __rshift__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rshift__.ushort3",  ushort3,  _other)
    def __rrshift__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rrshift__.ushort3",  ushort3,  _other)
    def __irshift__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__irshift__.ushort3",  ushort3,  _other)
    def __and__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__and__.ushort3",  ushort3,  _other)
    def __rand__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rand__.ushort3",  ushort3,  _other)
    def __iand__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__iand__.ushort3",  ushort3,  _other)
    def __or__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__or__.ushort3",  ushort3,  _other)
    def __ror__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__ror__.ushort3",  ushort3,  _other)
    def __ior__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__ior__.ushort3",  ushort3,  _other)
    def __xor__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__xor__.ushort3",  ushort3,  _other)
    def __rxor__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__rxor__.ushort3",  ushort3,  _other)
    def __ixor__(self, _other:  tp.Union['ushort3', u16, int]) -> 'ushort3': return intrinsic("binop.__ixor__.ushort3",  ushort3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32]), 3))
class int3:
    x: i32
    y: i32
    z: i32
    def __init__(self, x: tp.Union['i32', int] = 0, y: tp.Union['i32', int] = 0, z: tp.Union['i32', int] = 0) -> None: self = intrinsic("init.int3", int3, x, y, z)
    def __add__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__add__.int3",  int3,  _other)
    def __radd__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__radd__.int3",  int3,  _other)
    def __iadd__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__iadd__.int3",  int3,  _other)
    def __sub__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__sub__.int3",  int3,  _other)
    def __rsub__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rsub__.int3",  int3,  _other)
    def __isub__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__isub__.int3",  int3,  _other)
    def __mul__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__mul__.int3",  int3,  _other)
    def __rmul__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rmul__.int3",  int3,  _other)
    def __imul__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__imul__.int3",  int3,  _other)
    def __mod__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__mod__.int3",  int3,  _other)
    def __rmod__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rmod__.int3",  int3,  _other)
    def __imod__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__imod__.int3",  int3,  _other)
    def __lt__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return intrinsic("cmp.__lt__.int3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return intrinsic("cmp.__le__.int3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return intrinsic("cmp.__gt__.int3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return intrinsic("cmp.__ge__.int3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return intrinsic("cmp.__eq__.int3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['int3', i32, int]) -> 'bool3': return intrinsic("cmp.__ne__.int3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__floordiv__.int3",  int3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rfloordiv__.int3",  int3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__ifloordiv__.int3",  int3,  _other)
    def __lshift__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__lshift__.int3",  int3,  _other)
    def __rlshift__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rlshift__.int3",  int3,  _other)
    def __ilshift__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__ilshift__.int3",  int3,  _other)
    def __rshift__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rshift__.int3",  int3,  _other)
    def __rrshift__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rrshift__.int3",  int3,  _other)
    def __irshift__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__irshift__.int3",  int3,  _other)
    def __and__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__and__.int3",  int3,  _other)
    def __rand__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rand__.int3",  int3,  _other)
    def __iand__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__iand__.int3",  int3,  _other)
    def __or__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__or__.int3",  int3,  _other)
    def __ror__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__ror__.int3",  int3,  _other)
    def __ior__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__ior__.int3",  int3,  _other)
    def __xor__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__xor__.int3",  int3,  _other)
    def __rxor__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__rxor__.int3",  int3,  _other)
    def __ixor__(self, _other:  tp.Union['int3', i32, int]) -> 'int3': return intrinsic("binop.__ixor__.int3",  int3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32]), 3))
class uint3:
    x: u32
    y: u32
    z: u32
    def __init__(self, x: tp.Union['u32', int] = 0, y: tp.Union['u32', int] = 0, z: tp.Union['u32', int] = 0) -> None: self = intrinsic("init.uint3", uint3, x, y, z)
    def __add__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__add__.uint3",  uint3,  _other)
    def __radd__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__radd__.uint3",  uint3,  _other)
    def __iadd__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__iadd__.uint3",  uint3,  _other)
    def __sub__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__sub__.uint3",  uint3,  _other)
    def __rsub__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rsub__.uint3",  uint3,  _other)
    def __isub__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__isub__.uint3",  uint3,  _other)
    def __mul__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__mul__.uint3",  uint3,  _other)
    def __rmul__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rmul__.uint3",  uint3,  _other)
    def __imul__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__imul__.uint3",  uint3,  _other)
    def __mod__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__mod__.uint3",  uint3,  _other)
    def __rmod__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rmod__.uint3",  uint3,  _other)
    def __imod__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__imod__.uint3",  uint3,  _other)
    def __lt__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return intrinsic("cmp.__lt__.uint3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return intrinsic("cmp.__le__.uint3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return intrinsic("cmp.__gt__.uint3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return intrinsic("cmp.__ge__.uint3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return intrinsic("cmp.__eq__.uint3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['uint3', u32, int]) -> 'bool3': return intrinsic("cmp.__ne__.uint3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__floordiv__.uint3",  uint3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rfloordiv__.uint3",  uint3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__ifloordiv__.uint3",  uint3,  _other)
    def __lshift__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__lshift__.uint3",  uint3,  _other)
    def __rlshift__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rlshift__.uint3",  uint3,  _other)
    def __ilshift__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__ilshift__.uint3",  uint3,  _other)
    def __rshift__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rshift__.uint3",  uint3,  _other)
    def __rrshift__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rrshift__.uint3",  uint3,  _other)
    def __irshift__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__irshift__.uint3",  uint3,  _other)
    def __and__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__and__.uint3",  uint3,  _other)
    def __rand__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rand__.uint3",  uint3,  _other)
    def __iand__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__iand__.uint3",  uint3,  _other)
    def __or__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__or__.uint3",  uint3,  _other)
    def __ror__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__ror__.uint3",  uint3,  _other)
    def __ior__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__ior__.uint3",  uint3,  _other)
    def __xor__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__xor__.uint3",  uint3,  _other)
    def __rxor__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__rxor__.uint3",  uint3,  _other)
    def __ixor__(self, _other:  tp.Union['uint3', u32, int]) -> 'uint3': return intrinsic("binop.__ixor__.uint3",  uint3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64]), 3))
class long3:
    x: i64
    y: i64
    z: i64
    def __init__(self, x: tp.Union['i64', int] = 0, y: tp.Union['i64', int] = 0, z: tp.Union['i64', int] = 0) -> None: self = intrinsic("init.long3", long3, x, y, z)
    def __add__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__add__.long3",  long3,  _other)
    def __radd__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__radd__.long3",  long3,  _other)
    def __iadd__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__iadd__.long3",  long3,  _other)
    def __sub__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__sub__.long3",  long3,  _other)
    def __rsub__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rsub__.long3",  long3,  _other)
    def __isub__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__isub__.long3",  long3,  _other)
    def __mul__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__mul__.long3",  long3,  _other)
    def __rmul__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rmul__.long3",  long3,  _other)
    def __imul__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__imul__.long3",  long3,  _other)
    def __mod__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__mod__.long3",  long3,  _other)
    def __rmod__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rmod__.long3",  long3,  _other)
    def __imod__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__imod__.long3",  long3,  _other)
    def __lt__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return intrinsic("cmp.__lt__.long3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return intrinsic("cmp.__le__.long3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return intrinsic("cmp.__gt__.long3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return intrinsic("cmp.__ge__.long3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return intrinsic("cmp.__eq__.long3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['long3', i64, int]) -> 'bool3': return intrinsic("cmp.__ne__.long3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__floordiv__.long3",  long3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rfloordiv__.long3",  long3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__ifloordiv__.long3",  long3,  _other)
    def __lshift__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__lshift__.long3",  long3,  _other)
    def __rlshift__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rlshift__.long3",  long3,  _other)
    def __ilshift__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__ilshift__.long3",  long3,  _other)
    def __rshift__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rshift__.long3",  long3,  _other)
    def __rrshift__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rrshift__.long3",  long3,  _other)
    def __irshift__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__irshift__.long3",  long3,  _other)
    def __and__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__and__.long3",  long3,  _other)
    def __rand__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rand__.long3",  long3,  _other)
    def __iand__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__iand__.long3",  long3,  _other)
    def __or__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__or__.long3",  long3,  _other)
    def __ror__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__ror__.long3",  long3,  _other)
    def __ior__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__ior__.long3",  long3,  _other)
    def __xor__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__xor__.long3",  long3,  _other)
    def __rxor__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__rxor__.long3",  long3,  _other)
    def __ixor__(self, _other:  tp.Union['long3', i64, int]) -> 'long3': return intrinsic("binop.__ixor__.long3",  long3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64]), 3))
class ulong3:
    x: u64
    y: u64
    z: u64
    def __init__(self, x: tp.Union['u64', int] = 0, y: tp.Union['u64', int] = 0, z: tp.Union['u64', int] = 0) -> None: self = intrinsic("init.ulong3", ulong3, x, y, z)
    def __add__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__add__.ulong3",  ulong3,  _other)
    def __radd__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__radd__.ulong3",  ulong3,  _other)
    def __iadd__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__iadd__.ulong3",  ulong3,  _other)
    def __sub__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__sub__.ulong3",  ulong3,  _other)
    def __rsub__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rsub__.ulong3",  ulong3,  _other)
    def __isub__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__isub__.ulong3",  ulong3,  _other)
    def __mul__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__mul__.ulong3",  ulong3,  _other)
    def __rmul__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rmul__.ulong3",  ulong3,  _other)
    def __imul__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__imul__.ulong3",  ulong3,  _other)
    def __mod__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__mod__.ulong3",  ulong3,  _other)
    def __rmod__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rmod__.ulong3",  ulong3,  _other)
    def __imod__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__imod__.ulong3",  ulong3,  _other)
    def __lt__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return intrinsic("cmp.__lt__.ulong3",  bool3,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return intrinsic("cmp.__le__.ulong3",  bool3,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return intrinsic("cmp.__gt__.ulong3",  bool3,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return intrinsic("cmp.__ge__.ulong3",  bool3,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return intrinsic("cmp.__eq__.ulong3",  bool3,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ulong3', u64, int]) -> 'bool3': return intrinsic("cmp.__ne__.ulong3",  bool3,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__floordiv__.ulong3",  ulong3,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rfloordiv__.ulong3",  ulong3,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__ifloordiv__.ulong3",  ulong3,  _other)
    def __lshift__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__lshift__.ulong3",  ulong3,  _other)
    def __rlshift__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rlshift__.ulong3",  ulong3,  _other)
    def __ilshift__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__ilshift__.ulong3",  ulong3,  _other)
    def __rshift__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rshift__.ulong3",  ulong3,  _other)
    def __rrshift__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rrshift__.ulong3",  ulong3,  _other)
    def __irshift__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__irshift__.ulong3",  ulong3,  _other)
    def __and__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__and__.ulong3",  ulong3,  _other)
    def __rand__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rand__.ulong3",  ulong3,  _other)
    def __iand__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__iand__.ulong3",  ulong3,  _other)
    def __or__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__or__.ulong3",  ulong3,  _other)
    def __ror__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__ror__.ulong3",  ulong3,  _other)
    def __ior__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__ior__.ulong3",  ulong3,  _other)
    def __xor__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__xor__.ulong3",  ulong3,  _other)
    def __rxor__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__rxor__.ulong3",  ulong3,  _other)
    def __ixor__(self, _other:  tp.Union['ulong3', u64, int]) -> 'ulong3': return intrinsic("binop.__ixor__.ulong3",  ulong3,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[bool]), 4))
class bool4:
    x: bool
    y: bool
    z: bool
    w: bool
    def __init__(self, x: tp.Union['bool', bool] = False, y: tp.Union['bool', bool] = False, z: tp.Union['bool', bool] = False, w: tp.Union['bool', bool] = False) -> None: self = intrinsic("init.bool4", bool4, x, y, z, w)
    def __eq__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("cmp.__eq__.bool4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("cmp.__ne__.bool4",  bool4,  _other) # type: ignore[override]
    def __and__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__and__.bool4",  bool4,  _other)
    def __rand__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__rand__.bool4",  bool4,  _other)
    def __iand__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__iand__.bool4",  bool4,  _other)
    def __or__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__or__.bool4",  bool4,  _other)
    def __ror__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__ror__.bool4",  bool4,  _other)
    def __ior__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__ior__.bool4",  bool4,  _other)
    def __xor__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__xor__.bool4",  bool4,  _other)
    def __rxor__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__rxor__.bool4",  bool4,  _other)
    def __ixor__(self, _other:  tp.Union['bool4', bool, bool]) -> 'bool4': return intrinsic("binop.__ixor__.bool4",  bool4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32]), 4))
class float4(FloatBuiltin['float4']):
    x: f32
    y: f32
    z: f32
    w: f32
    def __init__(self, x: tp.Union['f32', float] = 0.0, y: tp.Union['f32', float] = 0.0, z: tp.Union['f32', float] = 0.0, w: tp.Union['f32', float] = 0.0) -> None: self = intrinsic("init.float4", float4, x, y, z, w)
    def __add__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__add__.float4",  float4,  _other)
    def __radd__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__radd__.float4",  float4,  _other)
    def __iadd__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__iadd__.float4",  float4,  _other)
    def __sub__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__sub__.float4",  float4,  _other)
    def __rsub__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__rsub__.float4",  float4,  _other)
    def __isub__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__isub__.float4",  float4,  _other)
    def __mul__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__mul__.float4",  float4,  _other)
    def __rmul__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__rmul__.float4",  float4,  _other)
    def __imul__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__imul__.float4",  float4,  _other)
    def __mod__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__mod__.float4",  float4,  _other)
    def __rmod__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__rmod__.float4",  float4,  _other)
    def __imod__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__imod__.float4",  float4,  _other)
    def __lt__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return intrinsic("cmp.__lt__.float4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return intrinsic("cmp.__le__.float4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return intrinsic("cmp.__gt__.float4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return intrinsic("cmp.__ge__.float4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return intrinsic("cmp.__eq__.float4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['float4', f32, float]) -> 'bool4': return intrinsic("cmp.__ne__.float4",  bool4,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__truediv__.float4",  float4,  _other)
    def __rtruediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__rtruediv__.float4",  float4,  _other)
    def __itruediv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__itruediv__.float4",  float4,  _other)
    def __pow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__pow__.float4",  float4,  _other)
    def __rpow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__rpow__.float4",  float4,  _other)
    def __ipow__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__ipow__.float4",  float4,  _other)
    def __floordiv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__floordiv__.float4",  float4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['float4', f32, float]) -> 'float4': return intrinsic("binop.__rfloordiv__.float4",  float4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64]), 4))
class double4(FloatBuiltin['double4']):
    x: f64
    y: f64
    z: f64
    w: f64
    def __init__(self, x: tp.Union['f64', float] = 0.0, y: tp.Union['f64', float] = 0.0, z: tp.Union['f64', float] = 0.0, w: tp.Union['f64', float] = 0.0) -> None: self = intrinsic("init.double4", double4, x, y, z, w)
    def __add__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__add__.double4",  double4,  _other)
    def __radd__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__radd__.double4",  double4,  _other)
    def __iadd__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__iadd__.double4",  double4,  _other)
    def __sub__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__sub__.double4",  double4,  _other)
    def __rsub__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__rsub__.double4",  double4,  _other)
    def __isub__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__isub__.double4",  double4,  _other)
    def __mul__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__mul__.double4",  double4,  _other)
    def __rmul__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__rmul__.double4",  double4,  _other)
    def __imul__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__imul__.double4",  double4,  _other)
    def __mod__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__mod__.double4",  double4,  _other)
    def __rmod__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__rmod__.double4",  double4,  _other)
    def __imod__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__imod__.double4",  double4,  _other)
    def __lt__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return intrinsic("cmp.__lt__.double4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return intrinsic("cmp.__le__.double4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return intrinsic("cmp.__gt__.double4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return intrinsic("cmp.__ge__.double4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return intrinsic("cmp.__eq__.double4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['double4', f64, float]) -> 'bool4': return intrinsic("cmp.__ne__.double4",  bool4,  _other) # type: ignore[override]
    def __truediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__truediv__.double4",  double4,  _other)
    def __rtruediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__rtruediv__.double4",  double4,  _other)
    def __itruediv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__itruediv__.double4",  double4,  _other)
    def __pow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__pow__.double4",  double4,  _other)
    def __rpow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__rpow__.double4",  double4,  _other)
    def __ipow__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__ipow__.double4",  double4,  _other)
    def __floordiv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__floordiv__.double4",  double4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['double4', f64, float]) -> 'double4': return intrinsic("binop.__rfloordiv__.double4",  double4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8]), 4))
class byte4:
    x: i8
    y: i8
    z: i8
    w: i8
    def __init__(self, x: tp.Union['i8', int] = 0, y: tp.Union['i8', int] = 0, z: tp.Union['i8', int] = 0, w: tp.Union['i8', int] = 0) -> None: self = intrinsic("init.byte4", byte4, x, y, z, w)
    def __add__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__add__.byte4",  byte4,  _other)
    def __radd__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__radd__.byte4",  byte4,  _other)
    def __iadd__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__iadd__.byte4",  byte4,  _other)
    def __sub__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__sub__.byte4",  byte4,  _other)
    def __rsub__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rsub__.byte4",  byte4,  _other)
    def __isub__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__isub__.byte4",  byte4,  _other)
    def __mul__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__mul__.byte4",  byte4,  _other)
    def __rmul__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rmul__.byte4",  byte4,  _other)
    def __imul__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__imul__.byte4",  byte4,  _other)
    def __mod__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__mod__.byte4",  byte4,  _other)
    def __rmod__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rmod__.byte4",  byte4,  _other)
    def __imod__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__imod__.byte4",  byte4,  _other)
    def __lt__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return intrinsic("cmp.__lt__.byte4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return intrinsic("cmp.__le__.byte4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return intrinsic("cmp.__gt__.byte4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return intrinsic("cmp.__ge__.byte4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return intrinsic("cmp.__eq__.byte4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['byte4', i8, int]) -> 'bool4': return intrinsic("cmp.__ne__.byte4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__floordiv__.byte4",  byte4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rfloordiv__.byte4",  byte4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__ifloordiv__.byte4",  byte4,  _other)
    def __lshift__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__lshift__.byte4",  byte4,  _other)
    def __rlshift__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rlshift__.byte4",  byte4,  _other)
    def __ilshift__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__ilshift__.byte4",  byte4,  _other)
    def __rshift__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rshift__.byte4",  byte4,  _other)
    def __rrshift__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rrshift__.byte4",  byte4,  _other)
    def __irshift__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__irshift__.byte4",  byte4,  _other)
    def __and__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__and__.byte4",  byte4,  _other)
    def __rand__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rand__.byte4",  byte4,  _other)
    def __iand__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__iand__.byte4",  byte4,  _other)
    def __or__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__or__.byte4",  byte4,  _other)
    def __ror__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__ror__.byte4",  byte4,  _other)
    def __ior__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__ior__.byte4",  byte4,  _other)
    def __xor__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__xor__.byte4",  byte4,  _other)
    def __rxor__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__rxor__.byte4",  byte4,  _other)
    def __ixor__(self, _other:  tp.Union['byte4', i8, int]) -> 'byte4': return intrinsic("binop.__ixor__.byte4",  byte4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8]), 4))
class ubyte4:
    x: u8
    y: u8
    z: u8
    w: u8
    def __init__(self, x: tp.Union['u8', int] = 0, y: tp.Union['u8', int] = 0, z: tp.Union['u8', int] = 0, w: tp.Union['u8', int] = 0) -> None: self = intrinsic("init.ubyte4", ubyte4, x, y, z, w)
    def __add__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__add__.ubyte4",  ubyte4,  _other)
    def __radd__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__radd__.ubyte4",  ubyte4,  _other)
    def __iadd__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__iadd__.ubyte4",  ubyte4,  _other)
    def __sub__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__sub__.ubyte4",  ubyte4,  _other)
    def __rsub__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rsub__.ubyte4",  ubyte4,  _other)
    def __isub__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__isub__.ubyte4",  ubyte4,  _other)
    def __mul__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__mul__.ubyte4",  ubyte4,  _other)
    def __rmul__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rmul__.ubyte4",  ubyte4,  _other)
    def __imul__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__imul__.ubyte4",  ubyte4,  _other)
    def __mod__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__mod__.ubyte4",  ubyte4,  _other)
    def __rmod__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rmod__.ubyte4",  ubyte4,  _other)
    def __imod__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__imod__.ubyte4",  ubyte4,  _other)
    def __lt__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return intrinsic("cmp.__lt__.ubyte4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return intrinsic("cmp.__le__.ubyte4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return intrinsic("cmp.__gt__.ubyte4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return intrinsic("cmp.__ge__.ubyte4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return intrinsic("cmp.__eq__.ubyte4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'bool4': return intrinsic("cmp.__ne__.ubyte4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__floordiv__.ubyte4",  ubyte4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rfloordiv__.ubyte4",  ubyte4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__ifloordiv__.ubyte4",  ubyte4,  _other)
    def __lshift__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__lshift__.ubyte4",  ubyte4,  _other)
    def __rlshift__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rlshift__.ubyte4",  ubyte4,  _other)
    def __ilshift__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__ilshift__.ubyte4",  ubyte4,  _other)
    def __rshift__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rshift__.ubyte4",  ubyte4,  _other)
    def __rrshift__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rrshift__.ubyte4",  ubyte4,  _other)
    def __irshift__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__irshift__.ubyte4",  ubyte4,  _other)
    def __and__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__and__.ubyte4",  ubyte4,  _other)
    def __rand__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rand__.ubyte4",  ubyte4,  _other)
    def __iand__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__iand__.ubyte4",  ubyte4,  _other)
    def __or__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__or__.ubyte4",  ubyte4,  _other)
    def __ror__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__ror__.ubyte4",  ubyte4,  _other)
    def __ior__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__ior__.ubyte4",  ubyte4,  _other)
    def __xor__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__xor__.ubyte4",  ubyte4,  _other)
    def __rxor__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__rxor__.ubyte4",  ubyte4,  _other)
    def __ixor__(self, _other:  tp.Union['ubyte4', u8, int]) -> 'ubyte4': return intrinsic("binop.__ixor__.ubyte4",  ubyte4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16]), 4))
class short4:
    x: i16
    y: i16
    z: i16
    w: i16
    def __init__(self, x: tp.Union['i16', int] = 0, y: tp.Union['i16', int] = 0, z: tp.Union['i16', int] = 0, w: tp.Union['i16', int] = 0) -> None: self = intrinsic("init.short4", short4, x, y, z, w)
    def __add__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__add__.short4",  short4,  _other)
    def __radd__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__radd__.short4",  short4,  _other)
    def __iadd__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__iadd__.short4",  short4,  _other)
    def __sub__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__sub__.short4",  short4,  _other)
    def __rsub__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rsub__.short4",  short4,  _other)
    def __isub__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__isub__.short4",  short4,  _other)
    def __mul__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__mul__.short4",  short4,  _other)
    def __rmul__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rmul__.short4",  short4,  _other)
    def __imul__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__imul__.short4",  short4,  _other)
    def __mod__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__mod__.short4",  short4,  _other)
    def __rmod__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rmod__.short4",  short4,  _other)
    def __imod__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__imod__.short4",  short4,  _other)
    def __lt__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return intrinsic("cmp.__lt__.short4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return intrinsic("cmp.__le__.short4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return intrinsic("cmp.__gt__.short4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return intrinsic("cmp.__ge__.short4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return intrinsic("cmp.__eq__.short4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['short4', i16, int]) -> 'bool4': return intrinsic("cmp.__ne__.short4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__floordiv__.short4",  short4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rfloordiv__.short4",  short4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__ifloordiv__.short4",  short4,  _other)
    def __lshift__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__lshift__.short4",  short4,  _other)
    def __rlshift__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rlshift__.short4",  short4,  _other)
    def __ilshift__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__ilshift__.short4",  short4,  _other)
    def __rshift__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rshift__.short4",  short4,  _other)
    def __rrshift__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rrshift__.short4",  short4,  _other)
    def __irshift__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__irshift__.short4",  short4,  _other)
    def __and__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__and__.short4",  short4,  _other)
    def __rand__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rand__.short4",  short4,  _other)
    def __iand__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__iand__.short4",  short4,  _other)
    def __or__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__or__.short4",  short4,  _other)
    def __ror__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__ror__.short4",  short4,  _other)
    def __ior__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__ior__.short4",  short4,  _other)
    def __xor__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__xor__.short4",  short4,  _other)
    def __rxor__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__rxor__.short4",  short4,  _other)
    def __ixor__(self, _other:  tp.Union['short4', i16, int]) -> 'short4': return intrinsic("binop.__ixor__.short4",  short4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16]), 4))
class ushort4:
    x: u16
    y: u16
    z: u16
    w: u16
    def __init__(self, x: tp.Union['u16', int] = 0, y: tp.Union['u16', int] = 0, z: tp.Union['u16', int] = 0, w: tp.Union['u16', int] = 0) -> None: self = intrinsic("init.ushort4", ushort4, x, y, z, w)
    def __add__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__add__.ushort4",  ushort4,  _other)
    def __radd__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__radd__.ushort4",  ushort4,  _other)
    def __iadd__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__iadd__.ushort4",  ushort4,  _other)
    def __sub__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__sub__.ushort4",  ushort4,  _other)
    def __rsub__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rsub__.ushort4",  ushort4,  _other)
    def __isub__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__isub__.ushort4",  ushort4,  _other)
    def __mul__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__mul__.ushort4",  ushort4,  _other)
    def __rmul__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rmul__.ushort4",  ushort4,  _other)
    def __imul__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__imul__.ushort4",  ushort4,  _other)
    def __mod__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__mod__.ushort4",  ushort4,  _other)
    def __rmod__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rmod__.ushort4",  ushort4,  _other)
    def __imod__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__imod__.ushort4",  ushort4,  _other)
    def __lt__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return intrinsic("cmp.__lt__.ushort4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return intrinsic("cmp.__le__.ushort4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return intrinsic("cmp.__gt__.ushort4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return intrinsic("cmp.__ge__.ushort4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return intrinsic("cmp.__eq__.ushort4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ushort4', u16, int]) -> 'bool4': return intrinsic("cmp.__ne__.ushort4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__floordiv__.ushort4",  ushort4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rfloordiv__.ushort4",  ushort4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__ifloordiv__.ushort4",  ushort4,  _other)
    def __lshift__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__lshift__.ushort4",  ushort4,  _other)
    def __rlshift__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rlshift__.ushort4",  ushort4,  _other)
    def __ilshift__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__ilshift__.ushort4",  ushort4,  _other)
    def __rshift__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rshift__.ushort4",  ushort4,  _other)
    def __rrshift__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rrshift__.ushort4",  ushort4,  _other)
    def __irshift__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__irshift__.ushort4",  ushort4,  _other)
    def __and__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__and__.ushort4",  ushort4,  _other)
    def __rand__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rand__.ushort4",  ushort4,  _other)
    def __iand__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__iand__.ushort4",  ushort4,  _other)
    def __or__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__or__.ushort4",  ushort4,  _other)
    def __ror__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__ror__.ushort4",  ushort4,  _other)
    def __ior__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__ior__.ushort4",  ushort4,  _other)
    def __xor__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__xor__.ushort4",  ushort4,  _other)
    def __rxor__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__rxor__.ushort4",  ushort4,  _other)
    def __ixor__(self, _other:  tp.Union['ushort4', u16, int]) -> 'ushort4': return intrinsic("binop.__ixor__.ushort4",  ushort4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32]), 4))
class int4:
    x: i32
    y: i32
    z: i32
    w: i32
    def __init__(self, x: tp.Union['i32', int] = 0, y: tp.Union['i32', int] = 0, z: tp.Union['i32', int] = 0, w: tp.Union['i32', int] = 0) -> None: self = intrinsic("init.int4", int4, x, y, z, w)
    def __add__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__add__.int4",  int4,  _other)
    def __radd__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__radd__.int4",  int4,  _other)
    def __iadd__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__iadd__.int4",  int4,  _other)
    def __sub__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__sub__.int4",  int4,  _other)
    def __rsub__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rsub__.int4",  int4,  _other)
    def __isub__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__isub__.int4",  int4,  _other)
    def __mul__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__mul__.int4",  int4,  _other)
    def __rmul__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rmul__.int4",  int4,  _other)
    def __imul__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__imul__.int4",  int4,  _other)
    def __mod__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__mod__.int4",  int4,  _other)
    def __rmod__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rmod__.int4",  int4,  _other)
    def __imod__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__imod__.int4",  int4,  _other)
    def __lt__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return intrinsic("cmp.__lt__.int4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return intrinsic("cmp.__le__.int4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return intrinsic("cmp.__gt__.int4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return intrinsic("cmp.__ge__.int4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return intrinsic("cmp.__eq__.int4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['int4', i32, int]) -> 'bool4': return intrinsic("cmp.__ne__.int4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__floordiv__.int4",  int4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rfloordiv__.int4",  int4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__ifloordiv__.int4",  int4,  _other)
    def __lshift__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__lshift__.int4",  int4,  _other)
    def __rlshift__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rlshift__.int4",  int4,  _other)
    def __ilshift__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__ilshift__.int4",  int4,  _other)
    def __rshift__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rshift__.int4",  int4,  _other)
    def __rrshift__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rrshift__.int4",  int4,  _other)
    def __irshift__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__irshift__.int4",  int4,  _other)
    def __and__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__and__.int4",  int4,  _other)
    def __rand__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rand__.int4",  int4,  _other)
    def __iand__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__iand__.int4",  int4,  _other)
    def __or__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__or__.int4",  int4,  _other)
    def __ror__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__ror__.int4",  int4,  _other)
    def __ior__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__ior__.int4",  int4,  _other)
    def __xor__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__xor__.int4",  int4,  _other)
    def __rxor__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__rxor__.int4",  int4,  _other)
    def __ixor__(self, _other:  tp.Union['int4', i32, int]) -> 'int4': return intrinsic("binop.__ixor__.int4",  int4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32]), 4))
class uint4:
    x: u32
    y: u32
    z: u32
    w: u32
    def __init__(self, x: tp.Union['u32', int] = 0, y: tp.Union['u32', int] = 0, z: tp.Union['u32', int] = 0, w: tp.Union['u32', int] = 0) -> None: self = intrinsic("init.uint4", uint4, x, y, z, w)
    def __add__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__add__.uint4",  uint4,  _other)
    def __radd__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__radd__.uint4",  uint4,  _other)
    def __iadd__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__iadd__.uint4",  uint4,  _other)
    def __sub__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__sub__.uint4",  uint4,  _other)
    def __rsub__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rsub__.uint4",  uint4,  _other)
    def __isub__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__isub__.uint4",  uint4,  _other)
    def __mul__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__mul__.uint4",  uint4,  _other)
    def __rmul__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rmul__.uint4",  uint4,  _other)
    def __imul__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__imul__.uint4",  uint4,  _other)
    def __mod__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__mod__.uint4",  uint4,  _other)
    def __rmod__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rmod__.uint4",  uint4,  _other)
    def __imod__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__imod__.uint4",  uint4,  _other)
    def __lt__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return intrinsic("cmp.__lt__.uint4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return intrinsic("cmp.__le__.uint4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return intrinsic("cmp.__gt__.uint4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return intrinsic("cmp.__ge__.uint4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return intrinsic("cmp.__eq__.uint4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['uint4', u32, int]) -> 'bool4': return intrinsic("cmp.__ne__.uint4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__floordiv__.uint4",  uint4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rfloordiv__.uint4",  uint4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__ifloordiv__.uint4",  uint4,  _other)
    def __lshift__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__lshift__.uint4",  uint4,  _other)
    def __rlshift__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rlshift__.uint4",  uint4,  _other)
    def __ilshift__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__ilshift__.uint4",  uint4,  _other)
    def __rshift__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rshift__.uint4",  uint4,  _other)
    def __rrshift__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rrshift__.uint4",  uint4,  _other)
    def __irshift__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__irshift__.uint4",  uint4,  _other)
    def __and__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__and__.uint4",  uint4,  _other)
    def __rand__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rand__.uint4",  uint4,  _other)
    def __iand__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__iand__.uint4",  uint4,  _other)
    def __or__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__or__.uint4",  uint4,  _other)
    def __ror__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__ror__.uint4",  uint4,  _other)
    def __ior__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__ior__.uint4",  uint4,  _other)
    def __xor__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__xor__.uint4",  uint4,  _other)
    def __rxor__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__rxor__.uint4",  uint4,  _other)
    def __ixor__(self, _other:  tp.Union['uint4', u32, int]) -> 'uint4': return intrinsic("binop.__ixor__.uint4",  uint4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64]), 4))
class long4:
    x: i64
    y: i64
    z: i64
    w: i64
    def __init__(self, x: tp.Union['i64', int] = 0, y: tp.Union['i64', int] = 0, z: tp.Union['i64', int] = 0, w: tp.Union['i64', int] = 0) -> None: self = intrinsic("init.long4", long4, x, y, z, w)
    def __add__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__add__.long4",  long4,  _other)
    def __radd__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__radd__.long4",  long4,  _other)
    def __iadd__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__iadd__.long4",  long4,  _other)
    def __sub__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__sub__.long4",  long4,  _other)
    def __rsub__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rsub__.long4",  long4,  _other)
    def __isub__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__isub__.long4",  long4,  _other)
    def __mul__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__mul__.long4",  long4,  _other)
    def __rmul__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rmul__.long4",  long4,  _other)
    def __imul__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__imul__.long4",  long4,  _other)
    def __mod__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__mod__.long4",  long4,  _other)
    def __rmod__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rmod__.long4",  long4,  _other)
    def __imod__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__imod__.long4",  long4,  _other)
    def __lt__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return intrinsic("cmp.__lt__.long4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return intrinsic("cmp.__le__.long4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return intrinsic("cmp.__gt__.long4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return intrinsic("cmp.__ge__.long4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return intrinsic("cmp.__eq__.long4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['long4', i64, int]) -> 'bool4': return intrinsic("cmp.__ne__.long4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__floordiv__.long4",  long4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rfloordiv__.long4",  long4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__ifloordiv__.long4",  long4,  _other)
    def __lshift__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__lshift__.long4",  long4,  _other)
    def __rlshift__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rlshift__.long4",  long4,  _other)
    def __ilshift__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__ilshift__.long4",  long4,  _other)
    def __rshift__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rshift__.long4",  long4,  _other)
    def __rrshift__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rrshift__.long4",  long4,  _other)
    def __irshift__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__irshift__.long4",  long4,  _other)
    def __and__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__and__.long4",  long4,  _other)
    def __rand__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rand__.long4",  long4,  _other)
    def __iand__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__iand__.long4",  long4,  _other)
    def __or__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__or__.long4",  long4,  _other)
    def __ror__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__ror__.long4",  long4,  _other)
    def __ior__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__ior__.long4",  long4,  _other)
    def __xor__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__xor__.long4",  long4,  _other)
    def __rxor__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__rxor__.long4",  long4,  _other)
    def __ixor__(self, _other:  tp.Union['long4', i64, int]) -> 'long4': return intrinsic("binop.__ixor__.long4",  long4,  _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64]), 4))
class ulong4:
    x: u64
    y: u64
    z: u64
    w: u64
    def __init__(self, x: tp.Union['u64', int] = 0, y: tp.Union['u64', int] = 0, z: tp.Union['u64', int] = 0, w: tp.Union['u64', int] = 0) -> None: self = intrinsic("init.ulong4", ulong4, x, y, z, w)
    def __add__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__add__.ulong4",  ulong4,  _other)
    def __radd__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__radd__.ulong4",  ulong4,  _other)
    def __iadd__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__iadd__.ulong4",  ulong4,  _other)
    def __sub__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__sub__.ulong4",  ulong4,  _other)
    def __rsub__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rsub__.ulong4",  ulong4,  _other)
    def __isub__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__isub__.ulong4",  ulong4,  _other)
    def __mul__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__mul__.ulong4",  ulong4,  _other)
    def __rmul__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rmul__.ulong4",  ulong4,  _other)
    def __imul__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__imul__.ulong4",  ulong4,  _other)
    def __mod__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__mod__.ulong4",  ulong4,  _other)
    def __rmod__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rmod__.ulong4",  ulong4,  _other)
    def __imod__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__imod__.ulong4",  ulong4,  _other)
    def __lt__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return intrinsic("cmp.__lt__.ulong4",  bool4,  _other) # type: ignore[override]
    def __le__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return intrinsic("cmp.__le__.ulong4",  bool4,  _other) # type: ignore[override]
    def __gt__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return intrinsic("cmp.__gt__.ulong4",  bool4,  _other) # type: ignore[override]
    def __ge__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return intrinsic("cmp.__ge__.ulong4",  bool4,  _other) # type: ignore[override]
    def __eq__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return intrinsic("cmp.__eq__.ulong4",  bool4,  _other) # type: ignore[override]
    def __ne__(self, _other:  tp.Union['ulong4', u64, int]) -> 'bool4': return intrinsic("cmp.__ne__.ulong4",  bool4,  _other) # type: ignore[override]
    def __floordiv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__floordiv__.ulong4",  ulong4,  _other)
    def __rfloordiv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rfloordiv__.ulong4",  ulong4,  _other)
    def __ifloordiv__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__ifloordiv__.ulong4",  ulong4,  _other)
    def __lshift__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__lshift__.ulong4",  ulong4,  _other)
    def __rlshift__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rlshift__.ulong4",  ulong4,  _other)
    def __ilshift__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__ilshift__.ulong4",  ulong4,  _other)
    def __rshift__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rshift__.ulong4",  ulong4,  _other)
    def __rrshift__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rrshift__.ulong4",  ulong4,  _other)
    def __irshift__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__irshift__.ulong4",  ulong4,  _other)
    def __and__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__and__.ulong4",  ulong4,  _other)
    def __rand__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rand__.ulong4",  ulong4,  _other)
    def __iand__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__iand__.ulong4",  ulong4,  _other)
    def __or__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__or__.ulong4",  ulong4,  _other)
    def __ror__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__ror__.ulong4",  ulong4,  _other)
    def __ior__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__ior__.ulong4",  ulong4,  _other)
    def __xor__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__xor__.ulong4",  ulong4,  _other)
    def __rxor__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__rxor__.ulong4",  ulong4,  _other)
    def __ixor__(self, _other:  tp.Union['ulong4', u64, int]) -> 'ulong4': return intrinsic("binop.__ixor__.ulong4",  ulong4,  _other)

__all__ = ['FLOAT_TYPES', 'FloatType', 'FloatBuiltin', 'abs', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh', 'ceil', 'cos', 'cosh', 'exp', 'floor', 'log', 'log10', 'log2', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc', 'atan2', 'copysign', 'f32', 'f64', 'i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'bool2', 'float2', 'double2', 'byte2', 'ubyte2', 'short2', 'ushort2', 'int2', 'uint2', 'long2', 'ulong2', 'bool3', 'float3', 'double3', 'byte3', 'ubyte3', 'short3', 'ushort3', 'int3', 'uint3', 'long3', 'ulong3', 'bool4', 'float4', 'double4', 'byte4', 'ubyte4', 'short4', 'ushort4', 'int4', 'uint4', 'long4', 'ulong4']
