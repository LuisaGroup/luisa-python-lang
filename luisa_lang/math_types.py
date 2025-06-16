# fmt: off
import typing as tp
from luisa_lang._builtin_decor import func, builtin_type, trace
from luisa_lang.lang_runtime import __intrinsic__, __intrinsic_checked__, __escape__, assign, type_of, is_jit, JitVar
from luisa_lang.core_types import Ref
from luisa_lang.classinfo import register_class
import luisa_lang.hir as _hir
IntLiteral = int
FloatLiteral = float
_ctx = _hir.GlobalContext.get()
def _literal_to_value(literal, dtype):
    if isinstance(literal, JitVar):
        return literal
    return _hir.Constant(literal, dtype)
FLOAT_TYPES: tp.Final[tp.List[str]] = ["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
FloatType = tp.Union["f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4"]
_F = tp.TypeVar("_F")
_F1 = tp.TypeVar("_F1", "f32", "f64", "float2", "double2", "float3", "double3", "float4", "double4")

@func
def abs(x: _F1) -> _F1: return __intrinsic__('math.abs', _F1, x) # type: ignore
@func
def acos(x: _F1) -> _F1: return __intrinsic__('math.acos', _F1, x) # type: ignore
@func
def acosh(x: _F1) -> _F1: return __intrinsic__('math.acosh', _F1, x) # type: ignore
@func
def asin(x: _F1) -> _F1: return __intrinsic__('math.asin', _F1, x) # type: ignore
@func
def asinh(x: _F1) -> _F1: return __intrinsic__('math.asinh', _F1, x) # type: ignore
@func
def atan(x: _F1) -> _F1: return __intrinsic__('math.atan', _F1, x) # type: ignore
@func
def atanh(x: _F1) -> _F1: return __intrinsic__('math.atanh', _F1, x) # type: ignore
@func
def ceil(x: _F1) -> _F1: return __intrinsic__('math.ceil', _F1, x) # type: ignore
@func
def cos(x: _F1) -> _F1: return __intrinsic__('math.cos', _F1, x) # type: ignore
@func
def cosh(x: _F1) -> _F1: return __intrinsic__('math.cosh', _F1, x) # type: ignore
@func
def exp(x: _F1) -> _F1: return __intrinsic__('math.exp', _F1, x) # type: ignore
@func
def floor(x: _F1) -> _F1: return __intrinsic__('math.floor', _F1, x) # type: ignore
@func
def log(x: _F1) -> _F1: return __intrinsic__('math.log', _F1, x) # type: ignore
@func
def log10(x: _F1) -> _F1: return __intrinsic__('math.log10', _F1, x) # type: ignore
@func
def log2(x: _F1) -> _F1: return __intrinsic__('math.log2', _F1, x) # type: ignore
@func
def sin(x: _F1) -> _F1: return __intrinsic__('math.sin', _F1, x) # type: ignore
@func
def sinh(x: _F1) -> _F1: return __intrinsic__('math.sinh', _F1, x) # type: ignore
@func
def sqrt(x: _F1) -> _F1: return __intrinsic__('math.sqrt', _F1, x) # type: ignore
@func
def tan(x: _F1) -> _F1: return __intrinsic__('math.tan', _F1, x) # type: ignore
@func
def tanh(x: _F1) -> _F1: return __intrinsic__('math.tanh', _F1, x) # type: ignore
@func
def trunc(x: _F1) -> _F1: return __intrinsic__('math.trunc', _F1, x) # type: ignore
@func
def atan2(x: _F1, y: _F1) -> _F1: return __intrinsic__('math.atan2', _F1, x, y) # type: ignore
@func
def copysign(x: _F1, y: _F1) -> _F1: return __intrinsic__('math.copysign', _F1, x, y) # type: ignore
@builtin_type(_hir.BoolType())
class boolean:
    @trace
    def __init__(self, _value: tp.Union['boolean', bool]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.boolean",  boolean,  _literal_to_value(_value, type_of(boolean))))
        else:
            pass # TODO
    @trace
    def __eq__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other) # type: ignore
    @trace
    def __and__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__and__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__rand__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__iand__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__or__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__ror__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__ior__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__xor__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['boolean', bool]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.boolean", [boolean, __escape__( tp.Union[boolean, bool])], boolean,  Ref(self), _other)
    @trace
    def __invert__(self) -> 'boolean': return __intrinsic__("unary.__invert__.boolean",  boolean, self)

@builtin_type(_hir.FloatType(32))
class f32:
    @trace
    def __init__(self, _value: tp.Union['f32', float]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.f32",  f32,  _literal_to_value(_value, type_of(f32))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__add__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__radd__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__sub__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__isub__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__mul__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__imul__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__mod__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__imod__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['f32', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.f32", [f32, __escape__( tp.Union[f32, float])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['f32', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.f32", [f32, __escape__( tp.Union[f32, float])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['f32', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.f32", [f32, __escape__( tp.Union[f32, float])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['f32', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.f32", [f32, __escape__( tp.Union[f32, float])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['f32', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.f32", [f32, __escape__( tp.Union[f32, float])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['f32', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.f32", [f32, __escape__( tp.Union[f32, float])], boolean,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__pow__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['f32', float]) -> 'f32': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.f32", [f32, __escape__( tp.Union[f32, float])], f32,  self, _other)
    @trace
    def __neg__(self) -> 'f32': return __intrinsic__("unary.__neg__.f32",  f32, self)
    @trace
    def __pos__(self) -> 'f32': return __intrinsic__("unary.__pos__.f32",  f32, self)

@builtin_type(_hir.FloatType(64))
class f64:
    @trace
    def __init__(self, _value: tp.Union['f64', float]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.f64",  f64,  _literal_to_value(_value, type_of(f64))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__add__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__radd__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__sub__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__isub__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__mul__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__imul__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__mod__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__imod__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['f64', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.f64", [f64, __escape__( tp.Union[f64, float])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['f64', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.f64", [f64, __escape__( tp.Union[f64, float])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['f64', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.f64", [f64, __escape__( tp.Union[f64, float])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['f64', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.f64", [f64, __escape__( tp.Union[f64, float])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['f64', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.f64", [f64, __escape__( tp.Union[f64, float])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['f64', float]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.f64", [f64, __escape__( tp.Union[f64, float])], boolean,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__pow__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['f64', float]) -> 'f64': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.f64", [f64, __escape__( tp.Union[f64, float])], f64,  self, _other)
    @trace
    def __neg__(self) -> 'f64': return __intrinsic__("unary.__neg__.f64",  f64, self)
    @trace
    def __pos__(self) -> 'f64': return __intrinsic__("unary.__pos__.f64",  f64, self)

@builtin_type(_hir.IntType(8, True))
class i8:
    @trace
    def __init__(self, _value: tp.Union['i8', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.i8",  i8,  _literal_to_value(_value, type_of(i8))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__add__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__radd__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__sub__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__isub__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__mul__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__imul__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__mod__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__imod__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['i8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['i8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['i8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['i8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['i8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['i8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__and__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rand__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__iand__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__or__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__ror__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__ior__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__xor__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['i8', IntLiteral]) -> 'i8': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.i8", [i8, __escape__( tp.Union[i8, IntLiteral])], i8,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'i8': return __intrinsic__("unary.__neg__.i8",  i8, self)
    @trace
    def __pos__(self) -> 'i8': return __intrinsic__("unary.__pos__.i8",  i8, self)
    @trace
    def __invert__(self) -> 'i8': return __intrinsic__("unary.__invert__.i8",  i8, self)

@builtin_type(_hir.IntType(8, False))
class u8:
    @trace
    def __init__(self, _value: tp.Union['u8', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.u8",  u8,  _literal_to_value(_value, type_of(u8))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__add__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__radd__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__sub__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__isub__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__mul__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__imul__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__mod__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__imod__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['u8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['u8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['u8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['u8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['u8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['u8', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__and__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rand__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__iand__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__or__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__ror__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__ior__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__xor__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['u8', IntLiteral]) -> 'u8': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.u8", [u8, __escape__( tp.Union[u8, IntLiteral])], u8,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'u8': return __intrinsic__("unary.__neg__.u8",  u8, self)
    @trace
    def __pos__(self) -> 'u8': return __intrinsic__("unary.__pos__.u8",  u8, self)
    @trace
    def __invert__(self) -> 'u8': return __intrinsic__("unary.__invert__.u8",  u8, self)

@builtin_type(_hir.IntType(16, True))
class i16:
    @trace
    def __init__(self, _value: tp.Union['i16', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.i16",  i16,  _literal_to_value(_value, type_of(i16))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__add__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__radd__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__sub__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__isub__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__mul__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__imul__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__mod__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__imod__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['i16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['i16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['i16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['i16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['i16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['i16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__and__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rand__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__iand__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__or__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__ror__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__ior__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__xor__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['i16', IntLiteral]) -> 'i16': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.i16", [i16, __escape__( tp.Union[i16, IntLiteral])], i16,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'i16': return __intrinsic__("unary.__neg__.i16",  i16, self)
    @trace
    def __pos__(self) -> 'i16': return __intrinsic__("unary.__pos__.i16",  i16, self)
    @trace
    def __invert__(self) -> 'i16': return __intrinsic__("unary.__invert__.i16",  i16, self)

@builtin_type(_hir.IntType(16, False))
class u16:
    @trace
    def __init__(self, _value: tp.Union['u16', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.u16",  u16,  _literal_to_value(_value, type_of(u16))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__add__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__radd__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__sub__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__isub__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__mul__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__imul__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__mod__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__imod__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['u16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['u16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['u16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['u16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['u16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['u16', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__and__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rand__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__iand__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__or__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__ror__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__ior__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__xor__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['u16', IntLiteral]) -> 'u16': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.u16", [u16, __escape__( tp.Union[u16, IntLiteral])], u16,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'u16': return __intrinsic__("unary.__neg__.u16",  u16, self)
    @trace
    def __pos__(self) -> 'u16': return __intrinsic__("unary.__pos__.u16",  u16, self)
    @trace
    def __invert__(self) -> 'u16': return __intrinsic__("unary.__invert__.u16",  u16, self)

@builtin_type(_hir.IntType(64, True))
class i64:
    @trace
    def __init__(self, _value: tp.Union['i64', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.i64",  i64,  _literal_to_value(_value, type_of(i64))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__add__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__radd__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__sub__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__isub__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__mul__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__imul__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__mod__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__imod__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['i64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['i64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['i64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['i64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['i64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['i64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__and__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rand__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__iand__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__or__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__ror__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__ior__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__xor__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['i64', IntLiteral]) -> 'i64': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.i64", [i64, __escape__( tp.Union[i64, IntLiteral])], i64,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'i64': return __intrinsic__("unary.__neg__.i64",  i64, self)
    @trace
    def __pos__(self) -> 'i64': return __intrinsic__("unary.__pos__.i64",  i64, self)
    @trace
    def __invert__(self) -> 'i64': return __intrinsic__("unary.__invert__.i64",  i64, self)

@builtin_type(_hir.IntType(64, False))
class u64:
    @trace
    def __init__(self, _value: tp.Union['u64', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.u64",  u64,  _literal_to_value(_value, type_of(u64))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__add__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__radd__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__sub__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__isub__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__mul__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__imul__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__mod__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__imod__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['u64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['u64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['u64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['u64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['u64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['u64', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__and__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rand__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__iand__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__or__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__ror__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__ior__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__xor__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['u64', IntLiteral]) -> 'u64': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.u64", [u64, __escape__( tp.Union[u64, IntLiteral])], u64,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'u64': return __intrinsic__("unary.__neg__.u64",  u64, self)
    @trace
    def __pos__(self) -> 'u64': return __intrinsic__("unary.__pos__.u64",  u64, self)
    @trace
    def __invert__(self) -> 'u64': return __intrinsic__("unary.__invert__.u64",  u64, self)

@builtin_type(_hir.IntType(32, True))
class i32:
    @trace
    def __init__(self, _value: tp.Union['i32', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.i32",  i32,  _literal_to_value(_value, type_of(i32))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__add__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__radd__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__sub__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__isub__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__mul__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__imul__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__mod__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__imod__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['i32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['i32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['i32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['i32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['i32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['i32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__and__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rand__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__iand__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__or__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__ror__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__ior__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__xor__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['i32', IntLiteral]) -> 'i32': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.i32", [i32, __escape__( tp.Union[i32, IntLiteral])], i32,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'i32': return __intrinsic__("unary.__neg__.i32",  i32, self)
    @trace
    def __pos__(self) -> 'i32': return __intrinsic__("unary.__pos__.i32",  i32, self)
    @trace
    def __invert__(self) -> 'i32': return __intrinsic__("unary.__invert__.i32",  i32, self)

@builtin_type(_hir.IntType(32, False))
class u32:
    @trace
    def __init__(self, _value: tp.Union['u32', IntLiteral]) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.u32",  u32,  _literal_to_value(_value, type_of(u32))))
        else:
            pass # TODO
    @trace
    def __add__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__add__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__radd__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__sub__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__isub__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__mul__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__imul__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__mod__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__imod__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['u32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['u32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__le__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['u32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['u32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['u32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['u32', IntLiteral]) -> 'boolean': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], boolean,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__and__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rand__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__iand__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__or__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__ror__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__ior__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__xor__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['u32', IntLiteral]) -> 'u32': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.u32", [u32, __escape__( tp.Union[u32, IntLiteral])], u32,  Ref(self), _other)
    @trace
    def __neg__(self) -> 'u32': return __intrinsic__("unary.__neg__.u32",  u32, self)
    @trace
    def __pos__(self) -> 'u32': return __intrinsic__("unary.__pos__.u32",  u32, self)
    @trace
    def __invert__(self) -> 'u32': return __intrinsic__("unary.__invert__.u32",  u32, self)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[boolean].default()), 2))
class bool2:
    x: boolean
    y: boolean
    @trace
    def __init__(self, x: tp.Union['boolean', bool] = False, y: tp.Union['boolean', bool] = False) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.bool2", bool2, _literal_to_value(x, type_of(bool2)), _literal_to_value(y, type_of(bool2))))
        else:
            pass # TODO

    @trace
    def __eq__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other) # type: ignore
    @trace
    def __and__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__and__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__or__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['bool2', boolean, bool]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.bool2", [bool2, __escape__( tp.Union[bool2, boolean, bool])], bool2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32].default()), 2))
class float2:
    x: f32
    y: f32
    @trace
    def __init__(self, x: tp.Union['f32', FloatLiteral] = FloatLiteral(), y: tp.Union['f32', FloatLiteral] = FloatLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.float2", float2, _literal_to_value(x, type_of(float2)), _literal_to_value(y, type_of(float2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__add__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__pow__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['float2', f32, FloatLiteral]) -> 'float2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.float2", [float2, __escape__( tp.Union[float2, f32, FloatLiteral])], float2,  self, _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64].default()), 2))
class double2:
    x: f64
    y: f64
    @trace
    def __init__(self, x: tp.Union['f64', FloatLiteral] = FloatLiteral(), y: tp.Union['f64', FloatLiteral] = FloatLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.double2", double2, _literal_to_value(x, type_of(double2)), _literal_to_value(y, type_of(double2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__add__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__pow__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['double2', f64, FloatLiteral]) -> 'double2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.double2", [double2, __escape__( tp.Union[double2, f64, FloatLiteral])], double2,  self, _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8].default()), 2))
class byte2:
    x: i8
    y: i8
    @trace
    def __init__(self, x: tp.Union['i8', IntLiteral] = IntLiteral(), y: tp.Union['i8', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.byte2", byte2, _literal_to_value(x, type_of(byte2)), _literal_to_value(y, type_of(byte2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__add__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__and__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__or__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['byte2', i8, IntLiteral]) -> 'byte2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.byte2", [byte2, __escape__( tp.Union[byte2, i8, IntLiteral])], byte2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8].default()), 2))
class ubyte2:
    x: u8
    y: u8
    @trace
    def __init__(self, x: tp.Union['u8', IntLiteral] = IntLiteral(), y: tp.Union['u8', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ubyte2", ubyte2, _literal_to_value(x, type_of(ubyte2)), _literal_to_value(y, type_of(ubyte2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__add__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__and__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__or__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ubyte2', u8, IntLiteral]) -> 'ubyte2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ubyte2", [ubyte2, __escape__( tp.Union[ubyte2, u8, IntLiteral])], ubyte2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16].default()), 2))
class short2:
    x: i16
    y: i16
    @trace
    def __init__(self, x: tp.Union['i16', IntLiteral] = IntLiteral(), y: tp.Union['i16', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.short2", short2, _literal_to_value(x, type_of(short2)), _literal_to_value(y, type_of(short2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__add__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__and__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__or__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['short2', i16, IntLiteral]) -> 'short2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.short2", [short2, __escape__( tp.Union[short2, i16, IntLiteral])], short2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16].default()), 2))
class ushort2:
    x: u16
    y: u16
    @trace
    def __init__(self, x: tp.Union['u16', IntLiteral] = IntLiteral(), y: tp.Union['u16', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ushort2", ushort2, _literal_to_value(x, type_of(ushort2)), _literal_to_value(y, type_of(ushort2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__add__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__and__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__or__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ushort2', u16, IntLiteral]) -> 'ushort2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ushort2", [ushort2, __escape__( tp.Union[ushort2, u16, IntLiteral])], ushort2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32].default()), 2))
class int2:
    x: i32
    y: i32
    @trace
    def __init__(self, x: tp.Union['i32', IntLiteral] = IntLiteral(), y: tp.Union['i32', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.int2", int2, _literal_to_value(x, type_of(int2)), _literal_to_value(y, type_of(int2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__add__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__and__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__or__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['int2', i32, IntLiteral]) -> 'int2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.int2", [int2, __escape__( tp.Union[int2, i32, IntLiteral])], int2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32].default()), 2))
class uint2:
    x: u32
    y: u32
    @trace
    def __init__(self, x: tp.Union['u32', IntLiteral] = IntLiteral(), y: tp.Union['u32', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.uint2", uint2, _literal_to_value(x, type_of(uint2)), _literal_to_value(y, type_of(uint2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__add__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__and__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__or__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['uint2', u32, IntLiteral]) -> 'uint2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.uint2", [uint2, __escape__( tp.Union[uint2, u32, IntLiteral])], uint2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64].default()), 2))
class long2:
    x: i64
    y: i64
    @trace
    def __init__(self, x: tp.Union['i64', IntLiteral] = IntLiteral(), y: tp.Union['i64', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.long2", long2, _literal_to_value(x, type_of(long2)), _literal_to_value(y, type_of(long2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__add__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__and__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__or__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['long2', i64, IntLiteral]) -> 'long2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.long2", [long2, __escape__( tp.Union[long2, i64, IntLiteral])], long2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64].default()), 2))
class ulong2:
    x: u64
    y: u64
    @trace
    def __init__(self, x: tp.Union['u64', IntLiteral] = IntLiteral(), y: tp.Union['u64', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ulong2", ulong2, _literal_to_value(x, type_of(ulong2)), _literal_to_value(y, type_of(ulong2))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__add__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'bool2': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], bool2,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__and__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__or__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ulong2', u64, IntLiteral]) -> 'ulong2': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ulong2", [ulong2, __escape__( tp.Union[ulong2, u64, IntLiteral])], ulong2,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[boolean].default()), 3))
class bool3:
    x: boolean
    y: boolean
    z: boolean
    @trace
    def __init__(self, x: tp.Union['boolean', bool] = False, y: tp.Union['boolean', bool] = False, z: tp.Union['boolean', bool] = False) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.bool3", bool3, _literal_to_value(x, type_of(bool3)), _literal_to_value(y, type_of(bool3)), _literal_to_value(z, type_of(bool3))))
        else:
            pass # TODO

    @trace
    def __eq__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other) # type: ignore
    @trace
    def __and__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__and__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__or__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['bool3', boolean, bool]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.bool3", [bool3, __escape__( tp.Union[bool3, boolean, bool])], bool3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32].default()), 3))
class float3:
    x: f32
    y: f32
    z: f32
    @trace
    def __init__(self, x: tp.Union['f32', FloatLiteral] = FloatLiteral(), y: tp.Union['f32', FloatLiteral] = FloatLiteral(), z: tp.Union['f32', FloatLiteral] = FloatLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.float3", float3, _literal_to_value(x, type_of(float3)), _literal_to_value(y, type_of(float3)), _literal_to_value(z, type_of(float3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__add__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__pow__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['float3', f32, FloatLiteral]) -> 'float3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.float3", [float3, __escape__( tp.Union[float3, f32, FloatLiteral])], float3,  self, _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64].default()), 3))
