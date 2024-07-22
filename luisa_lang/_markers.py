from typing import Any, Callable, TypeVar


_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Any])


def _builtin_type(any: _T, *args, **kwargs) -> _T:
    return any


def _builtin(func: _F, *args, **kwargs) -> _F:
    return func


def _intrinsic_impl(*args, **kwargs) -> Any:
    raise NotImplementedError(
        "intrinsic functions should not be called in normal Python code"
    )
