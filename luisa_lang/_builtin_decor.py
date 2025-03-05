from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Set, TypeVar, cast
import typing

from lang_runtime import is_jit
from utils import get_full_name, unique_hash
from luisa_lang import hir
from luisa_lang import classinfo
from luisa_lang import ast_rewrite
import inspect
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeAlias,
    TypeVar,
    Union,
    Generic,
    Literal,
    overload,
    Any,
)


def _parse_type(ty: classinfo.VarType) -> hir.Type:
    match ty:
        case Type() as t:
            return hir.get_dsl_type(t).default()
        case classinfo.GenericInstance() as gi:
            template = hir.get_dsl_type(gi.origin)
            return template.instantiate(tuple(gi.args))
        case _:
            raise NotImplementedError()


def _dsl_struct_impl[T](cls: type[T], ir_ty_override: hir.Type | None = None) -> type[T]:
    ctx = hir.GlobalContext()
    assert cls not in ctx.types, f"Class {cls} is already registered in the global context"
    classinfo.register_class(cls)
    cls_info = classinfo.class_typeinfo(cls)
    is_generic = len(cls_info.type_vars) > 0
    globalns = classinfo._get_cls_globalns(cls)
    globalns[cls.__name__] = cls

    def instantiation_func(args: Tuple[hir.TypeTemplateArg, ...]) -> hir.Type:
        if not is_generic:
            assert len(
                args) == 0, f"Expected 0 type arguments but got {len(args)}"
        instantiated_cls = cls_info.instantiate(list(args))
        ir_ty: hir.Type
        if ir_ty_override is None:
            fields: List[Tuple[str, hir.Type]] = []
            for name, field in instantiated_cls.fields.items():
                field_ty = _parse_type(field)
                if field_ty is None:
                    raise hir.TypeCheckError(
                        None, f"Cannot infer type for field {name} of {cls.__name__}")
                fields.append((name, field_ty))
            ir_ty = hir.StructType(
                f'{cls.__name__}_{unique_hash(cls.__qualname__)}', cls.__qualname__, fields)
        else:
            ir_ty = ir_ty_override
        for name in cls_info.methods:
            method_object = getattr(cls, name)
            template = _make_func_template(
                method_object, globalns)
            ir_ty.methods[name] = template
        return ir_ty

    ctx.types[cls] = hir.TypeTemplate(instantiation_func)
    return cls


def _rewrite_func(f: Callable[..., Any]) -> Callable[..., Any]:
    if hasattr(f, '__luisa_func__'):
        return getattr(f, '__luisa_func__')
    rewritten = ast_rewrite.rewrite_function(f)
    setattr(f, '__luisa_func__', rewritten)
    return rewritten


def _make_func_template(f: Callable[..., Any], globalns: Dict[str, Any], trace_only: bool) -> hir.FunctionTemplate:
    sig = classinfo.parse_func_signature(f, globalns, [], False)
    rewritten = _rewrite_func(f)

    def instantiation_func(args: Tuple[hir.FunctionTemplateArg, ...]) -> hir.Function:
        raise NotImplementedError()


def struct[T](cls: type[T]) -> type[T]:
    return _dsl_struct_impl(cls)


def trace[F:Callable[..., Any]](f: F) -> F:
    return f


def func[F:Callable[..., Any]](f: F) -> F:
    def wrapper(*args, **kwargs):
        if not is_jit():
            return f(*args, **kwargs)
        if hasattr(f, '__luisa_func__'):
            return getattr(f, '__luisa_func__')(*args, **kwargs)
    return cast(F, wrapper)

# T = TypeVar('T')
# _T = TypeVar("_T", bound=type)
# _F = TypeVar("_F", bound=Callable[..., Any])


# def intrinsic(name: str, ret_type: type[T], *args, **kwargs) -> T:
#     raise NotImplementedError(
#         "intrinsic functions should not be called in host-side Python code. "
#         "Did you mistakenly called a DSL function?"
#     )

