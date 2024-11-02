from types import UnionType
from typing import Any, Callable, List, Optional, Set, TypeVar
import typing
from luisa_lang import hir
import inspect
from luisa_lang.utils import get_full_name, get_union_args
from luisa_lang.classinfo import register_class, class_typeinfo, MethodType, _get_cls_globalns
import functools

_T = TypeVar("_T", bound=type)
_F = TypeVar("_F", bound=Callable[..., Any])


def _builtin_type(ty: hir.Type, *args, **kwargs) -> Callable[[_T], _T]:
    def decorator(cls: _T) -> _T:
        cls_name = get_full_name(cls)
        ctx = hir.GlobalContext.get()
        ctx.types[cls] = ty

        register_class(cls)
        cls_info = class_typeinfo(cls)
        globalns = _get_cls_globalns(cls)

        def make_type_rule(
            name: str, method: MethodType
        ) -> hir.BuiltinTypeRule:

            # # print(f'{cls_name}.{name}', signature)
            member = getattr(cls, name)
            signature = inspect.signature(member, globals=globalns)
            type_hints = typing.get_type_hints(member, globalns=globalns)
            parameters = signature.parameters
            return_type = method.return_type
            semantics: List[hir.ParameterSemantic] = []
            if not isinstance(return_type, type):
                raise hir.TypeInferenceError(None,
                                             f"Valid return type annotation required for {cls_name}.{name}"
                                             )
            parameters_list = list(parameters.values())
            for i, arg in enumerate(args):
                param = parameters_list[i]
                if param.name == "self":
                    # self is always passed by reference
                    semantics.append(hir.ParameterSemantic.BYREF)
                else:
                    # other parameters are passed by value
                    semantics.append(hir.ParameterSemantic.BYVAL)

            def type_rule(args: List[hir.Type]) -> hir.Type:

                if len(args) > len(parameters_list):
                    raise hir.TypeInferenceError(None,
                                                 f"Too many arguments for {cls_name}.{name} expected at most {len(parameters_list)} but got {len(args)}"
                                                 )
                for i, arg in enumerate(args):
                    param = parameters_list[i]
                    param_ty = type_hints.get(param.name)
                    if param.name == "self":
                        if arg != ty:
                            if i != 0:
                                raise hir.TypeInferenceError(None,
                                                             f"Expected {cls_name}.{name} to be called with an instance of {cls_name} as the first argument but got {arg}"
                                                             )
                            raise hir.TypeInferenceError(None,
                                                         f"Expected {cls_name}.{name} to be called with an instance of {cls_name} but got {arg}"
                                                         )

                        continue
                    if param_ty is None:
                        raise hir.TypeInferenceError(None,
                                                     f"Parameter type annotation required for {cls_name}.{name}"
                                                     )

                    def check(anno_tys: List[type | Any]):
                        possible_failed_reasons: List[str] = []
                        for anno_ty in anno_tys:
                            param_ir_ty = ctx.types.get(anno_ty)
                            if param_ir_ty is None:
                                possible_failed_reasons.append(
                                    f"Type {anno_ty} is not a valid DSL type"
                                )
                                continue
                            if hir.is_type_compatible_to(arg, param_ir_ty):
                                return
                            possible_failed_reasons.append(
                                f"Expected {cls_name}.{name} to be called with {anno_ty} but got {arg}"
                            )
                        raise hir.TypeInferenceError(None,
                                                     f"Possible reasons {possible_failed_reasons}"
                                                     )

                    union_args = get_union_args(param_ty)
                    if union_args == []:
                        union_args = [param_ty]
                    check(union_args)
                if name == '__init__':
                    return ty
                if return_type:
                    return ctx.types[return_type]
                else:
                    return hir.UnitType()

            return hir.BuiltinTypeRule(type_rule, semantics)

        def make_builtin():
            for name, member in cls_info.methods.items():
                type_rule = make_type_rule(name, member)
                builtin = hir.BuiltinFunction(
                    f"{cls_name}.{name}",
                    type_rule,
                )
                ty.methods[name] = builtin

        make_builtin()
        return cls

    return decorator


def _builtin(func: _F) -> _F:
    return func


def _intrinsic_impl(*args, **kwargs) -> Any:
    raise NotImplementedError(
        "intrinsic functions should not be called in host-side Python code. "
        "Did you mistakenly called a DSL function?"
    )
