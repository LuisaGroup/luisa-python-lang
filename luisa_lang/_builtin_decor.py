from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Set, TypeVar, cast
import typing

from luisa_lang.lang_runtime import (
    FlattenedTree,
    JitVar,
    TraceContext,
    _invoke_function_tracer,
    current_func,
    is_jit,
    tree_flatten,
)
from luisa_lang.utils import Lazy, get_full_name, inherit, unique_hash
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
        case type() as t:
            return hir.get_dsl_type(t).default()
        case classinfo.GenericInstance() as gi:
            template = hir.get_dsl_type(gi.origin)
            return template.instantiate(tuple(gi.args))
        case _:
            raise NotImplementedError()


def _dsl_struct_impl[T](
    cls: type[T], ir_ty_override: hir.Type | None = None
) -> type[T]:
    ctx = hir.GlobalContext.get()
    assert (
        cls not in ctx.types
    ), f"Class {cls} is already registered in the global context"

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
            assert len(args) == 0, f"Expected 0 type arguments but got {len(args)}"

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
                        None, f"Cannot infer type for field {name} of {cls.__name__}"
                    )
                fields.append((name, field_ty))

            # Create unique name for the struct type
            ir_ty = hir.StructType(
                f"{cls.__name__}_{unique_hash(cls.__qualname__)}",
                cls.__qualname__,
                fields,
            )
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
    # print(f'Registered class {cls} (id: {id(cls)} with type {ctx.types[cls]}')
    return cls


def _get_func_template(f: Callable[..., Any]) -> Optional[hir.FunctionTemplate]:
    if not hasattr(f, "__luisa_func__"):
        return None
    template = getattr(f, "__luisa_func__").get()
    assert isinstance(
        template, hir.FunctionTemplate
    ), f"Function {f} is not a Luisa function"
    return template


def _rewrite_func(decorator_name: str, f: Callable[..., Any]) -> Callable[..., Any]:
    rewritten = ast_rewrite.rewrite_function(f, decorator_name)
    return rewritten


def __inherit_jitvar(cls: type) -> type:
    new_cls: None | type = None

    def init_fn(self, *args, **kwargs):
        assert new_cls is not None
        JitVar.__init__(self, dtype=new_cls)
        assert self.dtype is not None

    new_cls = inherit(cls, JitVar, init_fn)
    return cast(type, new_cls)


def struct[T](cls: type[T]) -> type[T]:
    """
    Mark a class as a DSL struct. The class will automatically inherit from JitVar.

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
    cls = __inherit_jitvar(cls)
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
        cls = __inherit_jitvar(cls)
        return _dsl_struct_impl(cls, ir_type)

    return decorator


def trace[F: Callable[..., Any]](f: F) -> F:
    rewritten = _rewrite_func("trace", f)
    globalns = classinfo._get_func_globalns(f)

    def wrapper(
        *args,
        __lc_ctx__: Optional[TraceContext] = None,
        **kwargs,
    ):
        """
        Under jit context:,  the first argument is __lc_ctx__
        """
        # print(is_jit())
        if not is_jit():
            assert __lc_ctx__ is None
            # In non-JIT context, just call the original function
            return f(*args, **kwargs)
        else:
            func_tracer = current_func()
            old_globals = func_tracer.func_globals
            func_tracer.func_globals = globalns
            assert isinstance(__lc_ctx__, TraceContext)
            # Call the rewritten function with the trace context
            ret = rewritten(*args, **kwargs, __lc_ctx__=__lc_ctx__)
            # Restore the original globals
            func_tracer.func_globals = old_globals
            return ret

    # Copy over important attributes from the original function
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    wrapper.__annotations__ = f.__annotations__

    return cast(F, wrapper)


def _make_func_template(
    f: Callable[..., Any], globalns: Dict[str, Any]
) -> hir.FunctionTemplate:
    sig = classinfo.parse_func_signature(f, globalns, [], False)
    rewritten = _rewrite_func("func", f)

    def instantiation_func(args: hir.FunctionTemplateArgs) -> hir.Function:
        func = _invoke_function_tracer(rewritten, args, globalns)
        assert isinstance(func, hir.Function)
        return func

    return hir.FunctionTemplate(hir.FunctionTemplateArgs, instantiation_func)


def func[F: Callable[..., Any]](f: F) -> F:
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

    def template():
        return _make_func_template(f, globalns)

    # Store the template on the function object
    setattr(f, "__luisa_func__", Lazy[hir.FunctionTemplate](template))

    def wrapper(*args, __lc_ctx__: Optional[TraceContext] = None, **kwargs):
        if not is_jit():
            # In non-JIT context, just call the original function
            assert __lc_ctx__ is None
            return f(*args, **kwargs)
        assert isinstance(__lc_ctx__, TraceContext)

        template = cast(hir.FunctionTemplate, getattr(f, "__luisa_func__").get())

        pytree_args = list([tree_flatten(x, False) for x in args])
        pytree_kwargs: Dict[str, FlattenedTree] = {
            k: tree_flatten(v, False) for k, v in kwargs.items()
        }
        pytree_structure_args = [x.structure() for x in pytree_args]
        pytree_structure_kwargs = {k: v.structure() for k, v in pytree_kwargs.items()}
        instantiated_func = template.instantiate(
            hir.FunctionTemplateArgs(
                args=pytree_structure_args, kwargs=pytree_structure_kwargs
            )
        )
        func_tracer = current_func()

    # Copy over important attributes from the original function
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    wrapper.__annotations__ = f.__annotations__

    return cast(F, wrapper)
