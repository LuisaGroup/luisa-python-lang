from typing import *

from lang_runtime import KernelTracer
from luisa_lang.codegen.cpp import CppCodeGen


class Compiler:
    codegen: CppCodeGen

    def __init__(self, target: Literal['cpp', 'custom']):
        match target:
            case 'cpp':
                self.codegen = CppCodeGen()
            case 'custom':
                raise NotImplementedError()

    def compile_function_with_inputs(self, f: Callable[..., Any],
                                     fn_args: Tuple[Any, ...] | None = None,
                                     fn_kwargs: Dict[str, Any] | None = None,
                                     name: str | None = None) -> None:
        """
        Compile an function with example inputs.
        """
        try:
            with KernelTracer() as tracer:
                fn_args = fn_args or ()
                fn_kwargs = fn_kwargs or {}
                f(*fn_args, **fn_kwargs)
            
        except Exception as e:
            print(f"Error during function execution: {e}")
            return


__all__ = [
    'Compiler'
]
