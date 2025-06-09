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

    def compile(
        self,
        f: Callable[..., Any],
        example_inputs: Tuple[Any, ...] | None = None,
        example_kwargs: Dict[str, Any] | None = None,
        name: str | None = None,
    ) -> None:
        """
        Compile a function/kernel with example inputs.
        """
        try:
            globalns = classinfo._get_func_globalns(f)
            with KernelTracer(globalns) as tracer:
                example_inputs = example_inputs or ()
                example_kwargs = example_kwargs or {}
                trace_ctx = TraceContext(True)
                assert is_jit()
                f(*example_inputs, **example_kwargs, __lc_ctx__=trace_ctx)
                func_ir = trace_ctx.top_level_func
                assert func_ir is not None
            self.codegen.gen_function(func_ir)

        except Exception as e:
            print(f"Error during function execution: {e}")
            traceback.print_exc()
            return
    
    def output(self) -> str:
        """
        Get the output code from the code generator.
        """
        return self.codegen.finalize_code()


__all__ = ["Compiler"]
