from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Set, TypeVar, cast
import typing

from lang_runtime import TraceContext, _invoke_function_tracer, is_jit
from utils import Lazy, get_full_name, unique_hash
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
    ctx = hir.GlobalContext.get()
    assert cls not in ctx.types, f"Class {cls} is already registered in the global context"

    # Register the class and get its type info
    classinfo.register_class(cls)
    cls_info = classinfo.class_typeinfo(cls)
    is_generic = len(cls_info.type_vars) > 0

    # Get the global namespace and register the class name
    globalns = classinfo._get_cls_globalns(cls)
    globalns[cls.__name__] = cls
    assert cls.__name__ in globalns

    def instantiation_func(args: hir.TypeTemplateArgs) -> hir.Type:
        # For non-generic classes, ensure no type args are provided
        if not is_generic:
            assert len(
                args) == 0, f"Expected 0 type arguments but got {len(args)}"

        # Instantiate the class with the provided type arguments
        instantiated_cls = cls_info.instantiate(list(args))

        # Create the IR type either from override or by building from fields
        ir_ty: hir.Type
        if ir_ty_override is None:
            # Build struct type from fields
            fields: List[Tuple[str, hir.Type]] = []
            for name, field in instantiated_cls.fields.items():
                field_ty = _parse_type(field)
                if field_ty is None:
                    raise hir.TypeCheckError(
                        None, f"Cannot infer type for field {name} of {cls.__name__}")
                fields.append((name, field_ty))

            # Create unique name for the struct type
            ir_ty = hir.StructType(
                f'{cls.__name__}_{unique_hash(cls.__qualname__)}',
                cls.__qualname__,
                fields)
        else:
            ir_ty = ir_ty_override

        # Register all methods of the class
        for name in cls_info.methods:
            method_object = getattr(cls, name)
            template = _get_func_template(method_object)
            if template is not None:
                ir_ty.methods[name] = template

        return ir_ty

    # Register the type template in the global context
    ctx.types[cls] = hir.TypeTemplate(tuple, instantiation_func)
    return cls


def _get_func_template(f: Callable[..., Any]) -> Optional[hir.FunctionTemplate]:
    if not hasattr(f, '__luisa_func__'):
        return None
    template = getattr(f, '__luisa_func__').get()
    assert isinstance(
        template, hir.FunctionTemplate), f"Function {f} is not a Luisa function"
    return template


def _rewrite_func(decorator_name: str, f: Callable[..., Any]) -> Callable[..., Any]:
    rewritten = ast_rewrite.rewrite_function(f, decorator_name)
    return rewritten


def _make_func_template(decorator_name: str, f: Callable[..., Any], globalns: Dict[str, Any], trace_only: bool) -> hir.FunctionTemplate:
    sig = classinfo.parse_func_signature(f, globalns, [], False)
    rewritten = _rewrite_func('func', f)

    def instantiation_func(args: hir.FunctionTemplateArgs) -> hir.Function:
        func = _invoke_function_tracer(
            'func', rewritten, args.args, args.kwargs)
        assert isinstance(func, hir.Function)
        return func

    return hir.FunctionTemplate(hir.FunctionTemplateArgs, instantiation_func)


def struct[T](cls: type[T]) -> type[T]:
    """
    Mark a class as a DSL struct.

    Example:
    ```python
    @luisa.struct
    class Sphere:
        center: luisa.float3
        radius: luisa.float

        @luisa.func
        def volume(self) -> float:
            return 4.0 / 3.0 * math.pi * self.radius ** 3
    ```
    """
    return _dsl_struct_impl(cls)


def builtin_type(ir_type: hir.Type):
    """
    Mark a class as a builtin type.

    Example:
    ```
    @builtin_type(_hir.FloatType(32))
    class f32:
        pass
    ```
    """
    def decorator(cls: type):
        return _dsl_struct_impl(cls, ir_type)
    return decorator


# class FunctionProxy:
#     compiled: bool
#     f: Callable[..., Any]
#     __doc__: str | None
#     __annotations__: Dict[str, type]
#     __name__: str

#     def __init__(self, f: Callable[..., Any], compiled: bool):
#         self.f = f
#         self.compiled = compiled
#         self.__doc__ = f.__doc__
#         self.__annotations__ = f.__annotations__
#         self.__name__ = f.__name__

#     def __get__(self, instance, _owner) -> Callable[..., Any]:
#         return lambda *args, **kwargs: self(instance, *args, **kwargs)

#     def __call__(self, *args, **kwargs) -> Any:
#         raise NotImplementedError()

def _trace_func_impl[F:Callable[..., Any]](f: F, mode: str) -> F:
    # Get the global namespace for the function
    globalns = classinfo._get_func_globalns(f)

    
    # Create the function template
    def template(): return _make_func_template(
        'func', f, globalns, trace_only=False)

    # Store the template on the function object
    setattr(f, '__luisa_func__', Lazy[hir.FunctionTemplate](template))

    def wrapper(*args, **kwargs):
        if not is_jit():
            # In non-JIT context, just call the original function
            return f(*args, **kwargs)

        template = cast(hir.FunctionTemplate,
                        getattr(f, '__luisa_func__').get())
        instantiated_func = template.instantiate(
            hir.FunctionTemplateArgs(args=list(args), kwargs=kwargs))

    # Copy over important attributes from the original function
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    wrapper.__annotations__ = f.__annotations__

    return cast(F, wrapper)


def trace[F:Callable[..., Any]](f: F) -> F:
    return _trace_func_impl(f, 'trace')


def func[F:Callable[..., Any]](f: F) -> F:
    """
    Decorator for Luisa functions that are compiled once and reused.
    Different from @trace, this avoids code duplication by compiling the function body only once.

    Example:
    ```python
    @luisa.func
    def add(a: float, b: float) -> float:
        return a + b
    ```
    """
    # Get the global namespace for the function
    globalns = classinfo._get_func_globalns(f)

    
    # Create the function template
    def template(): return _make_func_template(
        'func', f, globalns, trace_only=False)

    # Store the template on the function object
    setattr(f, '__luisa_func__', Lazy[hir.FunctionTemplate](template))

    def wrapper(*args, **kwargs):
        if not is_jit():
            # In non-JIT context, just call the original function
            return f(*args, **kwargs)

        template = cast(hir.FunctionTemplate,
                        getattr(f, '__luisa_func__').get())
        instantiated_func = template.instantiate(
            hir.FunctionTemplateArgs(args=list(args), kwargs=kwargs))

    # Copy over important attributes from the original function
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    wrapper.__annotations__ = f.__annotations__

    return cast(F, wrapper)