# def byref(value: T) -> T:
#     """Indicate that the value is a reference/should be passed by reference
#     Example:

#     ```python
#     x: lc.Ref[int] = byref(some_value) # x is bound to the reference of some_value
#     ```
#     """

#     raise NotImplementedError(
#         "byref should not be called in host-side Python code. "
#         "Did you mistakenly called a DSL function?"
#     )

# parse._add_special_function('byref', byref)

# def _is_method(f):
#     if inspect.ismethod(f):
#         return True
#     return inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__


# class _ObjKind(Enum):
#     BUILTIN_TYPE = auto()
#     STRUCT = auto()
#     FUNC = auto()
#     KERNEL = auto()


# def _make_func_template(f: Callable[..., Any], func_name: str, func_sig: Optional[MethodType],
#                         func_globals: Dict[str, Any], foreign_type_var_ns: Dict[TypeVar, hir.Type],
#                         props: hir.FuncProperties, self_type: Optional[hir.Type] = None):
#     # parsing_ctx = _parse.ParsingContext(func_name, func_globals)
#     # func_sig_parser = _parse.FuncParser(func_name, f, parsing_ctx, self_type)
#     # func_sig = func_sig_parser.parsed_func
#     # params = [v.name for v in func_sig_parser.params]
#     # is_generic = func_sig_parser.p_ctx.type_vars != {}
#     if func_sig is None:
#         func_sig = classinfo.parse_func_signature(f, func_globals, [])

#     func_sig_converted, sig_parser = parse.convert_func_signature(
#         func_sig, func_name, props, func_globals, foreign_type_var_ns, {}, self_type)
#     implicit_type_params = sig_parser.implicit_type_params
#     implicit_generic_params: Set[hir.GenericParameter] = set()
#     for p in implicit_type_params.values():
#         assert isinstance(p, hir.SymbolicType)
#         implicit_generic_params.add(p.param)

#     def parsing_func(args: hir.FunctionTemplateResolvingArgs) -> hir.Function:
#         type_var_ns: Dict[TypeVar, hir.Type] = foreign_type_var_ns.copy()
#         mapped_implicit_type_params: Dict[str,
#                                           hir.Type] = dict()
#         assert func_sig is not None
#         type_parser = parse.TypeParser(
#             func_name, func_globals, type_var_ns, self_type, 'instantiate')
#         for (tv, t) in func_sig.env.items():
#             type_var_ns[tv] = unwrap(type_parser.parse_type(t))
#         if is_generic:
#             mapping = hir.match_func_template_args(func_sig_converted, args)
#             if isinstance(mapping, hir.TypeInferenceError):
#                 raise mapping
#             if len(mapping) != len(func_sig_converted.generic_params):
#                 raise hir.TypeInferenceError(
#                     None, "not all type parameters are resolved")
#             for p in func_sig_converted.generic_params:
#                 if p not in mapping:
#                     raise hir.TypeInferenceError(
#                         None, f"type parameter {p} is not resolved")
#                 if p not in implicit_generic_params:
#                     type_var_ns[sig_parser.generic_param_to_type_var[p]
#                                 ] = mapping[p]

#             for name, itp, in implicit_type_params.items():
#                 assert isinstance(itp, hir.SymbolicType)
#                 gp = itp.param
#                 mapped_type = mapping[gp]
#                 assert isinstance(mapped_type, hir.Type)
#                 mapped_implicit_type_params[name] = mapped_type