class double3:
    x: f64
    y: f64
    z: f64
    @trace
    def __init__(self, x: tp.Union['f64', FloatLiteral] = FloatLiteral(), y: tp.Union['f64', FloatLiteral] = FloatLiteral(), z: tp.Union['f64', FloatLiteral] = FloatLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.double3", double3, _literal_to_value(x, type_of(double3)), _literal_to_value(y, type_of(double3)), _literal_to_value(z, type_of(double3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__add__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__pow__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['double3', f64, FloatLiteral]) -> 'double3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.double3", [double3, __escape__( tp.Union[double3, f64, FloatLiteral])], double3,  self, _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8].default()), 3))
class byte3:
    x: i8
    y: i8
    z: i8
    @trace
    def __init__(self, x: tp.Union['i8', IntLiteral] = IntLiteral(), y: tp.Union['i8', IntLiteral] = IntLiteral(), z: tp.Union['i8', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.byte3", byte3, _literal_to_value(x, type_of(byte3)), _literal_to_value(y, type_of(byte3)), _literal_to_value(z, type_of(byte3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__add__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__and__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__or__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['byte3', i8, IntLiteral]) -> 'byte3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.byte3", [byte3, __escape__( tp.Union[byte3, i8, IntLiteral])], byte3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8].default()), 3))
