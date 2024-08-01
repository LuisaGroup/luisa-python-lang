from typing import Any, Callable, List, TypedDict


class Serializer:
    pass


def export_funcs(export_funcs: List[Callable[..., Any]]) -> str:
    raise NotImplementedError


def export_all() -> str:
    raise NotImplementedError


__all__ = ["export_to_json"]