#         func_sig_instantiated, _p = parse.convert_func_signature(
#             func_sig, func_name, props, func_globals, type_var_ns, mapped_implicit_type_params, self_type, mode='instantiate')
#         # print(func_name, func_sig)
#         assert len(
#             func_sig_instantiated.generic_params) == 0, f"generic params should be resolved but found {func_sig_instantiated.generic_params}"
#         assert not isinstance(
#             func_sig_instantiated.return_type, hir.SymbolicType)
#         func_parser = parse.FuncParser(
#             func_name, f, func_sig_instantiated, func_globals, type_var_ns, self_type)
#         ret = func_parser.parse_body()
#         ret.inline_hint = props.inline
#         ret.export = props.export
#         return ret
#     params = [v[0] for v in func_sig.args]
#     is_generic = len(func_sig_converted.generic_params) > 0
#     # print(
#     # f"func {func_name} is_generic: {is_generic} {func_sig_converted.generic_params}")
#     return hir.FunctionTemplate(func_name, params, parsing_func, is_generic)


# _TT = TypeVar('_TT')


# def _dsl_func_impl(f: _TT, kind: _ObjKind, attrs: Dict[str, Any]) -> _TT:
#     assert inspect.isfunction(f), f"{f} is not a function"
#     # print(hir.GlobalContext.get)
#     ctx = hir.GlobalContext.get()
#     func_name = get_full_name(f)
#     func_globals: Any = getattr(f, "__globals__", {})
#     props = _parse_func_kwargs(attrs)
#     is_method = _is_method(f)
#     setattr(f, '__luisa_func_props__', props)
#     if is_method:
#         return typing.cast(_TT, f)
#     if kind == _ObjKind.FUNC:
#         template = _make_func_template(
#             f, func_name, None, func_globals, {}, props)
#         ctx.functions[f] = template
#         setattr(f, "__luisa_func__", template)
#         return typing.cast(_TT, f)
#     else:
#         raise NotImplementedError()
#         # return cast(_T, f)


# _MakeTemplateFn = Callable[[List[hir.GenericParameter]], hir.Type]
# _InstantiateFn = Callable[[List[hir.Type]], hir.Type]


# def _dsl_struct_impl(cls: type[_TT], attrs: Dict[str, Any], ir_ty_override: hir.Type | Tuple[_MakeTemplateFn, _InstantiateFn] | None = None, opqaue_override: str | None = None) -> type[_TT]:
#     ctx = hir.GlobalContext.get()
#     register_class(cls)
#     assert not (ir_ty_override is not None and opqaue_override is not None)
#     cls_info = class_typeinfo(cls)
#     globalns = _get_cls_globalns(cls)
#     globalns[cls.__name__] = cls
#     type_var_to_generic_param: Dict[TypeVar, hir.GenericParameter] = {}
#     for type_var in cls_info.type_vars:
#         type_var_to_generic_param[type_var] = hir.GenericParameter(
#             type_var.__name__, cls.__qualname__)
#     generic_params = [type_var_to_generic_param[tv]
#                       for tv in cls_info.type_vars]

#     def parse_fields(tp: parse.TypeParser, self_ty: hir.Type):
#         fields: List[Tuple[str, hir.Type]] = []
#         for name, field in cls_info.fields.items():
#             field_ty = tp.parse_type(field)
#             if field_ty is None:
#                 raise hir.TypeInferenceError(
#                     None, f"Cannot infer type for field {name} of {cls.__name__}")
#             fields.append((name, field_ty))
#         if len(fields) > 0:
#             if isinstance(self_ty, hir.StructType):
#                 self_ty.fields = fields
#             elif isinstance(self_ty, hir.BoundType):
#                 assert isinstance(self_ty.instantiated, hir.StructType)
#                 self_ty.instantiated.fields = fields
#             else:
#                 raise NotImplementedError()