class ubyte3:
    x: u8
    y: u8
    z: u8
    @trace
    def __init__(self, x: tp.Union['u8', IntLiteral] = IntLiteral(), y: tp.Union['u8', IntLiteral] = IntLiteral(), z: tp.Union['u8', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ubyte3", ubyte3, _literal_to_value(x, type_of(ubyte3)), _literal_to_value(y, type_of(ubyte3)), _literal_to_value(z, type_of(ubyte3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__add__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__and__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__or__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ubyte3', u8, IntLiteral]) -> 'ubyte3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ubyte3", [ubyte3, __escape__( tp.Union[ubyte3, u8, IntLiteral])], ubyte3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16].default()), 3))
class short3:
    x: i16
    y: i16
    z: i16
    @trace
    def __init__(self, x: tp.Union['i16', IntLiteral] = IntLiteral(), y: tp.Union['i16', IntLiteral] = IntLiteral(), z: tp.Union['i16', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.short3", short3, _literal_to_value(x, type_of(short3)), _literal_to_value(y, type_of(short3)), _literal_to_value(z, type_of(short3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__add__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__and__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__or__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['short3', i16, IntLiteral]) -> 'short3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.short3", [short3, __escape__( tp.Union[short3, i16, IntLiteral])], short3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16].default()), 3))
