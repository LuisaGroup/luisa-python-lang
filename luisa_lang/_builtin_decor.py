from types import UnionType
from typing import Any, Callable, List, Optional, Set, TypeVar
import typing
from luisa_lang import hir
import inspect
from luisa_lang._utils import _get_full_name, get_union_args
from luisa_lang._classinfo import _register_class, _class_typeinfo, MethodType, _get_cls_globalns
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

        _register_class(cls)
        cls_info = _class_typeinfo(cls)
        globalns = _get_cls_globalns(cls)

        def make_type_rule(
            name: str, method: MethodType
        ) -> Callable[[List[hir.Type]], hir.Type]:

            # # print(f'{cls_name}.{name}', signature)
            member = getattr(cls, name)
            signature = inspect.signature(member, globals=globalns)
            type_hints = typing.get_type_hints(member, globalns=globalns)
            parameters = signature.parameters
            return_type = method.return_type
            if not isinstance(return_type, type):
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

                    def check(anno_tys: List[type | Any]):
                        possible_failed_reasons: List[str] = []
                        for anno_ty in anno_tys:
                            if anno_ty == float:
                                # match all hir.FloatType
                                if isinstance(arg, hir.FloatType):
                                    return
                                else:
                                    possible_failed_reasons.append(
                                        f"Expected {cls_name}.{name} to be called with {anno_ty} but got {arg}"
                                    )
                                    continue
                            if anno_ty == int:
                                if isinstance(arg, hir.IntType):
                                    return
                                else:
                                    possible_failed_reasons.append(
                                        f"Expected {cls_name}.{name} to be called with {anno_ty} but got {arg}"
                                    )
                                    continue
                            if anno_ty == bool:
                                if isinstance(arg, hir.BoolType):
                                    return
                                else:
                                    possible_failed_reasons.append(
                                        f"Expected {cls_name}.{name} to be called with {anno_ty} but got {arg}"
                                    )
                                    continue

                            param_ir_ty = ctx.types.get(anno_ty)
                            if param_ir_ty is None:
                                possible_failed_reasons.append(
                                    f"Type {anno_ty} is not a valid DSL type"
                                )
                                continue
                            if arg == param_ir_ty:
                                return
                            possible_failed_reasons.append(
                                f"Expected {cls_name}.{name} to be called with {anno_ty} but got {arg}"
                            )
                        raise hir.TypeInferenceError(
                            f"Expected {cls_name}.{name} to be called with one of {possible_failed_reasons}"
                        )

                    union_args = get_union_args(param_ty)
                    if union_args == []:
                        union_args = [param_ty]
                    check(union_args)
                if return_type:
                    return ctx.types[return_type]
                else:
                    return hir.UnitType()

            return type_rule

        def make_builtin():
            for name, member in cls_info.methods.items():
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
