import types

from _builtin_decor import func
from luisa_lang.math_types import *
from luisa_lang.core_types import Ref
import luisa_lang.hir as hir
from luisa_lang.lang_runtime import (
    assign,
    current_span,
    __intrinsic__,
    JitVar,
    push_to_current_bb,
)
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
    Annotated,
)

# from luisa_lang._builtin_decor import func, intrinsic, opaque, builtin_generic_type, byref, struct
# from luisa_lang import parse

# T = TypeVar("T")
# N = TypeVar("N")

# type Ref[T] = Annotated[T, byref]
# """ A *reference* type. """


# @func
# def dispatch_id() -> uint3:
#     return intrinsic("dispatch_id", uint3)


# @func
# def thread_id() -> uint3:
#     return intrinsic("thread_id", uint3)


# @func
# def block_id() -> uint3:
#     return intrinsic("block_id", uint3)


# def cast(target: type[T], value: Any) -> T:
#     """
#     Attempt to convert the value to the target type.
#     """
#     return intrinsic("cast", target, value)


# def bitcast(target: type[T], value: Any) -> T:
#     """
#     Attempt to convert the value to the target type, preserving the bit representation.
#     """
#     return intrinsic("bitcast", target, value)


# class ComptimeBlock:
#     def __init__(self):
#         pass

#     def __enter__(self):
#         pass

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass

#     def __call__(self):
#         pass


# class _ComptimeBlockMarker:
#     pass


# F = TypeVar("F", bound=Callable[..., Any])


# def instantiate(f: F, *args: List[type]) -> F:
#     raise NotImplementedError(
#         "instantiate should not be called in host-side Python code. ")


# @overload
# def comptime(a: _ComptimeBlockMarker) -> ComptimeBlock: ...


# @overload
# def comptime(src: str) -> Any: ...


# @overload
# def comptime(a: T) -> T: ...


# def comptime(a):
#     """
#     Allowing mixing normal python object as compile-time value with DSL code.
#     Usage:
#         - `lc.comptime(e)` marks the expression `e` as a compile-time value.
#         - `with lc.comptime() as block: ...` marks the block as a compile-time block.
#     """
#     if isinstance(a, _ComptimeBlockMarker):
#         return ComptimeBlock()
#     return a


# @func
# def trap() -> None:
#     """
#     Aborts the kernel execution
#     """
#     intrinsic("trap", types.NoneType)


# def device_assert(cond: bool, msg: str = "") -> typing.NoReturn:
#     """
#     Assert that the condition is true at runtime.
#     """
#     raise NotImplementedError(
#         "device_assert should not be called in host-side Python code. ")


# def sizeof(t: type[T]) -> u64:
#     raise NotImplementedError(
#         "sizeof should not be called in host-side Python code. ")


# @overload
# def range(n: T) -> List[T]: ...
# @overload
# def range(start: T, end: T) -> List[T]: ...
# @overload
# def range(start: T, end: T, step: T) -> List[T]: ...


# def range(*args, **kwargs):  # type: ignore
#     raise NotImplementedError(
#         "range should not be called in host-side Python code. ")


# parse._add_special_function("comptime", comptime)
# parse._add_special_function("intrinsic", intrinsic)
# parse._add_special_function("range", range)
# parse._add_special_function('reveal_type', typing.reveal_type)
# parse._add_special_function('cast', cast)
# parse._add_special_function('bitcast', bitcast)
# parse._add_special_function('device_assert', device_assert)
# parse._add_special_function('sizeof', sizeof)


# def static_assert(cond: Any, msg: str = ""):
#     pass


# def unroll(range_: Sequence[int]) -> Sequence[int]:
#     return range_


# @func
# def address_of(a: T) -> u64:
#     return intrinsic("address_of", u64, a)

# # class StaticEval:
# #


# def type_of_opt(value: Any) -> Optional[hir.Type]:
#     if isinstance(value, hir.Type):
#         return value
#     if isinstance(value, type):
#         return hir.GlobalContext.get().types[value]
#     return hir.GlobalContext.get().types.get(type(value))


# def typeof(value: Any) -> hir.Type:
#     ty = type_of_opt(value)
#     if ty is None:
#         raise TypeError(f"Cannot determine type of {value}")
#     return ty


# # _t = hir.SymbolicType(hir.GenericParameter("_T", "luisa_lang.lang"))
# # _n = hir.SymbolicConstant(hir.GenericParameter(
# #     "_N", "luisa_lang.lang")), typeof(u32)


# def _make_array_type(params: List[hir.GenericParameter]) -> hir.Type:
#     assert len(params) == 2
#     elem_ty = hir.SymbolicType(params[0])
#     size = hir.SymbolicConstant(params[1])
#     return hir.ParametricType(params, hir.ArrayType(elem_ty, size))


# def _instantiate_array_type(args: List[Any]) -> hir.Type:
#     assert len(args) == 2, "Array should have 2 arguments"
#     assert isinstance(
#         args[1], hir.LiteralType), f"Array size should be a Literal but found {args[1]} of type {type(args[1])}"
#     array_len = args[1].value
#     assert isinstance(
#         array_len, int), f"Array size should be an integer but found {array_len} of type {type(array_len)}"
#     return hir.ArrayType(args[0], array_len)