class ushort3:
    x: u16
    y: u16
    z: u16
    @trace
    def __init__(self, x: tp.Union['u16', IntLiteral] = IntLiteral(), y: tp.Union['u16', IntLiteral] = IntLiteral(), z: tp.Union['u16', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ushort3", ushort3, _literal_to_value(x, type_of(ushort3)), _literal_to_value(y, type_of(ushort3)), _literal_to_value(z, type_of(ushort3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__add__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__and__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__or__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ushort3', u16, IntLiteral]) -> 'ushort3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ushort3", [ushort3, __escape__( tp.Union[ushort3, u16, IntLiteral])], ushort3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32].default()), 3))
class int3:
    x: i32
    y: i32
    z: i32
    @trace
    def __init__(self, x: tp.Union['i32', IntLiteral] = IntLiteral(), y: tp.Union['i32', IntLiteral] = IntLiteral(), z: tp.Union['i32', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.int3", int3, _literal_to_value(x, type_of(int3)), _literal_to_value(y, type_of(int3)), _literal_to_value(z, type_of(int3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__add__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__and__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__or__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['int3', i32, IntLiteral]) -> 'int3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.int3", [int3, __escape__( tp.Union[int3, i32, IntLiteral])], int3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32].default()), 3))
class uint3:
    x: u32
    y: u32
    z: u32
    @trace
    def __init__(self, x: tp.Union['u32', IntLiteral] = IntLiteral(), y: tp.Union['u32', IntLiteral] = IntLiteral(), z: tp.Union['u32', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.uint3", uint3, _literal_to_value(x, type_of(uint3)), _literal_to_value(y, type_of(uint3)), _literal_to_value(z, type_of(uint3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__add__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__and__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__or__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['uint3', u32, IntLiteral]) -> 'uint3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.uint3", [uint3, __escape__( tp.Union[uint3, u32, IntLiteral])], uint3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64].default()), 3))
