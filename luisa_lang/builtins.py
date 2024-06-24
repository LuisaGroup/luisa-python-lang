import luisa_lang
from luisa_lang.lang import *

@lcpyc("builtin_function")
def dispatch_id() -> u32:
    return intrinsic_impl()
