import luisa_lang
from luisa_lang.lang import *

@builtin
def dispatch_id() -> uint3:
    return intrinsic_impl()

@builtin
def thread_id() -> uint3:
    return intrinsic_impl()

@builtin
def block_id() -> uint3:
    return intrinsic_impl()