class long3:
    x: i64
    y: i64
    z: i64
    @trace
    def __init__(self, x: tp.Union['i64', IntLiteral] = IntLiteral(), y: tp.Union['i64', IntLiteral] = IntLiteral(), z: tp.Union['i64', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.long3", long3, _literal_to_value(x, type_of(long3)), _literal_to_value(y, type_of(long3)), _literal_to_value(z, type_of(long3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__add__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__and__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__or__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['long3', i64, IntLiteral]) -> 'long3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.long3", [long3, __escape__( tp.Union[long3, i64, IntLiteral])], long3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64].default()), 3))
class ulong3:
    x: u64
    y: u64
    z: u64
    @trace
    def __init__(self, x: tp.Union['u64', IntLiteral] = IntLiteral(), y: tp.Union['u64', IntLiteral] = IntLiteral(), z: tp.Union['u64', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ulong3", ulong3, _literal_to_value(x, type_of(ulong3)), _literal_to_value(y, type_of(ulong3)), _literal_to_value(z, type_of(ulong3))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__add__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'bool3': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], bool3,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__and__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__or__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ulong3', u64, IntLiteral]) -> 'ulong3': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ulong3", [ulong3, __escape__( tp.Union[ulong3, u64, IntLiteral])], ulong3,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[boolean].default()), 4))
