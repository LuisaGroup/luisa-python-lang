from types import UnionType
from typing import Any, Callable, List, Set, TypeVar
import typing
from luisa_lang import hir
import inspect
from luisa_lang._utils import _get_full_name
import functools

_T = TypeVar("_T", bound=type)
_F = TypeVar("_F", bound=Callable[..., Any])


@functools.lru_cache(maxsize=None)
def _retrieve_generic_params(cls: type) -> Set[TypeVar]:
    if hasattr(cls, "__orig_bases__"):
        orig_bases = cls.__orig_bases__
        for base in orig_bases:
            print(base, typing.get_args(base))
            _retrieve_generic_params(base)
    return set()


def _builtin_type(ty: hir.Type, *args, **kwargs) -> Callable[[_T], _T]:
    def decorator(cls: _T) -> _T:
        cls_name = _get_full_name(cls)
        ctx = hir.GlobalContext.get()
        ctx.types[cls] = ty

        cls_qualname = cls.__qualname__
        module = inspect.getmodule(cls)
        globalns = module.__dict__
        globalns[cls.__name__] = cls
        assert module is not None
        assert (
            "<locals>" not in cls_qualname
        ), f"Cannot use local class {cls_qualname} as a DSL type. Must be a top-level class!"
        ctx = hir.GlobalContext.get()

        _retrieve_generic_params(cls)

        def make_type_rule(
            name: str, member: Any
        ) -> Callable[[List[hir.Type]], hir.Type]:

            # print(f'{cls_name}.{name}', signature)
            signature = inspect.signature(member)
            type_hints = typing.get_type_hints(member, globalns=globalns)
            parameters = signature.parameters
            return_type = type_hints.get("return")
            if return_type and not isinstance(return_type, type):
                raise hir.TypeInferenceError(
                    f"Valid return type annotation required for {cls_name}.{name}"
                )

            def type_rule(args: List[hir.Type]) -> hir.Type:
                if len(args) > len(parameters):
                    raise hir.TypeInferenceError(
                        f"Too many arguments for {cls_name}.{name} expected at most {len(parameters)} but got {len(args)}"
                    )
                parameters_list = list(parameters.values())
                for i, arg in enumerate(args):
                    param = parameters_list[i]
                    param_ty = type_hints.get(param.name)
                    if param.name == "self":
                        if arg != ty:
                            if i != 0:
                                raise hir.TypeInferenceError(
                                    f"Expected {cls_name}.{name} to be called with an instance of {cls_name} as the first argument but got {arg}"
                                )
                            raise hir.TypeInferenceError(
                                f"Expected {cls_name}.{name} to be called with an instance of {cls_name} but got {arg}"
                            )
                        continue
                    if param_ty is None:
                        raise hir.TypeInferenceError(
                            f"Parameter type annotation required for {cls_name}.{name}"
                        )

                    def check(anno_ty: hir.Type | None):
                        if anno_ty is None:
                            raise hir.TypeInferenceError(
                                f"Type {param_ty} is not a valid DSL type"
                            )
                        if arg != anno_ty:
                            raise hir.TypeInferenceError(
                                f"Expected {cls_name}.{name} to be called with {param_ty} but got {arg}"
                            )

                    if isinstance(param_ty, UnionType):
                        for a in param_ty.__args__:
                            check(a)
                    else:
                        param_ir_ty = ctx.types.get(param_ty)
                        check(param_ir_ty)
                if return_type:
                    return ctx.types[return_type]
                else:
                    return hir.UnitType()

            return type_rule

        def make_builtin():
            for name, member in inspect.getmembers(cls):
                if inspect.isfunction(member):
                    type_rule = make_type_rule(name, member)
                    builtin = hir.BuiltinFunction(
                        f"{cls_name}.{name}",
                        hir.TypeRule.from_fn(type_rule),
                    )
                    ty.methods[name] = builtin

        make_builtin()
        return cls

    return decorator


def _builtin(func: _F, *args, **kwargs) -> _F:
    return func


def _intrinsic_impl(*args, **kwargs) -> Any:
    raise NotImplementedError(
        "intrinsic functions should not be called in normal Python code"
    )
