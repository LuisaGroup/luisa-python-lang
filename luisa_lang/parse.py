import ast
import os
from types import FunctionType, ModuleType
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union, overload
import typing
import luisa_lang
from luisa_lang.lang_builtins import comptime
import luisa_lang.math_types
from luisa_lang.utils import get_typevar_constrains_and_bounds, unwrap
import luisa_lang.hir as hir
import sys
from copy import copy
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
from luisa_lang.hir import get_dsl_type, ComptimeValue
import luisa_lang.classinfo as classinfo


def _implicit_typevar_name(v: str) -> str:
    return f"T#{v}"


def is_valid_comptime_value_in_dsl_code(value: Any) -> bool:
    if isinstance(value, (int, float, bool)):
        return True
    if isinstance(value, ModuleType):
        return True
    if get_dsl_type(type(value)) is not None:
        return True
    return False


class TypeParser:
    ctx_name: str
    globalns: Dict[str, Any]
    self_type: Optional[Type]
    type_var_ns: Dict[typing.TypeVar, hir.Type | ComptimeValue]
    generic_params: List[hir.GenericParameter]
    generic_param_to_type_var: Dict[hir.GenericParameter, typing.TypeVar]
    implicit_type_params: Dict[str, hir.Type]

    def __init__(self,  ctx_name: str, globalns: Dict[str, Any],  type_var_ns: Dict[typing.TypeVar, hir.Type | ComptimeValue], self_type: Optional[Type] = None) -> None:
        self.globalns = globalns
        self.self_type = self_type
        self.type_var_ns = type_var_ns
        self.ctx_name = ctx_name
        self.generic_params = []
        self.generic_param_to_type_var = {}

    def parse_type(self, ty: classinfo.VarType) -> Optional[hir.Type]:
        match ty:
            case classinfo.GenericInstance():
                raise NotImplementedError()
            case classinfo.TypeVar():
                # print(f'{ty} @ {id(ty)} {ty.__name__} in {self.type_var_ns}? : {ty in self.type_var_ns}')
                if ty in self.type_var_ns:
                    v = self.type_var_ns[ty]
                    if isinstance(v, ComptimeValue):
                        raise RuntimeError(
                            "Type expected but got comptime value")
                    # print(f'{ty} resolved to {v}')
                    return v
                p = hir.GenericParameter(ty.__name__, self.ctx_name)
                pt = hir.SymbolicType(p)
                self.type_var_ns[ty] = pt
                self.generic_params.append(p)
                self.generic_param_to_type_var[p] = ty
                return pt
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


def convert_func_signature(signature: classinfo.MethodType,
                           ctx_name: str,
                           globalns: Dict[str, Any],
                           type_var_ns: Dict[typing.TypeVar, hir.Type | ComptimeValue],
                           implicit_type_params: Dict[str, hir.Type],
                           self_type: Optional[Type],
                           mode: Literal['parse', 'instantiate'] = 'parse'
                           ) -> Tuple[hir.FunctionSignature, TypeParser]:
    """
    implicit_type_params: Tuple[List[Tuple[str,
        classinfo.VarType]], classinfo.VarType]
    """
    type_parser = TypeParser(ctx_name, globalns, type_var_ns, self_type)
    type_parser.implicit_type_params = implicit_type_params
    params: List[Var] = []
    for arg in signature.args:
        param_type = type_parser.parse_type(arg[1])
        semantic = hir.ParameterSemantic.BYVAL
        if arg[0] == "self":
            assert self_type is not None
            param_type = self_type
            semantic = hir.ParameterSemantic.BYREF
        if param_type is not None:
            params.append(
                Var(arg[0], param_type, span=None, semantic=semantic))
        else:
            if mode == 'parse':
                gp = hir.GenericParameter(
                    _implicit_typevar_name(arg[0]), ctx_name)
                implicit_type_params[arg[0]] = hir.SymbolicType(gp)
                type_parser.generic_params.append(gp)
            else:
                assert not isinstance(
                    implicit_type_params[arg[0]], hir.SymbolicType)
            params.append(
                Var(arg[0], implicit_type_params[arg[0]], span=None, semantic=semantic))
    return_type = type_parser.parse_type(signature.return_type)
    if return_type is not None:
        return_type = return_type
    return hir.FunctionSignature(type_parser.generic_params, params, return_type), type_parser


SPECIAL_FUNCTIONS: Set[Callable[..., Any]] = {
    comptime,
    reveal_type,
    range
}

NewVarHint = Literal[False, 'dsl', 'comptime']


