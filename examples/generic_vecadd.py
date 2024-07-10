from typing import Any, TypeVar
import luisa_lang
from luisa_lang import Buffer, dispatch_id, static_assert

T = TypeVar("T", bound=Any)


@luisa_lang.kernel
def vecadd(a: Buffer[T], b: Buffer[T], c: Buffer[T]):
    static_assert(
        type(a[0] + b[0]) == type(c[0]),
        f"Type {type(a)} does not support addition.",
    )
    tid = dispatch_id().x
    c[tid] = a[tid] + b[tid]
