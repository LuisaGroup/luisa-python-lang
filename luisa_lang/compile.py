from typing import *

from luisa_lang import classinfo

from luisa_lang.lang_runtime import JitVar, KernelTracer, TraceContext, is_jit
from luisa_lang.codegen.cpp import CppCodeGen
import traceback


class Compiler:
    codegen: CppCodeGen

    def __init__(self, target: Literal["cpp", "custom"]):
        match target:
            case "cpp":
                self.codegen = CppCodeGen()
            case "custom":
                raise NotImplementedError()

    def compile_with_inputs(
        self,
        f: Callable[..., Any],
        fn_args: Tuple[Any, ...] | None = None,
        fn_kwargs: Dict[str, Any] | None = None,
        name: str | None = None,
    ) -> None:
        """
        Compile a function/kernel with example inputs.
        """
        try:
            globalns = classinfo._get_func_globalns(f)
            with KernelTracer(globalns) as tracer:
                fn_args = fn_args or ()
                fn_kwargs = fn_kwargs or {}
                trace_ctx = TraceContext()
                assert is_jit()
                f(*fn_args, **fn_kwargs, __lc_ctx__=trace_ctx)

        except Exception as e:
            print(f"Error during function execution: {e}")
            traceback.print_exc()
            return


__all__ = ["Compiler"]
