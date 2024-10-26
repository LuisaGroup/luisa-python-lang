import ast
import os
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload
import typing
import luisa_lang
from luisa_lang.lang import type_of_opt
from luisa_lang.utils import get_typevar_constrains_and_bounds, report_error
import luisa_lang.hir as hir
import sys
from luisa_lang.utils import retrieve_ast_and_filename
from luisa_lang.hir import (
    Type,
    BoundType,
    ParametricType,
    Function,
    Var,
    get_dsl_func
)
from typing import NoReturn, cast, Set, reveal_type
from enum import Enum
import inspect
from luisa_lang.hir.defs import get_dsl_type
import luisa_lang.classinfo as classinfo


class ConstexprValue:
    value: Any

    def __init__(self, value: Any) -> None:
        self.value = value


def _any_typevar_name(i: int) -> str:
    return f"Any#{i}"


class FuncParser:
    name: str
    func: object
    globalns: Dict[str, Any]
    self_type: Optional[Type]
    vars: Dict[str, hir.Var | ConstexprValue]
    func_def: ast.FunctionDef
    parsed_func: Optional[hir.Function]
    type_var_ns: Dict[typing.TypeVar, hir.Type]

    def __init__(self, name: str,
                 func: object,
                 signature: classinfo.MethodType,
                 globalns: Dict[str, Any],
                 type_var_ns: Dict[typing.TypeVar, hir.Type],
                 any_param_types: List[hir.Type]) -> None:
        self.name = name
        self.func = func
        self.signature = signature
        self.globalns = globalns
        obj_ast, _obj_file = retrieve_ast_and_filename(func)
        print(ast.dump(obj_ast))
        assert isinstance(obj_ast, ast.Module), f"{obj_ast} is not a module"
        if not isinstance(obj_ast.body[0], ast.FunctionDef):
            raise RuntimeError("Function definition expected.")
        self.func_def = obj_ast.body[0]
        self.name_eval_cache = {}
        self.vars = {}
        self.parsed_func = None
        self.type_var_ns = type_var_ns

        params = []
        any_param_cnt = 0
        for arg in self.signature.args:
            param_type = self.parse_type(arg)
            if param_type is not None:
                params.append(param_type)
            else:
                params.append(any_param_types[any_param_cnt])
                any_param_cnt += 1
        return_type = self.parse_type(signature.return_type)

    def parse_type(self, ty: classinfo.VarType) -> Optional[hir.Type]:
        match ty:
            case classinfo.GenericInstance():
                raise NotImplementedError()
            case classinfo.TypeVar():
                return self.type_var_ns[ty]
            case classinfo.UnionType():
                raise RuntimeError("UnionType is not supported")
            case classinfo.SelfType():
                assert self.self_type is not None
                return self.self_type
            case classinfo.AnyType():
                return None
            case type():
                dsl_type = get_dsl_type(ty)
                assert dsl_type is not None
                return dsl_type

    def convert_constexpr(self, value: ConstexprValue) -> Optional[hir.Value]:
        value = value.value
        if isinstance(value, int):
            return hir.Constant(value, type=hir.GenericIntType())
        if isinstance(value, float):
            return hir.Constant(value, type=hir.GenericFloatType())
        if isinstance(value, bool):
            return hir.Constant(value, type=hir.BoolType())
        return None

    def parse_const(self, const: ast.Constant) -> hir.Value:
        span = hir.Span.from_ast(const)
        value = const.value
        if isinstance(value, (int, float, bool)):
            cst = hir.Constant(value, type=None, span=span)
            match value:
                case int():
                    cst.type = hir.GenericIntType()
                case float():
                    cst.type = hir.GenericFloatType()
                case bool():
                    cst.type = hir.BoolType()
        report_error(
            const, f"unsupported constant type {type(value)}, wrap it in lc.constexpr(...) if you intead to use it as a constexpr")

    # def parse_name(self, name: ast.Name, is_ref: bool, maybe_new_var: bool) -> hir.Value:
    #     span = hir.Span.from_ast(name)
    #     var = self.vars.get(name.id)
    #     if var is not None:
    #         if is_ref:  # if it's a reference
    #             return var
    #         return hir.Load(var)
    #     if maybe_new_var:
    #         var = hir.Var(name.id, None, span)
    #         self.vars[name.id] = var
    #         return var
    #     report_error(name, f"unknown variable {name.id}")

    # def parse_access(self, expr: ast.Subscript | ast.Attribute, is_ref: bool) -> ValueLike | RefLike:
    #     span = hir.Span.from_ast(expr)

    #     def access(value: ValueLike | RefLike,
    #                index: ValueLike,
    #                get_fn: Callable[[Any, Any], Any],
    #                set_fn: Callable[[Any, Any, Any], None]) -> ValueLike | RefLike:
    #         if is_ref:
    #             assert isinstance(value, RefLike)
    #             if isinstance(value, hir.Ref):
    #                 if isinstance(index, ConstexprValue):
    #                     converted_index = self.convert_constexpr(index)
    #                     if converted_index is None:
    #                         report_error(
    #                             expr, "failed to convert constexpr index to DSL value; Note that only literals are supported here")
    #                     return hir.Index(value, converted_index, span)
    #                 return hir.Index(value, index, span)
    #             else:  # ConstexprRef
    #                 if not isinstance(index, ConstexprValue):
    #                     report_error(
    #                         expr, "index must be constexpr when accessing a constexpr")

    #                 def update_func(v):
    #                     set_fn(value.value, index.value, v)
    #                 return ConstexprRef(get_fn(value.value, index.value), update_func)
    #         else:
    #             assert isinstance(value, ValueLike)
    #             if isinstance(value, hir.Value):
    #                 if isinstance(index, ConstexprValue):
    #                     converted_index = self.convert_constexpr(index)
    #                     if converted_index is None:
    #                         report_error(
    #                             expr, "failed to convert constexpr index to DSL value; Note that only literals are supported here")
    #                     return hir.Index(value, converted_index, span)
    #                 else:
    #                     return hir.Index(value, index, span)
    #             else:  # ConstexprValue
    #                 if not isinstance(index, ConstexprValue):
    #                     report_error(
    #                         expr, "index must be constexpr when accessing a constexpr")
    #                 return ConstexprValue(get_fn(value.value, index.value))
    #     if isinstance(expr, ast.Subscript):
    #         value = self.parse_expr(expr.value, is_ref)
    #         index = self.parse_expr(expr.slice, False)
    #         assert isinstance(index, ValueLike)

    #         def get_fn(value, index):
    #             return value[index]

    #         def set_fn(value, index, v):
    #             value[index] = v
    #         return access(value, index, get_fn, set_fn)
    #     elif isinstance(expr, ast.Attribute):
    #         value = self.parse_expr(expr.value, is_ref)
    #         attr_name = expr.attr

    #         def get_fn(value, attr_name):
    #             return getattr(value, attr_name)

    #         def set_fn(value, attr_name, v):
    #             setattr(value, attr_name, v)
    #         return access(value, ConstexprValue(attr_name), get_fn, set_fn)

    #     raise NotImplementedError()  # unreachable

    # def parse_call(self, call: ast.Call) -> ValueLike:
    #     func = self.parse_expr(call.func, False)
    #     args = [self.parse_expr(arg, False) for arg in call.args]
    #     raise NotImplementedError()

    def parse_name(self, name: ast.Name, is_ref: bool, maybe_new_var: bool) -> hir.Ref | hir.Value:
        span = hir.Span.from_ast(name)
        var = self.vars.get(name.id)
        if var is not None:
            if isinstance(var, hir.Var):
                if is_ref:
                    return hir.Load(var)
                return var
            report_error
        if maybe_new_var:
            var = hir.Var(name.id, None, span)
            self.vars[name.id] = var
            if is_ref:
                return hir.Load(var)
            return var
        else:
            # look up in global namespace
            if name in self.globalns:
                resolved = self.globalns[name.id]
                if callable(resolved):
                    dsl_func = get_dsl_func(resolved)
                    if dsl_func is None:
                        report_error(name, f"expected DSL function")
                    if dsl_func.is_generic:
                        return hir.ValueRef(hir.Constant(dsl_func, type=None, span=span))
                    else:
                        resolved_f = dsl_func.resolve(None)
                        return hir.ValueRef(hir.Constant(resolved_f, type=hir.FunctionType(resolved_f), span=span))
                elif isinstance(resolved, hir.Type):
                    pass
        report_error(name, f"unknown variable {name.id}")

    def parse_access_ref(self, expr: ast.Subscript | ast.Attribute, is_ref: bool) -> hir.Ref | hir.Value:
        span = hir.Span.from_ast(expr)
        if isinstance(expr, ast.Subscript):
            value = self.parse_expr(expr.value)
            index = self.parse_expr(expr.slice)
            return hir.Index(value, index, span)
        elif isinstance(expr, ast.Attribute):
            value = self.parse_expr(expr.value)
            attr_name = expr.attr
            return hir.Member(value, attr_name, span)
        raise NotImplementedError()  # unreachable

    def parse_call(self, expr: ast.Call) -> hir.Value:
        func = self.parse_expr(expr.func)
        args = [self.parse_expr(arg) for arg in expr.args]
        return hir.Call(func, args)

    def parse_expr(self, expr: ast.expr) -> hir.Value:
        match expr:
            case ast.Constant():
                return self.parse_const(expr)
            case ast.Name():
                ret = self.parse_name(expr, True, False)
                assert isinstance(ret, hir.Value)
                return ret
            case ast.Subscript() | ast.Attribute():
                ret = self.parse_access_ref(expr, True)
                assert isinstance(ret, hir.Value)
                return ret
            case ast.Call():
                return self.parse_call(expr)
            case _:
                raise RuntimeError(f"Unsupported expression: {ast.dump(expr)}")

    def parse_stmt(self, stmt: ast.stmt) -> Optional[hir.Stmt]:
        match stmt:
            case ast.Return():
                value = self.parse_expr(stmt.value, False)
                return hir.Return(value)
            case _:
                raise RuntimeError(f"Unsupported statement: {ast.dump(stmt)}")

    def parse_body(self):
        body = self.func_def.body
        parsed_body = [self.parse_stmt(stmt) for stmt in body]