class FuncParser:
    name: str
    func: object
    globalns: Dict[str, Any]
    self_type: Optional[Type]
    vars: Dict[str, hir.Var | ComptimeValue]
    func_def: ast.FunctionDef
    parsed_func: hir.Function
    type_var_ns: Dict[typing.TypeVar, hir.Type | ComptimeValue]
    bb_stack: List[hir.BasicBlock]
    type_parser: TypeParser

    def __init__(self, name: str,
                 func: object,
                 signature: hir.FunctionSignature,
                 globalns: Dict[str, Any],
                 type_var_ns: Dict[typing.TypeVar, hir.Type | ComptimeValue],
                 self_type: Optional[Type]) -> None:
        self.type_parser = TypeParser(name, globalns, type_var_ns, self_type)
        self.name = name
        self.func = func
        self.signature = signature
        self.globalns = copy(globalns)
        obj_ast, _obj_file = retrieve_ast_and_filename(func)
        print(ast.dump(obj_ast))
        assert isinstance(obj_ast, ast.Module), f"{obj_ast} is not a module"
        if not isinstance(obj_ast.body[0], ast.FunctionDef):
            raise RuntimeError("Function definition expected.")
        self.func_def = obj_ast.body[0]
        self.vars = {}
        self.parsed_func = hir.Function(name, [], None)
        self.type_var_ns = type_var_ns
        self.bb_stack = []

        self.parsed_func.params = signature.params
        for p in self.parsed_func.params:
            self.vars[p.name] = p
        self.parsed_func.return_type = signature.return_type

    def cur_bb(self) -> hir.BasicBlock:
        return self.bb_stack[-1]

    def parse_type(self, ty: classinfo.VarType) -> Optional[hir.Type]:
        t = self.type_parser.parse_type(ty)
        if t:
            if isinstance(t, hir.SymbolicType):
                raise RuntimeError(f"Type {t} is not resolved")
        return t

    def convert_constexpr(self, value: ComptimeValue, span: Optional[hir.Span] = None) -> Optional[hir.Value]:
        value = value.value
        if isinstance(value, int):
            return hir.Constant(value, type=hir.GenericIntType())
        elif isinstance(value, float):
            return hir.Constant(value, type=hir.GenericFloatType())
        elif isinstance(value, bool):
            return hir.Constant(value, type=hir.BoolType())
        elif isinstance(value, FunctionType):
            dsl_func = get_dsl_func(value)
            if dsl_func is None:
                raise hir.ParsingError(
                    span, f"expected DSL function but got {value}")
            if dsl_func.is_generic:
                return hir.Constant(dsl_func, type=None, span=span)
            else:
                resolved_f = dsl_func.resolve(None)
                assert not isinstance(
                    resolved_f, hir.TemplateMatchingError)
                return hir.Constant(resolved_f, type=hir.FunctionType(resolved_f), span=span)
        elif isinstance(value, type):
            dsl_type = get_dsl_type(value)
            if dsl_type is None:
                raise hir.ParsingError(
                    span, f"expected DSL type but got {value}")
            return hir.Ctor(dsl_type)
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
            return cst
        raise hir.ParsingError(
            const, f"unsupported constant type {type(value)}, wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")

    def convert_any_to_value(self, a: Any, span: hir.Span | None) -> hir.Value | ComptimeValue:
        if not isinstance(a, ComptimeValue):
            a = ComptimeValue(a, None)
        if a.value in SPECIAL_FUNCTIONS:
            return a
        if (converted := self.convert_constexpr(a, span)) is not None:
            return converted
        if is_valid_comptime_value_in_dsl_code(a.value):
            return a
        raise hir.ParsingError(
            span, f"unsupported constant type {type(a.value)}, wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")

    def parse_name(self, name: ast.Name, new_var_hint: NewVarHint) -> hir.Ref | hir.Value | ComptimeValue:
        span = hir.Span.from_ast(name)
        var = self.vars.get(name.id)
        # print(__builtins__)
        # print('range' in __builtins__)
        # assert hasattr(__builtins__, 'range')
        if var is not None:
            return var
        if new_var_hint == 'dsl':
            var = hir.Var(name.id, None, span)
            self.vars[name.id] = var
            return var
        else:
            # look up in global namespace
            if name.id in self.globalns:
                resolved = self.globalns[name.id]
                return self.convert_any_to_value(resolved, span)
            elif name.id in __builtins__: # type: ignore
                resolved = __builtins__[name.id]  # type: ignore
                return self.convert_any_to_value(resolved, span)
            elif new_var_hint == 'comptime':
                self.globalns[name.id] = None
                def update_fn(value: Any) -> None:
                    self.globalns[name.id] = value
                return ComptimeValue(None, update_fn)

        raise hir.ParsingError(name, f"unknown variable {name.id}")

    def try_convert_comptime_value(self,  value: ComptimeValue, span: hir.Span | None = None) -> hir.Value:
        if (cst := self.convert_constexpr(value)) is not None:
            return cst
        raise hir.ParsingError(
            span, f"unsupported constant type {type(value.value)}, wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")

    def get_index_type(self, span: Optional[hir.Span], base: hir.Type, index: hir.Value) -> Optional[hir.Type]:
        if isinstance(base, hir.TupleType):
            if isinstance(index, hir.Constant):
                if not isinstance(index.value, int):
                    raise hir.ParsingError(
                        span, f"expected integer index, got {type(index.value)}: {index.value}")
                if index.value < 0 or index.value >= len(base.elements):
                    raise hir.ParsingError(
                        span, f"index out of range: {index.value} not in [0, {len(base.elements)})")
                return base.elements[index.value]
            else:
                raise hir.ParsingError(
                    span, f"dynamically indexed tuple is not supported")
        else:
            ty = base.member(hir.DynamicIndex())
            return ty

    def parse_access_ref(self, expr: ast.Subscript | ast.Attribute) -> hir.Ref:
        span = hir.Span.from_ast(expr)
        if isinstance(expr, ast.Subscript):
            value = self.parse_ref(expr.value)
            index = self.parse_expr(expr.slice)
            assert isinstance(value, hir.Ref) and isinstance(index, hir.Value)
            index = self.convert_to_value(index, span)
            assert value.type
            index_ty = self.get_index_type(span, value.type, index)
            if index_ty is not None:
                return self.cur_bb().append(hir.IndexRef(value, index, type=index_ty, span=span))
            else:
                # check __getitem__
                if (method := value.type.method("__getitem__")) and method:
                    ret = self.parse_call_impl(
                        span, method, [value, index])
                    if isinstance(ret, hir.TemplateMatchingError):
                        raise hir.TypeInferenceError(
                            expr, f"error calling __getitem__: {ret.message}")
                    return self.cur_bb().append(hir.LocalRef(ret))
                else:
                    raise hir.TypeInferenceError(
                        expr, f"indexing not supported for type {value.type}")
        elif isinstance(expr, ast.Attribute):
            value = self.parse_ref(expr.value)
            assert isinstance(value, hir.Ref)
            attr_name = expr.attr
            assert value.type
            member_ty = value.type.member(attr_name)
            if not member_ty:
                raise hir.ParsingError(
                    expr, f"member {attr_name} not found in type {value.type}")
            return self.cur_bb().append(hir.MemberRef(value, attr_name, type=member_ty, span=span))
        raise NotImplementedError()  # unreachable

    def parse_access(self, expr: ast.Subscript | ast.Attribute) -> hir.Value | ComptimeValue:
        span = hir.Span.from_ast(expr)
        if isinstance(expr, ast.Subscript):
            value = self.parse_expr(expr.value)
            if isinstance(value, ComptimeValue):
                raise hir.ParsingError(
                    expr, "attempt to access comptime value in DSL code; wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")
            assert value.type
            index = self.parse_expr(expr.slice)
            index = self.convert_to_value(index, span)
            index_ty = self.get_index_type(span, value.type, index)
            if index_ty is not None:
                return self.cur_bb().append(hir.Index(value, index, type=index_ty, span=span))
            else:
                # check __getitem__
                if (method := value.type.method("__getitem__")) and method:
                    ret = self.parse_call_impl(
                        span, method, [value, index])
                    if isinstance(ret, hir.TemplateMatchingError):
                        raise hir.TypeInferenceError(
                            expr, f"error calling __getitem__: {ret.message}")
                    return ret
                else:
                    raise hir.TypeInferenceError(
                        expr, f"indexing not supported for type {value.type}")
        elif isinstance(expr, ast.Attribute):
            value = self.parse_expr(expr.value)
            attr_name = expr.attr
            if isinstance(value, ComptimeValue):
                return ComptimeValue(getattr(value.value, attr_name), None)
            assert value.type
            member_ty = value.type.member(attr_name)
            if not member_ty:
                raise hir.ParsingError(
                    expr, f"member {attr_name} not found in type {value.type}")
            return self.cur_bb().append(hir.Member(value, attr_name, type=member_ty, span=span))
        raise NotImplementedError()  # unreachable

    def parse_call_impl(self, span: hir.Span | None, f: hir.FunctionLike | hir.FunctionTemplate, args: List[hir.Value | hir.Ref]) -> hir.Value | hir.TemplateMatchingError:
        if isinstance(f, hir.FunctionTemplate):
            if f.is_generic:
                template_resolve_args: hir.FunctionTemplateResolvingArgs = []
                template_params = f.params
                if len(template_params) != len(args):
                    return hir.TemplateMatchingError(
                        span,
                        f"Expected {len(template_params)} arguments, got {len(args)}")
                for i, (param, arg) in enumerate(zip(template_params, args)):
                    assert arg.type is not None
                    template_resolve_args.append((param, arg.type))
                resolved_f = f.resolve(template_resolve_args)
                if isinstance(resolved_f, hir.TemplateMatchingError):
                    return resolved_f
            else:
                resolved_f = f.resolve(None)
                assert not isinstance(resolved_f, hir.TemplateMatchingError)
        else:
            resolved_f = f
        if isinstance(resolved_f, hir.Function):
            param_tys = []
            for p in resolved_f.params:
                assert p.type, f"Parameter {p.name} has no type"
                param_tys.append(p.type)
            if len(param_tys) != len(args):
                raise hir.TypeInferenceError(
                    span,
                    f"Expected {len(param_tys)} arguments, got {len(args)}"
                )
            for i, (param_ty, arg) in enumerate(zip(param_tys, args)):
                assert arg.type is not None
                if not hir.is_type_compatible_to(arg.type, param_ty):
                    raise hir.TypeInferenceError(
                        span,
                        f"Argument {i} expected {param_ty}, got {arg.type}"
                    )
            assert resolved_f.return_type
            return self.cur_bb().append(hir.Call(resolved_f, args, type=resolved_f.return_type, span=span))
        else:
            args_ty = []
            for arg in args:
                assert arg.type is not None
                args_ty.append(arg.type)
            ty = resolved_f.type_rule.infer(args_ty)
            return self.cur_bb().append(hir.Call(resolved_f, args, type=ty, span=span))
        raise NotImplementedError()  # unreachable

    def handle_special_functions(self, f: Callable[..., Any], expr: ast.Call) -> hir.Value | ComptimeValue:
        if f is comptime:
            if len(expr.args) != 1:
                raise hir.ParsingError(
                    expr, f"when used in expressions, lc.comptime function expects exactly one argument")
            arg = expr.args[0]
            # print(ast.dump(arg))
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                evaled = self.eval_expr(arg.value)
            else:
                evaled = self.eval_expr(arg)
            # print(evaled)
            v = self.convert_any_to_value(evaled, hir.Span.from_ast(expr))
            return v
        elif f is reveal_type:
            if len(expr.args) != 1:
                raise hir.ParsingError(
                    expr, f"lc.reveal_type expects exactly one argument")
            arg = expr.args[0]
            cur_bb = self.cur_bb()
            cur_bb_len = len(cur_bb.nodes)
            value = self.parse_expr(arg)
            assert cur_bb is self.cur_bb()
            del self.cur_bb().nodes[cur_bb_len:]
            unparsed_arg = ast.unparse(arg)
            if isinstance(value, ComptimeValue):
                print(
                    f"Type of {unparsed_arg} is ComptimeValue({type(value.value)})")
            else:
                print(f"Type of {unparsed_arg} is {value.type}")
            return hir.Unit()
        elif f is range:
            def handle_range() -> hir.Value | ComptimeValue:
                if 1 <= len(expr.args) <= 3:
                    args = [self.parse_expr(arg) for arg in expr.args]
                    is_all_comptime = all(
                        isinstance(arg, ComptimeValue) for arg in args)
                    if is_all_comptime:
                        try:
                            comptime_args = cast(List[hir.ComptimeValue], args)
                            return hir.ComptimeValue(range(*[arg.value for arg in comptime_args]), None)
                        except Exception as e:
                            raise hir.ParsingError(
                                expr, f"error evaluating range: {e}") from e
                    else:
                        for i, arg in enumerate(args):
                            if isinstance(arg, ComptimeValue):
                                args[i] = self.try_convert_comptime_value(
                                    arg, hir.Span.from_ast(expr.args[i]))
                        converted_args = cast(List[hir.Value], args)
                        def make_int(i: int) -> hir.Value:
                            return hir.Constant(i, type=hir.GenericIntType())
                        if len(args) == 1:
                            return hir.Range(make_int(0), converted_args[0], make_int(1))
                        elif len(args) == 2:
                            return hir.Range(converted_args[0], converted_args[1], make_int(1))
                        elif len(args) == 3:
                            return hir.Range(converted_args[0], converted_args[1], converted_args[2])
                        else:
                            raise RuntimeError(
                                f"Unsupported number of arguments for range function: {len(args)}")
                else:
                    raise hir.ParsingError(
                        expr, f"range function expects 1 to 3 arguments")
            return handle_range()
        else:
            raise RuntimeError(f"Unsupported special function {f}")

    def parse_call(self, expr: ast.Call) -> hir.Value | ComptimeValue:
        func = self.parse_expr(expr.func)

        if isinstance(func, hir.Ref):
            raise hir.ParsingError(expr, f"function expected")
        elif isinstance(func, ComptimeValue):
            if func.value in SPECIAL_FUNCTIONS:
                return self.handle_special_functions(func.value, expr)
            func = self.try_convert_comptime_value(
                func, hir.Span.from_ast(expr))

        def collect_args() -> List[hir.Value | hir.Ref]:
            args = [self.parse_expr(arg) for arg in expr.args]
            for i, arg in enumerate(args):
                if isinstance(arg, ComptimeValue):
                    args[i] = self.try_convert_comptime_value(
                        arg, hir.Span.from_ast(expr.args[i]))
            return cast(List[hir.Value | hir.Ref], args)

        if isinstance(func, hir.Ctor):
            cls = func.type
            assert cls
            init = cls.method("__init__")
            tmp = self.cur_bb().append(hir.Alloca(cls, span=hir.Span.from_ast(expr)))
            assert init is not None
            call = self.parse_call_impl(
                hir.Span.from_ast(expr), init,  [tmp]+collect_args())
            if isinstance(call, hir.TemplateMatchingError):
                raise hir.ParsingError(expr, call.message)
            assert isinstance(call, hir.Call)
            return self.cur_bb().append(hir.Load(tmp))

        if not isinstance(func, hir.Constant) or not isinstance(func.value, (hir.Function, hir.BuiltinFunction, hir.FunctionTemplate)):
            raise hir.ParsingError(expr, f"function expected")
        func_like = func.value
        ret = self.parse_call_impl(
            hir.Span.from_ast(expr), func_like,  collect_args())
        if isinstance(ret, hir.TemplateMatchingError):
            raise hir.ParsingError(expr, ret.message)
        return ret

    def parse_binop(self, expr: ast.BinOp) -> hir.Value:
        binop_to_op_str: Dict[type, str] = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.FloorDiv: "//",
            ast.Mod: "%",
            ast.Pow: "**",
            ast.LShift: "<<",
            ast.RShift: ">>",
            ast.BitAnd: '&',
            ast.BitOr: '|',
            ast.BitXor: '^',
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",

        }
        op_str = binop_to_op_str[type(expr.op)]
        lhs = self.parse_expr(expr.left)
        if isinstance(lhs, ComptimeValue):
            lhs = self.try_convert_comptime_value(lhs, hir.Span.from_ast(expr))
        if not lhs.type:
            raise hir.ParsingError(
                expr.left, f"unable to infer type of left operand of binary operation {op_str}")
        rhs = self.parse_expr(expr.right)
        if isinstance(rhs, ComptimeValue):
            rhs = self.try_convert_comptime_value(rhs, hir.Span.from_ast(expr))
        if not rhs.type:
            raise hir.ParsingError(
                expr.right, f"unable to infer type of right operand of binary operation {op_str}")
        ops = BINOP_TO_METHOD_NAMES[type(expr.op)]

        def infer_binop(name: str, rname: str) -> hir.Value:
            assert lhs.type and rhs.type
            matching_errors = []
            try:
                if (method := lhs.type.method(name)) and method:
                    ret = self.parse_call_impl(
                        hir.Span.from_ast(expr), method, [lhs, rhs])
                    if isinstance(ret, hir.TemplateMatchingError):
                        matching_errors.append(ret)
                    else:
                        return ret
                if (method := rhs.type.method(rname)) and method:
                    ret = self.parse_call_impl(
                        hir.Span.from_ast(expr), method, [rhs, lhs])
                    if isinstance(ret, hir.TemplateMatchingError):
                        matching_errors.append(ret)
                    else:
                        return ret
                raise hir.ParsingError(
                    expr, f"Operator {op_str} not defined for types {lhs.type} and {rhs.type}")
            except hir.TypeInferenceError as e:
                e.span = hir.Span.from_ast(expr)
                raise e from e
        return infer_binop(ops[0], ops[1])

    def parse_ref(self, expr: ast.expr, new_var_hint: NewVarHint = False) -> hir.Ref | ComptimeValue:
        match expr:
            case ast.Name():
                ret = self.parse_name(expr, new_var_hint)
                if isinstance(ret, (hir.Value, ComptimeValue)):
                    raise hir.ParsingError(
                        expr, f"value cannot be used as reference")
                return ret
            case ast.Subscript() | ast.Attribute():
                return self.parse_access_ref(expr)
            case _:
                raise hir.ParsingError(
                    expr, f"expression {ast.dump(expr)} cannot be parsed as reference")

    # def parse_assignment_targets(self, targets: List[ast.expr], new_var_hint: NewVarHint) -> List[hir.Ref]:
    #     return [self.parse_ref(t,  new_var_hint) for t in targets]

    # def assign(self, targets: List[hir.Ref], values: hir.Value | ComptimeValue) -> None:
    #     pass

    def parse_multi_assignment(self,
                               targets: List[ast.expr],
                               anno_ty_fn: List[Optional[Callable[..., hir.Type | None]]],
                               values: hir.Value | ComptimeValue) -> None:
        if isinstance(values, ComptimeValue):
            parsed_targets = [self.parse_ref(t, 'comptime') for t in targets]

            def do_assign(target: hir.Ref | ComptimeValue, value: ComptimeValue, i: int) -> None:
                span = hir.Span.from_ast(targets[i])
                if isinstance(target, ComptimeValue):
                    target.update(value.value)
                else:
                    self.cur_bb().append(hir.Assign(target,
                                                    self.try_convert_comptime_value(value, span)))
            if len(parsed_targets) > 1:
                if len(parsed_targets) != len(values.value):
                    raise hir.ParsingError(
                        targets[0], f"expected {len(parsed_targets)} values to unpack, got {len(values.value)}")
                for i, t in enumerate(parsed_targets):
                    do_assign(t, values.value[i],
                              i)
            else:
                t = parsed_targets[0]
                do_assign(t, values, 0)
        else:
            parsed_targets = [self.parse_ref(t, 'dsl') for t in targets]
            is_all_dsl = all(
                isinstance(t, hir.Ref) for t in parsed_targets)
            if not is_all_dsl:
                raise hir.ParsingError(
                    targets[0], "DSL value cannot be assigned to comptime variables")
            assert values.type
            ref_targets = cast(List[hir.Ref], parsed_targets)

            def do_unpack(length: int, extract_fn: Callable[[hir.Value, int, ast.expr], hir.Value]) -> None:
                def check(i: int, val_type: hir.Type) -> None:
                    if len(anno_ty_fn) > 0 and (fn := anno_ty_fn[i]) is not None:
                        ty = fn()
                        if ty is None:
                            raise hir.ParsingError(
                                targets[i], f"unable to infer type of target")
                        if ref_targets[i].type is None:
                            ref_targets[i].type = ty
                    tt = ref_targets[i].type
                    if not tt:
                        if val_type.is_concrete():
                            ref_targets[i].type = val_type
                        else:
                            raise hir.TypeInferenceError(
                                targets[i], f"unable to infer type of target, cannot assign with non-concrete type {val_type}")
                    elif not hir.is_type_compatible_to(val_type, tt):
                        raise hir.ParsingError(
                            targets[i], f"expected type {tt}, got {val_type}")

                if len(ref_targets) == 1:
                    assert values.type
                    check(0, values.type)
                    self.cur_bb().append(hir.Assign(
                        ref_targets[0], values))
                elif len(ref_targets) == length:
                    for i, t in enumerate(ref_targets):
                        e = extract_fn(values, i, targets[i])
                        assert e.type
                        check(i, e.type)
                        self.cur_bb().append(hir.Assign(t, e))
                else:
                    if len(ref_targets) > length:
                        raise hir.ParsingError(
                            targets[0], f"too few values to unpack: expected {len(ref_targets)} values, got {length}")
                    else:
                        raise hir.ParsingError(
                            targets[0], f"too many values to unpack: expected {len(ref_targets)} values, got {length}")
            match values.type:
                case hir.VectorType() as vt:
                    comps = 'xyzw'
                    do_unpack(vt.count, lambda values, i, target: self.cur_bb().append(
                        hir.Member(values, comps[i], type=vt.element, span=hir.Span.from_ast(target))))
                case hir.TupleType() as tt:
                    do_unpack(len(tt.elements), lambda values, i, target: self.cur_bb().append(
                        hir.Member(values, f'_{i}', type=tt.elements[i], span=hir.Span.from_ast(target)))
                    )
                case hir.ArrayType() as at:
                    assert isinstance(at.count, int)
                    do_unpack(at.count, lambda values, i, target: self.cur_bb().append(
                        hir.Index(values, hir.Constant(i, type=luisa_lang.typeof(luisa_lang.i32)), type=at.element, span=hir.Span.from_ast(target))))
                case hir.StructType() as st:
                    do_unpack(len(st.fields), lambda values, i, target: self.cur_bb().append(
                        hir.Member(values, st.fields[i][0], type=st.fields[i][1], span=hir.Span.from_ast(target)))
                    )

    def parse_expr(self, expr: ast.expr) -> hir.Value | ComptimeValue:
        match expr:
            case ast.Constant():
                return self.parse_const(expr)
            case ast.Name():
                ret = self.parse_name(expr, False)
                if isinstance(ret, hir.Ref):
                    ret = self.convert_to_value(ret, hir.Span.from_ast(expr))
                return ret
            case ast.Subscript() | ast.Attribute():
                return self.parse_access(expr)
            case ast.BinOp():
                return self.parse_binop(expr)
            case ast.Call():
                return self.parse_call(expr)
            case ast.Tuple():
                elements = [self.parse_expr(e) for e in expr.elts]
                is_all_comptime = all(
                    isinstance(e, ComptimeValue) for e in elements)
                if is_all_comptime:
                    return hir.ComptimeValue(
                        tuple(e.value for e in cast(List[ComptimeValue], elements)), None)
                else:
                    for i, e in enumerate(elements):
                        if isinstance(e, ComptimeValue):
                            elements[i] = self.try_convert_comptime_value(
                                e, hir.Span.from_ast(expr.elts[i]))
                    tt: hir.TupleType = hir.TupleType(
                        [unwrap(e.type) for e in cast(List[hir.Value], elements)])
                    return self.cur_bb().append(hir.AggregateInit(cast(List[hir.Value], elements), tt, span=hir.Span.from_ast(expr)))
            case _:
                raise RuntimeError(f"Unsupported expression: {ast.dump(expr)}")

    def eval_expr(self, tree: str | ast.Expression | ast.expr):  # -> Any:
        if isinstance(tree, ast.expr):
            tree = ast.Expression(tree)
        # print(tree)
        code_object = compile(tree, "<string>", "eval")
        localns = {}
        for name, v in self.vars.items():
            if isinstance(v, ComptimeValue):
                localns[name] = v.value
        return eval(code_object, self.globalns, localns)

    def convert_to_value(self, value: hir.Value | hir.Ref | ComptimeValue, span: Optional[hir.Span] = None) -> hir.Value:
        if isinstance(value, ComptimeValue):
            value = self.try_convert_comptime_value(value, span)
        if isinstance(value, hir.Ref):
            value = hir.Load(value)
            self.cur_bb().append(value)
        return value

    def parse_stmt(self, stmt: ast.stmt) -> None:
        span = hir.Span.from_ast(stmt)
        match stmt:
            case ast.If():
                cond = self.parse_expr(stmt.test)
                pred_bb = self.cur_bb()
                self.bb_stack.pop()
                if isinstance(cond, ComptimeValue):
                    if cond.value:
                        for s in stmt.body:
                            self.parse_stmt(s)
                    elif stmt.orelse:
                        for s in stmt.orelse:
                            self.parse_stmt(s)
                else:
                    merge = hir.BasicBlock(span)
                    self.bb_stack.append(hir.BasicBlock(span))
                    for s in stmt.body:
                        self.parse_stmt(s)
                    body = self.bb_stack.pop()
                    if stmt.orelse:
                        self.bb_stack.append(hir.BasicBlock(span))
                        for s in stmt.orelse:
                            self.parse_stmt(s)
                        orelse = self.bb_stack.pop()
                    else:
                        orelse = None
                    pred_bb.append(hir.If(cond, body, orelse, merge, span))
                    self.bb_stack.append(merge)
            case ast.While():
                pred_bb = self.cur_bb()
                self.bb_stack.pop()
                prepare = hir.BasicBlock(span)
                self.bb_stack.append(prepare)
                cond = self.parse_expr(stmt.test)
                self.bb_stack.pop()
                if isinstance(cond, ComptimeValue):
                    raise hir.ParsingError(
                        stmt, "while loop condition must not be a comptime value")
                body = hir.BasicBlock(span)
                self.bb_stack.append(body)
                for s in stmt.body:
                    self.parse_stmt(s)
                body = self.bb_stack.pop()
                update = hir.BasicBlock(span)
                merge = hir.BasicBlock(span)
                pred_bb.append(
                    hir.Loop(prepare, cond, body, update, merge, span))
                self.bb_stack.append(merge)
            case ast.For():
                iter_val = self.parse_expr(stmt.iter)
                if not isinstance(iter_val, hir.Value) or not isinstance(iter_val, hir.Range):
                    raise hir.ParsingError(
                        stmt, f"for loop iterable must be a range object but found {iter_val}")
                pred_bb = self.cur_bb()
                self.bb_stack.pop()
                loop_var = self.parse_ref(stmt.target, new_var_hint='dsl')
                if not isinstance(loop_var, hir.Ref):
                    raise hir.ParsingError(
                        stmt, "for loop target must be a DSL variable")
                if not loop_var.type:
                    loop_var.type = luisa_lang.typeof(luisa_lang.i32)
                if not isinstance(loop_var.type, hir.IntType):
                    raise hir.ParsingError(
                        stmt, "for loop target must be an integer variable")
                loop_range: hir.Range = iter_val

                prepare = hir.BasicBlock(span)
                self.bb_stack.append(prepare)
                int_lt = loop_var.type.method("__lt__")
                assert int_lt is not None
                cmp_result = self.parse_call_impl(
                    span, int_lt, [loop_var, loop_range.stop])
                assert isinstance(cmp_result, hir.Value)
                assert cmp_result.type == hir.BoolType()
                self.bb_stack.pop()
                body = hir.BasicBlock(span)
                self.bb_stack.append(body)
                for s in stmt.body:
                    self.parse_stmt(s)
                body = self.bb_stack.pop()
                update = hir.BasicBlock(span)
                self.bb_stack.append(update)
                inc =loop_range.step
                int_add = loop_var.type.method("__add__")
                assert int_add is not None
                add = self.parse_call_impl(
                    span, int_add, [loop_var, inc])
                assert isinstance(add, hir.Value)
                self.cur_bb().append(hir.Assign(loop_var, add))
                self.bb_stack.pop()
                merge = hir.BasicBlock(span)
                pred_bb.append(
                    hir.Loop(prepare, cmp_result, body, update, merge, span))
                self.bb_stack.append(merge)
            case ast.Return():
                def check_return_type(ty: hir.Type) -> None:
                    assert self.parsed_func
                    if self.parsed_func.return_type is None:
                        self.parsed_func.return_type = ty
                    else:
                        if not hir.is_type_compatible_to(ty, self.parsed_func.return_type):
                            raise hir.ParsingError(
                                stmt, f"return type mismatch: expected {self.parsed_func.return_type}, got {ty}")
                if stmt.value:
                    value = self.parse_expr(stmt.value)
                    value = self.convert_to_value(value, span)
                    assert value.type is not None
                    check_return_type(value.type)
                    self.cur_bb().append(hir.Return(value))
                else:
                    check_return_type(hir.UnitType())
                    self.cur_bb().append(hir.Return(None))
            case ast.Assign():
                # if len(stmt.targets) != 1:
                #     raise hir.ParsingError(stmt, f"expected single target")
                # target = stmt.targets[0]
                # var = self.parse_ref(target, new_var_hint='dsl')
                # value = self.parse_expr(stmt.value)
                # if isinstance(var, ComptimeValue):
                #     if not isinstance(value, ComptimeValue):
                #         raise hir.ParsingError(
                #             stmt, f"comptime value cannot be assigned with DSL value")
                #     var.update(value.value)
                #     return None
                # value = self.convert_to_value(value, span)
                # assert value.type
                # if var.type:
                #     if not hir.is_type_compatible_to(value.type, var.type):
                #         raise hir.ParsingError(
                #             stmt, f"expected {var.type}, got {value.type}")
                # else:
                #     if not value.type.is_concrete():
                #         raise hir.ParsingError(
                #             stmt, "only concrete type can be assigned, please annotate the variable with type hint")
                #     var.type = value.type
                # self.cur_bb().append(hir.Assign(var, value, span))
                assert len(stmt.targets) == 1
                target = stmt.targets[0]
                if isinstance(target, ast.Tuple):
                    self.parse_multi_assignment(
                        target.elts, [], self.parse_expr(stmt.value))
                else:
                    self.parse_multi_assignment(
                        [target], [], self.parse_expr(stmt.value)
                    )
            case ast.AugAssign():
                method_name = AUG_ASSIGN_TO_METHOD_NAMES[type(stmt.op)]
                var = self.parse_ref(stmt.target)
                value = self.parse_expr(stmt.value)
                if isinstance(var, ComptimeValue):
                    if not isinstance(value, ComptimeValue):
                        raise hir.ParsingError(
                            stmt, f"comptime value cannot be assigned with DSL value")
                    comptime_method = getattr(var.value, method_name, None)
                    if comptime_method is None:
                        raise hir.ParsingError(
                            stmt, f"comptime value of type {type(var.value)} does not support {method_name}")
                    var.update(comptime_method(value.value))
                    return None
                value = self.convert_to_value(value, span)
                assert value.type
                assert var.type
                method = var.type.method(method_name)
                if not method:
                    raise hir.ParsingError(
                        stmt, f"operator {method_name} not defined for type {var.type}")
                ret = self.parse_call_impl(
                    span, method, [var, value])
                if isinstance(ret, hir.TemplateMatchingError):
                    raise hir.ParsingError(stmt, ret.message)

            case ast.AnnAssign():
                def parse_anno_ty() -> hir.Type:
                    type_annotation = self.eval_expr(stmt.annotation)
                    type_hint = classinfo.parse_type_hint(type_annotation)
                    ty = self.parse_type(type_hint)
                    assert ty
                    return ty

                if stmt.value:
                    self.parse_multi_assignment(
                        [stmt.target], [parse_anno_ty], self.parse_expr(stmt.value))
                    # value = self.parse_expr(stmt.value)
                    # if isinstance(value, ComptimeValue):
                    #     var = self.parse_ref(
                    #         stmt.target, new_var_hint='comptime')
                    # else:
                    #     var = self.parse_ref(stmt.target, new_var_hint='dsl')
                    # if isinstance(var, ComptimeValue):
                    #     if isinstance(value, ComptimeValue):
                    #         try:
                    #             var.update(value.value)
                    #         except Exception as e:
                    #             raise hir.ParsingError(
                    #                 stmt, f"error updating comptime value: {e}") from e
                    #         return
                    #     else:
                    #         raise hir.ParsingError(
                    #             stmt, f"comptime value cannot be assigned with DSL value")
                    # else:
                    #     if isinstance(value, ComptimeValue):
                    #         value = self.try_convert_comptime_value(
                    #             value, span)
                    #     assert value.type
                    #     anno_ty = parse_anno_ty()
                    #     if not var.type:
                    #         var.type = value.type
                    #     if not var.type.is_concrete():
                    #         raise hir.ParsingError(
                    #             stmt, "only concrete type can be assigned, please annotate the variable with concrete types")
                    #     if not hir.is_type_compatible_to(value.type, anno_ty):
                    #         raise hir.ParsingError(
                    #             stmt, f"expected {anno_ty}, got {value.type}")
                    #     if not value.type.is_concrete():
                    #         value.type = var.type
                    #     self.cur_bb().append(hir.Assign(var, value, span))
                else:
                    var = self.parse_ref(stmt.target, new_var_hint='dsl')
                    anno_ty = parse_anno_ty()
                    assert isinstance(var, hir.Var)
                    if not var.type:
                        var.type = anno_ty
                    else:
                        if not hir.is_type_compatible_to(var.type, anno_ty):
                            raise hir.ParsingError(
                                stmt, f"expected {anno_ty}, got {var.type}")
            case ast.Expr():
                self.parse_expr(stmt.value)
            case ast.Pass():
                return
            case _:
                raise RuntimeError(f"Unsupported statement: {ast.dump(stmt)}")

    def parse_body(self):
        assert self.parsed_func is not None
        body = self.func_def.body
        entry = hir.BasicBlock(hir.Span.from_ast(self.func_def))
        self.bb_stack.append(entry)
        for stmt in body:
            self.parse_stmt(stmt)
        assert len(self.bb_stack) == 1
        self.parsed_func.body = entry
        self.parsed_func.locals = list(
            [x for x in self.vars.values() if isinstance(x, hir.Var)])
        if not self.parsed_func.return_type:
            self.parsed_func.return_type = hir.UnitType()
        self.parsed_func.complete = True
        return self.parsed_func


