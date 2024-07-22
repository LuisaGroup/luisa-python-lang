from typing import Optional, TypeVar

T = TypeVar("T")


def unwrap(opt: Optional[T]) -> T:
    if opt is None:
        raise ValueError("unwrap None")
    return opt