class bool4:
    x: boolean
    y: boolean
    z: boolean
    w: boolean
    @trace
    def __init__(self, x: tp.Union['boolean', bool] = False, y: tp.Union['boolean', bool] = False, z: tp.Union['boolean', bool] = False, w: tp.Union['boolean', bool] = False) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.bool4", bool4, _literal_to_value(x, type_of(bool4)), _literal_to_value(y, type_of(bool4)), _literal_to_value(z, type_of(bool4)), _literal_to_value(w, type_of(bool4))))
        else:
            pass # TODO

    @trace
    def __eq__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other) # type: ignore
    @trace
    def __and__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__and__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__or__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['bool4', boolean, bool]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.bool4", [bool4, __escape__( tp.Union[bool4, boolean, bool])], bool4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f32].default()), 4))
class float4:
    x: f32
    y: f32
    z: f32
    w: f32
    @trace
    def __init__(self, x: tp.Union['f32', FloatLiteral] = FloatLiteral(), y: tp.Union['f32', FloatLiteral] = FloatLiteral(), z: tp.Union['f32', FloatLiteral] = FloatLiteral(), w: tp.Union['f32', FloatLiteral] = FloatLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.float4", float4, _literal_to_value(x, type_of(float4)), _literal_to_value(y, type_of(float4)), _literal_to_value(z, type_of(float4)), _literal_to_value(w, type_of(float4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__add__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__pow__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['float4', f32, FloatLiteral]) -> 'float4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.float4", [float4, __escape__( tp.Union[float4, f32, FloatLiteral])], float4,  self, _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[f64].default()), 4))