UNARY_OP_TO_METHOD_NAMES: Dict[type, str] = {
    ast.UAdd: "__pos__",
    ast.USub: "__neg__",
    ast.Not: "__not__",
    ast.Invert: "__invert__",
}

AUG_ASSIGN_TO_METHOD_NAMES: Dict[type, str] = {
    ast.Add: "__iadd__",
    ast.Sub: "__isub__",
    ast.Mult: "__imul__",
    ast.Div: "__idiv__",
    ast.FloorDiv: "__ifloordiv__",
    ast.Mod: "__imod__",
    ast.Pow: "__ipow__",
    ast.LShift: "__ilshift__",
    ast.RShift: "__irshift__",
    ast.BitAnd: "__iand__",
    ast.BitOr: "__ior__",
    ast.BitXor: "__ixor__",
}

BINOP_TO_METHOD_NAMES: Dict[type, List[str]] = {
    ast.Add: ["__add__", "__radd__"],
    ast.Sub: ["__sub__", "__rsub__"],
    ast.Mult: ["__mul__", "__rmul__"],
    ast.Div: ["__truediv__", "__rtruediv__"],
    ast.FloorDiv: ["__floordiv__", "__rfloordiv__"],
    ast.Mod: ["__mod__", "__rmod__"],
    ast.Eq: ["__eq__", "__eq__"],
    ast.NotEq: ["__ne__", "__ne__"],
    ast.Lt: ["__lt__", "__gt__"],
    ast.LtE: ["__le__", "__ge__"],
    ast.Gt: ["__gt__", "__lt__"],
    ast.GtE: ["__ge__", "__le__"],
    ast.BitAnd: ["__and__", "__rand__"],
    ast.BitOr: ["__or__", "__ror__"],
    ast.BitXor: ["__xor__", "__rxor__"],
    ast.LShift: ["__lshift__", "__rlshift__"],
    ast.RShift: ["__rshift__", "__rrshift__"],
    ast.Pow: ["__pow__", "__rpow__"],
}

__all__ = ["convert_func_signature", "FuncParser"]