#     def parse_methods(type_var_ns: Dict[TypeVar, hir.Type | Any], self_ty: hir.Type,):
#         for name in cls_info.methods:
#             if name == '__setitem__':  # __setitem__ is ignored deliberately
#                 continue
#             method_object = getattr(cls, name)
#             props: hir.FuncProperties
#             if hasattr(method_object, '__luisa_func_props__'):
#                 props = getattr(method_object, '__luisa_func_props__')
#             else:
#                 props = hir.FuncProperties()
#             method_sig = cls_info.methods[name]
#             def is_ref_type(rt:classinfo.VarType):
#                 if not isinstance(rt, classinfo.AnnotatedType):
#                     return False
#                 anno = rt.annotations[0]
#                 return anno is byref
#             if name == '__getitem__':
#                 assert is_ref_type(method_sig.return_type), f"function `{cls.__qualname__}.{name}` __getitem__ should return a RefType but got {
#                     method_sig.return_type}"
#                 # raise NotImplementedError()
#             template = _make_func_template(
#                 method_object, get_full_name(method_object), method_sig, globalns, type_var_ns, props, self_type=self_ty)
#             if isinstance(self_ty, hir.BoundType):
#                 assert isinstance(self_ty.instantiated,
#                                   (hir.ArrayType, hir.StructType, hir.OpaqueType))
#                 self_ty.instantiated.methods[name] = template
#             else:
#                 self_ty.methods[name] = template
#     ir_ty: hir.Type
#     if ir_ty_override is not None:
#         if isinstance(ir_ty_override, hir.Type):
#             ir_ty = ir_ty_override
#         else:
#             ir_ty = ir_ty_override[0](generic_params)
#     elif opqaue_override is not None:
#         ir_ty = hir.OpaqueType(opqaue_override)
#     else:
#         ir_ty = hir.StructType(
#             f'{cls.__name__}_{unique_hash(cls.__qualname__)}', cls.__qualname__, [])
#         type_parser = parse.TypeParser(
#             cls.__qualname__, globalns, {}, ir_ty, 'parse')

#         parse_fields(type_parser, ir_ty)
#     is_generic = len(cls_info.type_vars) > 0
#     if is_generic:
#         def monomorphization_func(args: List[hir.Type]) -> hir.Type:
#             assert isinstance(ir_ty, hir.ParametricType)
#             type_var_ns = {}
#             if len(args) != len(cls_info.type_vars):
#                 raise hir.TypeInferenceError(
#                     None, f"Expected {len(cls_info.type_vars)} type arguments but got {len(args)}")
#             for i, arg in enumerate(args):
#                 type_var_ns[cls_info.type_vars[i]] = arg
#             hash_s = unique_hash(f'{cls.__qualname__}_{args}')
#             inner_ty: hir.Type
#             if ir_ty_override is not None:
#                 assert isinstance(ir_ty_override, tuple)
#                 inner_ty = ir_ty_override[1](args)
#             elif opqaue_override:
#                 inner_ty = hir.OpaqueType(opqaue_override, args[:])
#             else:
#                 inner_ty = hir.StructType(
#                     f'{cls.__name__}_{hash_s}M', f'{cls.__qualname__}[{",".join([str(a) for a in args])}]', [])
#             mono_self_ty = hir.BoundType(ir_ty, args, inner_ty)
#             mono_type_parser = parse.TypeParser(
#                 cls.__qualname__, globalns, type_var_ns, mono_self_ty, 'instantiate')
#             parse_fields(mono_type_parser, mono_self_ty)
#             parse_methods(type_var_ns, mono_self_ty)
#             return inner_ty
#         ir_ty = hir.ParametricType(
#             list(type_var_to_generic_param.values()), ir_ty, monomorphization_func)
#     else:
#         pass
#     ctx.types[cls] = ir_ty
#     if not is_generic:
#         parse_methods({}, ir_ty)
#     return cls


# def _dsl_decorator_impl(obj: _TT, kind: _ObjKind, attrs: Dict[str, Any]) -> _TT:
#     if kind == _ObjKind.STRUCT:
#         assert isinstance(obj, type), f"{obj} is not a type"
#         return typing.cast(_TT, _dsl_struct_impl(obj, attrs))
#     elif kind == _ObjKind.FUNC or kind == _ObjKind.KERNEL:
#         return _dsl_func_impl(obj, kind, attrs)
#     raise NotImplementedError()


# def opaque(name: str) -> Callable[[type[_TT]], type[_TT]]:
#     """
#     Mark a class as a DSL opaque type.