class double4:
    x: f64
    y: f64
    z: f64
    w: f64
    @trace
    def __init__(self, x: tp.Union['f64', FloatLiteral] = FloatLiteral(), y: tp.Union['f64', FloatLiteral] = FloatLiteral(), z: tp.Union['f64', FloatLiteral] = FloatLiteral(), w: tp.Union['f64', FloatLiteral] = FloatLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.double4", double4, _literal_to_value(x, type_of(double4)), _literal_to_value(y, type_of(double4)), _literal_to_value(z, type_of(double4)), _literal_to_value(w, type_of(double4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__add__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __truediv__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__truediv__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __rtruediv__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__rtruediv__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __itruediv__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__itruediv__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  Ref(self), _other)
    @trace
    def __pow__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__pow__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __rpow__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__rpow__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __ipow__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__ipow__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  Ref(self), _other)
    @trace
    def __floordiv__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['double4', f64, FloatLiteral]) -> 'double4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.double4", [double4, __escape__( tp.Union[double4, f64, FloatLiteral])], double4,  self, _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i8].default()), 4))
class byte4:
    x: i8
    y: i8
    z: i8
    w: i8
    @trace
    def __init__(self, x: tp.Union['i8', IntLiteral] = IntLiteral(), y: tp.Union['i8', IntLiteral] = IntLiteral(), z: tp.Union['i8', IntLiteral] = IntLiteral(), w: tp.Union['i8', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.byte4", byte4, _literal_to_value(x, type_of(byte4)), _literal_to_value(y, type_of(byte4)), _literal_to_value(z, type_of(byte4)), _literal_to_value(w, type_of(byte4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__add__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__and__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__or__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['byte4', i8, IntLiteral]) -> 'byte4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.byte4", [byte4, __escape__( tp.Union[byte4, i8, IntLiteral])], byte4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u8].default()), 4))
class ubyte4:
    x: u8
    y: u8
    z: u8
    w: u8
    @trace
    def __init__(self, x: tp.Union['u8', IntLiteral] = IntLiteral(), y: tp.Union['u8', IntLiteral] = IntLiteral(), z: tp.Union['u8', IntLiteral] = IntLiteral(), w: tp.Union['u8', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ubyte4", ubyte4, _literal_to_value(x, type_of(ubyte4)), _literal_to_value(y, type_of(ubyte4)), _literal_to_value(z, type_of(ubyte4)), _literal_to_value(w, type_of(ubyte4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__add__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__and__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__or__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ubyte4', u8, IntLiteral]) -> 'ubyte4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ubyte4", [ubyte4, __escape__( tp.Union[ubyte4, u8, IntLiteral])], ubyte4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i16].default()), 4))
class short4:
    x: i16
    y: i16
    z: i16
    w: i16
    @trace
    def __init__(self, x: tp.Union['i16', IntLiteral] = IntLiteral(), y: tp.Union['i16', IntLiteral] = IntLiteral(), z: tp.Union['i16', IntLiteral] = IntLiteral(), w: tp.Union['i16', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.short4", short4, _literal_to_value(x, type_of(short4)), _literal_to_value(y, type_of(short4)), _literal_to_value(z, type_of(short4)), _literal_to_value(w, type_of(short4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__add__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__and__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__or__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['short4', i16, IntLiteral]) -> 'short4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.short4", [short4, __escape__( tp.Union[short4, i16, IntLiteral])], short4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u16].default()), 4))
class ushort4:
    x: u16
    y: u16
    z: u16
    w: u16
    @trace
    def __init__(self, x: tp.Union['u16', IntLiteral] = IntLiteral(), y: tp.Union['u16', IntLiteral] = IntLiteral(), z: tp.Union['u16', IntLiteral] = IntLiteral(), w: tp.Union['u16', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ushort4", ushort4, _literal_to_value(x, type_of(ushort4)), _literal_to_value(y, type_of(ushort4)), _literal_to_value(z, type_of(ushort4)), _literal_to_value(w, type_of(ushort4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__add__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__and__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__or__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ushort4', u16, IntLiteral]) -> 'ushort4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ushort4", [ushort4, __escape__( tp.Union[ushort4, u16, IntLiteral])], ushort4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i32].default()), 4))
class int4:
    x: i32
    y: i32
    z: i32
    w: i32
    @trace
    def __init__(self, x: tp.Union['i32', IntLiteral] = IntLiteral(), y: tp.Union['i32', IntLiteral] = IntLiteral(), z: tp.Union['i32', IntLiteral] = IntLiteral(), w: tp.Union['i32', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.int4", int4, _literal_to_value(x, type_of(int4)), _literal_to_value(y, type_of(int4)), _literal_to_value(z, type_of(int4)), _literal_to_value(w, type_of(int4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__add__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__and__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__or__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['int4', i32, IntLiteral]) -> 'int4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.int4", [int4, __escape__( tp.Union[int4, i32, IntLiteral])], int4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u32].default()), 4))
