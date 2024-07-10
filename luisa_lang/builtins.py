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