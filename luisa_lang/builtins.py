from typing_extensions import TypeAliasType
from luisa_lang.lang import _builtin, _intrinsic_impl
from luisa_lang.lang import *


@_builtin
def dispatch_id() -> uint3:
    return _intrinsic_impl()


@_builtin
def thread_id() -> uint3:
    return _intrinsic_impl()


@_builtin
def block_id() -> uint3:
    return _intrinsic_impl()

# TODO: Implement the following builtins
# FloatType = TypeAliasType("FloatType", FloatTypeMarker)

# @_builtin
# def sin(x: FloatType) -> FloatType:
#     return _intrinsic_impl()

# @_builtin
# def cos(x: FloatType) -> FloatType:
#     return _intrinsic_impl()

# @_builtin
# def tan(x: FloatType) -> FloatType:
#     return _intrinsic_impl()