class uint4:
    x: u32
    y: u32
    z: u32
    w: u32
    @trace
    def __init__(self, x: tp.Union['u32', IntLiteral] = IntLiteral(), y: tp.Union['u32', IntLiteral] = IntLiteral(), z: tp.Union['u32', IntLiteral] = IntLiteral(), w: tp.Union['u32', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.uint4", uint4, _literal_to_value(x, type_of(uint4)), _literal_to_value(y, type_of(uint4)), _literal_to_value(z, type_of(uint4)), _literal_to_value(w, type_of(uint4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__add__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__and__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__or__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['uint4', u32, IntLiteral]) -> 'uint4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.uint4", [uint4, __escape__( tp.Union[uint4, u32, IntLiteral])], uint4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[i64].default()), 4))
class long4:
    x: i64
    y: i64
    z: i64
    w: i64
    @trace
    def __init__(self, x: tp.Union['i64', IntLiteral] = IntLiteral(), y: tp.Union['i64', IntLiteral] = IntLiteral(), z: tp.Union['i64', IntLiteral] = IntLiteral(), w: tp.Union['i64', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.long4", long4, _literal_to_value(x, type_of(long4)), _literal_to_value(y, type_of(long4)), _literal_to_value(z, type_of(long4)), _literal_to_value(w, type_of(long4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__add__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__and__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__or__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['long4', i64, IntLiteral]) -> 'long4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.long4", [long4, __escape__( tp.Union[long4, i64, IntLiteral])], long4,  Ref(self), _other)

@builtin_type(_hir.VectorType(tp.cast(_hir.ScalarType, _ctx.types[u64].default()), 4))
class ulong4:
    x: u64
    y: u64
    z: u64
    w: u64
    @trace
    def __init__(self, x: tp.Union['u64', IntLiteral] = IntLiteral(), y: tp.Union['u64', IntLiteral] = IntLiteral(), z: tp.Union['u64', IntLiteral] = IntLiteral(), w: tp.Union['u64', IntLiteral] = IntLiteral()) -> None:
        if is_jit():
            assign(self, __intrinsic__("init.ulong4", ulong4, _literal_to_value(x, type_of(ulong4)), _literal_to_value(y, type_of(ulong4)), _literal_to_value(z, type_of(ulong4)), _literal_to_value(w, type_of(ulong4))))
        else:
            pass # TODO

    @trace
    def __add__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__add__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __radd__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__radd__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __iadd__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__iadd__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __sub__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__sub__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rsub__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rsub__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __isub__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__isub__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __mul__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__mul__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rmul__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rmul__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __imul__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__imul__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __mod__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__mod__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rmod__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rmod__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __imod__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__imod__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __lt__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__lt__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __le__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__le__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __gt__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__gt__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ge__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ge__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __eq__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__eq__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __ne__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'bool4': # type: ignore
        return __intrinsic_checked__("cmp.__ne__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], bool4,  self, _other) # type: ignore
    @trace
    def __floordiv__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__floordiv__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rfloordiv__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rfloordiv__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __ifloordiv__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__ifloordiv__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __lshift__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__lshift__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rlshift__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rlshift__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __ilshift__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__ilshift__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __rshift__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rshift__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rrshift__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rrshift__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __irshift__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__irshift__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __and__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__and__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rand__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rand__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __iand__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__iand__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __or__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__or__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __ror__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__ror__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __ior__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__ior__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)
    @trace
    def __xor__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__xor__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __rxor__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__rxor__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  self, _other)
    @trace
    def __ixor__(self, _other:  tp.Union['ulong4', u64, IntLiteral]) -> 'ulong4': # type: ignore
        return __intrinsic_checked__("binop.__ixor__.ulong4", [ulong4, __escape__( tp.Union[ulong4, u64, IntLiteral])], ulong4,  Ref(self), _other)

__all__ = ['FLOAT_TYPES', 'FloatType', 'abs', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh', 'ceil', 'cos', 'cosh', 'exp', 'floor', 'log', 'log10', 'log2', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc', 'atan2', 'copysign', 'boolean', 'f32', 'f64', 'i8', 'u8', 'i16', 'u16', 'i64', 'u64', 'i32', 'u32', 'bool2', 'float2', 'double2', 'byte2', 'ubyte2', 'short2', 'ushort2', 'int2', 'uint2', 'long2', 'ulong2', 'bool3', 'float3', 'double3', 'byte3', 'ubyte3', 'short3', 'ushort3', 'int3', 'uint3', 'long3', 'ulong3', 'bool4', 'float4', 'double4', 'byte4', 'ubyte4', 'short4', 'ushort4', 'int4', 'uint4', 'long4', 'ulong4', 'f32', 'i32']