# @builtin_generic_type(
#     _make_array_type,
#     _instantiate_array_type
# )
# class Array(Generic[T, N]):
#     """
#     An array is a fixed-size collection of elements of type T. N need to be a Literal type.
#     Example:
#     ```python
#     arr = Array[int, Literal[10]]()
#     ```
#     """

#     def __init__(self) -> None:
#         self = intrinsic("init.array", Array[T, N])

#     def __getitem__(self, index: int | u32 | i64 | u64) -> Ref[T]:
#         return intrinsic("array.ref", T, byref(self), index)  # type: ignore

#     def __setitem__(self, index: int | u32 | i64 | u64, value: T) -> None:
#         pass

#     def __len__(self) -> u64:
#         return intrinsic("array.size", u64, self)  # type: ignore


# # def __buffer_ty():
# #     t = hir.GenericParameter("T", "luisa_lang.lang")
# #     return hir.ParametricType(
# #         [t], hir.OpaqueType("Buffer"), None
# #     )

# # @builtin_type(
# #     hir.ParametricType(
# #         [_t], [hir.TypeParameter(_t, bound=[])], hir.OpaqueType("Buffer")
# #     )
# # )


# @opaque("Buffer")
# class Buffer(Generic[T]):
#     """
#     A buffer is a contiguuos memory of elements of type T.
#     """

#     def __getitem__(self, index: int | u32 | i64 | u64) -> Ref[T]:
#         return intrinsic("buffer.ref",  Ref[T], self, index)  # type: ignore

#     def __setitem__(self,  index: int | u32 | i64 | u64,  value: T) -> None:
#         pass

#     def __len__(self) -> u64:
#         return intrinsic("buffer.size",  u64, self)  # type: ignore


# def _make_pointer_type(params: List[hir.GenericParameter]) -> hir.Type:
#     assert len(params) == 1
#     elem_ty = hir.SymbolicType(params[0])
#     return hir.ParametricType(params, hir.PointerType(elem_ty))


# def _inst_pointer_type(args: List[Any]) -> hir.Type:
#     assert len(args) == 1
#     return hir.PointerType(args[0])


# @builtin_generic_type(
#     _make_pointer_type,
#     _inst_pointer_type
# )
# class Pointer(Generic[T]):
#     """
#     A physical pointer (just like C pointer) to a memory location of type T.
#     Note that pointers might not be available in all backends.

#     ```python
#     p = Pointer[int](123456798) # 123456798 is the address of the memory location
#     i = p[0] # read the value at the memory location
#     p[0] = 10 # write the value at the memory location
#     # alternatively
#     i = p.read()
#     p.write(10)
#     # offset the pointer
#     x = p[1]
#     y = (p + 1).read()
#     ```
#     """

#     def __init__(self, addr: u64) -> None:
#         self = intrinsic("init.pointer", Pointer[T], addr)

#     def __getitem__(self, index:  i32 | i64 | u32 | u64) -> Ref[T]:
#         return intrinsic("pointer.read", Ref[T], self, index)  # type: ignore

#     def __setitem__(self, index: i32 | i64 | u32 | u64, value: T) -> None:
#         pass

#     def read(self) -> T:
#         return intrinsic("pointer.read", T, self)  # type: ignore

#     def write(self, value: T) -> None:
#         intrinsic("pointer.write", None, self, value)  # type: ignore

#     def __add__(self, offset: i32 | i64 | u32 | u64) -> 'Pointer[T]':
#         return intrinsic("pointer.add", Pointer[T], self, offset)

#     def __sub__(self, offset: i32 | i64 | u32 | u64) -> 'Pointer[T]':
#         return intrinsic("pointer.sub", Pointer[T], self, offset)


# @struct
# class RtxRay:
#     o: float3
#     d: float3
#     tmin: float
#     tmax: float

#     def __init__(self, o: float3, d: float3, tmin: float, tmax: float) -> None:
#         self.o = o
#         self.d = d
#         self.tmin = tmin
#         self.tmax = tmax


# @struct
# class RtxHit:
#     inst_id: u32
#     prim_id: u32
#     bary: float2

#     def __init__(self, inst_id: u32, prim_id: u32, bary: float2) -> None:
#         self.inst_id = inst_id
#         self.prim_id = prim_id
#         self.bary = bary


# @func
# def ray_query_pipeline(ray: RtxRay, on_surface_hit, on_procedural_hit) -> RtxHit:
#     return intrinsic("ray_query_pipeline", RtxHit, ray, on_surface_hit, on_procedural_hit)


@func
def copy[T: JitVar](v: T) -> T:
    """
    Copy a value of type T.
    """
    return __intrinsic__("copy", type(v), v)


__all__: List[str] = [
    "Ref",
    "copy",
    # 'Pointer',
    # 'Buffer',
    # 'Array',
    # 'range',
    # 'comptime',
    # 'address_of',
    # 'unroll',
    # 'static_assert',
    # 'type_of_opt',
    # 'typeof',
    # "dispatch_id",
    # "thread_id",
    # "block_id",
    # "intrinsic",
    # 'cast',
    # 'bitcast',
    # 'device_assert',
    # 'trap',
    # 'sizeof',
    # 'Ref'
]
