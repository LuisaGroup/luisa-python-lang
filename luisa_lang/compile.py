from typing import *

from lang_runtime import JitVar, KernelTracer
from luisa_lang.codegen.cpp import CppCodeGen
import traceback


class Compiler:
    codegen: CppCodeGen

    def __init__(self, target: Literal['cpp', 'custom']):
        match target:
            case 'cpp':
                self.codegen = CppCodeGen()
            case 'custom':
                raise NotImplementedError()

    def compile_with_inputs(self, f: Callable[..., Any],
                            fn_args: Tuple[Any, ...] | None = None,
                            fn_kwargs: Dict[str, Any] | None = None,
                            name: str | None = None) -> None:
        """
        Compile a function/kernel with example inputs.
        """
        try:
            with KernelTracer() as tracer:
                fn_args = fn_args or ()
                fn_kwargs = fn_kwargs or {}
                # for a in fn_args:
                #     if isinstance(a, JitVar):
                #         assert not a.is_symbolic()
                #         a._init_symbolic()
                # for _, v in fn_kwargs.items():
                #     if isinstance(v, JitVar):
                #         assert not v.is_symbolic()
                #         v._init_symbolic()

                f(*fn_args, **fn_kwargs)
                # for a in fn_args:
                #     if isinstance(a, JitVar):
                #         a._destroy_symbolic()
                # for _, v in fn_kwargs.items():
                #     if isinstance(v, JitVar):
                #         v._destroy_symbolic()

        except Exception as e:
            print(f"Error during function execution: {e}")
            traceback.print_exc()
            return


__all__ = [
    'Compiler'
]