#     Example:
#     ```python
#     @luisa.opaque("Buffer")
#     class Buffer(Generic[T]):
#         pass
#     ```
#     """
#     def wrapper(cls: type[_TT]) -> type[_TT]:
#         return _dsl_struct_impl(cls, {}, opqaue_override=name)
#     return wrapper


# def struct(cls: type[_TT]) -> type[_TT]:
#     """
#     Mark a class as a DSL struct.

#     Example:
#     ```python
#     @luisa.struct
#     class Sphere:
#         center: luisa.float3
#         radius: luisa.float

#         def volume(self) -> float:
#             return 4.0 / 3.0 * math.pi * self.radius ** 3
#     ```
#     """
#     return _dsl_decorator_impl(cls, _ObjKind.STRUCT, {})


# def builtin_type(ty: hir.Type, *args, **kwargs) -> Callable[[type[_TT]], type[_TT]]:
#     def decorator(cls: type[_TT]) -> type[_TT]:
#         return typing.cast(type[_TT], _dsl_struct_impl(cls, {}, ir_ty_override=ty))
#     return decorator


# def builtin_generic_type(make_template: _MakeTemplateFn, instantiate: _InstantiateFn) -> Callable[[type[_TT]], type[_TT]]:
#     def decorator(cls: type[_TT]) -> type[_TT]:
#         return typing.cast(type[_TT], _dsl_struct_impl(cls, {}, ir_ty_override=(make_template, instantiate)))
#     return decorator


# _KernelType = TypeVar("_KernelType", bound=Callable[..., None])


# @overload
# def kernel(f: _KernelType) -> _KernelType: ...


# @overload
# def kernel(export: bool = False, **kwargs) -> Callable[[
#     _KernelType], _KernelType]: ...


# def kernel(*args, **kwargs) -> _KernelType | Callable[[_KernelType], _KernelType]:
#     if len(args) == 1 and len(kwargs) == 0:
#         f = args[0]
#         return f

#     def decorator(f):
#         return f

#     return decorator


# class InoutMarker:
#     value: str

#     def __init__(self, value: str):
#         self.value = value


# def _parse_func_kwargs(kwargs: Dict[str, Any]) -> hir.FuncProperties:
#     props = hir.FuncProperties()
#     inline = kwargs.get("inline", False)
#     if isinstance(inline, bool):
#         props.inline = inline
#     elif inline == "always":
#         props.inline = "always"
#     else:
#         raise ValueError(f"invalid value for inline: {inline}")

#     props.export = kwargs.get("export", False)
#     if not isinstance(props.export, bool):
#         raise ValueError(f"export should be a bool")
#     return props


# @overload
# def func(f: _F) -> _F: ...


# @overload
# def func(**kwargs) -> Callable[[_F], _F]: ...


# def func(*args, **kwargs) -> _F | Callable[[_F], _F]:
#     """
#     Mark a function as a DSL function.
#     Acceptable kwargs:
#     - inline: bool | "always"  # hint for inlining
#     - export: bool             # hint for exporting (for bundled C++ codegen)

#     Example:
#     ```python
#     @luisa.func(export=True)
#     def swap(a: Ref[T], b: Ref[T]) -> None:
#         a, b = b, a
#     ```
#     """

#     def impl(f: _F) -> _F:
#         return _dsl_decorator_impl(f, _ObjKind.FUNC, kwargs)

#     if len(args) == 1 and len(kwargs) == 0:
#         f = args[0]
#         return impl(f)

#     def decorator(f):
#         return impl(f)

#     return decorator


# def block[B:Callable[[], None]](block: B) -> B:
#     """
#     Define a block scope for DSL code.
#     Example:
#     ```python
#     x: int = 0
#     y: int = 1
#     @lc.block
#     def some_name():
#         nonlocal y
#         x = 1 # shadowing x
#         y = 2 # modify y
#     some_name() # block must be called immediately after definition
#     ```
#     """
#     return block
