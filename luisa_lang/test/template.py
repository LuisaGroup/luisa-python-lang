from luisa_lang import lang as lc
from typing import TypeVar, Any

T = TypeVar("T", bound=Any)


@lc.func
def add(x: T, y: T) -> T:
    return x + y
