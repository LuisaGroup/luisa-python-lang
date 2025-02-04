import ast
import os
from types import FunctionType, ModuleType
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union, overload
import typing
import luisa_lang
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


ParsingMode = Literal['parse', 'instantiate']


def _make_type_parameteric_type() -> hir.ParametricType:
    t = hir.GenericParameter('T', '__builtins__.type')
    st = hir.SymbolicType(t)

    def mono_func(args: List[hir.Type]) -> hir.Type:
        assert len(args) == 1
        return hir.TypeConstructorType(args[0])
    type_type = hir.ParametricType([t], hir.TypeConstructorType(st), mono_func)
    return type_type


TYPE_PARAMETERIC_TYPE: hir.ParametricType = _make_type_parameteric_type()



class TypeParser:
    ctx_name: str
    globalns: Dict[str, Any]
    self_type: Optional[Type]
    type_var_ns: Dict[typing.TypeVar, hir.Type]
    generic_params: List[hir.GenericParameter]
    generic_param_to_type_var: Dict[hir.GenericParameter, typing.TypeVar]
    implicit_type_params: Dict[str, hir.Type]
    mode: ParsingMode

    def __init__(self,  ctx_name: str, globalns: Dict[str, Any],  type_var_ns: Dict[typing.TypeVar, hir.Type], self_type: Optional[Type], mode: ParsingMode) -> None:
        self.globalns = globalns
        self.self_type = self_type
        self.type_var_ns = type_var_ns
        self.ctx_name = ctx_name
        self.generic_params = []
        self.generic_param_to_type_var = {}
        self.mode = mode

    def parse_type(self, ty: classinfo.VarType) -> Optional[hir.Type]:
        ty_or_bound = self.parse_type_ext(ty)
        if ty_or_bound is None:
            return None
        if isinstance(ty_or_bound, hir.TypeBound):
            raise RuntimeError("Expected a specific type but got generic type")
        return ty_or_bound

    def parse_type_ext(self, ty: classinfo.VarType) -> Optional[Union[hir.Type, hir.TypeBound]]:
        match ty:
            case classinfo.GenericInstance():
                origin = ty.origin
                if origin is type:
                    def handle_type_t():
                        assert len(
                            ty.args) == 1, "type[T] expects exactly one type argument"
                        arg = self.parse_type(ty.args[0])
                        assert arg is not None
                        if self.mode == 'instantiate':
                            return TYPE_PARAMETERIC_TYPE.instantiate([arg])
                        return hir.BoundType(TYPE_PARAMETERIC_TYPE, [arg], None)
                    return handle_type_t()
                ir_ty = self.parse_type(origin)
                if not ir_ty:
                    raise RuntimeError(
                        f"Type {origin} is not a valid DSL type")
                if not isinstance(ir_ty, hir.ParametricType):
                    raise RuntimeError(
                        f"Type {origin} is not a parametric type but is supplied with type arguments")
                if len(ir_ty.params) != len(ty.args):
                    raise RuntimeError(
                        f"Type {origin} expects {len(ir_ty.params)} type arguments, got {len(ty.args)}")
                type_args = [self.parse_type(arg) for arg in ty.args]
                if any(arg is None for arg in type_args):
                    raise RuntimeError(
                        "failed to parse type arguments")
                if self.mode == 'instantiate':
                    instantiated = ir_ty.instantiate(type_args)
                else:
                    instantiated = None
                return hir.BoundType(ir_ty, cast(List[hir.Type | hir.SymbolicConstant], type_args), instantiated)
            case classinfo.TypeVar():
                # print(f'{ty} @ {id(ty)} {ty.__name__} in {self.type_var_ns}? : {ty in self.type_var_ns}')
                if ty in self.type_var_ns:
                    v = self.type_var_ns[ty]
                    return v
                p = hir.GenericParameter(ty.__name__, self.ctx_name)
                pt = hir.SymbolicType(p)
                self.type_var_ns[ty] = pt
                self.generic_params.append(p)
                self.generic_param_to_type_var[p] = ty
                return pt
            case classinfo.UnionType():
                # raise RuntimeError("UnionType is not supported")
                variants = [self.parse_type(v) for v in ty.types]
                if any(v is None for v in variants):
                    raise RuntimeError("failed to parse union type variants")
                return hir.UnionBound([hir.SubtypeBound(cast(hir.Type, v), True) for v in variants])
            case classinfo.SelfType():
                assert self.self_type is not None
                return self.self_type
            case classinfo.AnnotatedType():
                def do_anno() -> hir.Type:
                    origin = self.parse_type(ty.origin)
                    assert origin is not None
                    annotations = ty.annotations
                    if annotations == [SPECIAL_FUNCTIONS_DICT['byref']]:
                        return hir.RefType(origin)
                    raise RuntimeError(
                        f"Unsupported annotations {annotations}")
                return do_anno()
            case classinfo.AnyType():
                return hir.AnyBound()
            case type():
                if ty is type:
                    raise RuntimeError(
                        f"type alone cannot be used as a dsl type hint. use type[T] instead")
                dsl_type = get_dsl_type(ty)
                assert dsl_type is not None, f"Type {
                    ty} is not a valid DSL type"
                return dsl_type
            case classinfo.LiteralType():
                return hir.LiteralType(ty.value)
            case _:
                raise RuntimeError(f"Unsupported type {ty}")


def convert_func_signature(signature: classinfo.MethodType,
                           ctx_name: str,
                           props: hir.FuncProperties,
                           globalns: Dict[str, Any],
                           type_var_ns: Dict[typing.TypeVar, hir.Type],
                           implicit_type_params: Dict[str, hir.Type],
                           self_type: Optional[Type],
                           mode: ParsingMode = 'parse'
                           ) -> Tuple[hir.FunctionSignature, TypeParser]:
    """
    implicit_type_params: Tuple[List[Tuple[str,
        classinfo.VarType]], classinfo.VarType]
    """
    type_parser = TypeParser(ctx_name, globalns, type_var_ns, self_type, mode)
    type_parser.implicit_type_params = implicit_type_params
    params: List[Var] = []
    for arg in signature.args:
        param_type = type_parser.parse_type_ext(arg[1])
        semantic = hir.ParameterSemantic.BYVAL
        if arg[0] == "self":
            assert self_type is not None
            assert isinstance(
                arg[1], classinfo.SelfType), "self is implicit set to Ref[Self], so do not provide type hint!"
            if self_type.is_addressable():
                param_type = hir.RefType(self_type)
                semantic = hir.ParameterSemantic.BYREF
            else:
                param_type = self_type

        if param_type is None:
            raise RuntimeError(
                f"Unable to parse type of parameter {arg[0]}: {arg[1]}")
        if isinstance(param_type, hir.RefType):
            semantic = hir.ParameterSemantic.BYREF
        if isinstance(param_type, hir.Type):
            params.append(
                Var(arg[0], param_type.remove_ref(), span=None, semantic=semantic))
        else:
            if mode == 'parse':
                gp = hir.GenericParameter(
                    _implicit_typevar_name(arg[0]), ctx_name, bound=param_type)
                implicit_type_params[arg[0]] = hir.SymbolicType(gp)
                type_parser.generic_params.append(gp)
            else:
                assert not isinstance(
                    implicit_type_params[arg[0]], hir.SymbolicType)
            params.append(
                Var(arg[0], implicit_type_params[arg[0]], span=None, semantic=semantic))
    return_type = type_parser.parse_type_ext(signature.return_type)
    assert return_type is not None, f"failed to parse return type {
        signature.return_type}"
    if isinstance(return_type, hir.AnyBound):
        return_type = None
    elif isinstance(return_type, hir.TypeBound):
        raise NotImplementedError()

    return hir.FunctionSignature(type_parser.generic_params, params, return_type), type_parser


SPECIAL_FUNCTIONS_DICT: Dict[str, Callable[..., Any]] = {}
SPECIAL_FUNCTIONS: Set[Callable[..., Any]] = set()


def _add_special_function(name: str, f: Callable[..., Any]) -> None:
    SPECIAL_FUNCTIONS_DICT[name] = f
    SPECIAL_FUNCTIONS.add(f)

_add_special_function('print', print)

NewVarHint = Literal[False, 'dsl', 'comptime']


def _friendly_error_message_for_unrecognized_type(ty: Any) -> str:
    if ty is range:
        return 'expected builtin function range, use lc.range instead'
    return f"expected DSL type but got {ty}"

class FuncStack:
    st: List['FuncParser']

    def __init__(self) -> None:
        self.st = []

    def push(self, f: 'FuncParser') -> None:
        self.st.append(f)

    def pop(self) -> 'FuncParser':
        return self.st.pop()
    
    def dump_stack(self)->str:
        trace = []
        for i, f in enumerate(reversed(self.st)):
            span = hir.Span.from_ast(f.func_def)
            trace.append(f"{i}: {f.name} at {span if span else 'unknown'}")
        return '\n'.join(trace)


FUNC_STACK = FuncStack()

class FuncParser:

    name: str
    func: object
    globalns: Dict[str, Any]
    self_type: Optional[Type]
    vars: Dict[str, hir.Var | ComptimeValue]
    func_def: ast.FunctionDef
    parsed_func: hir.Function
    type_var_ns: Dict[typing.TypeVar, hir.Type]
    bb_stack: List[hir.BasicBlock]
    type_parser: TypeParser
    break_and_continues: List[hir.Break | hir.Continue] | None

    def __init__(self, name: str,
                 func: object,
                 signature: hir.FunctionSignature,
                 globalns: Dict[str, Any],
                 type_var_ns: Dict[typing.TypeVar, hir.Type],
                 self_type: Optional[Type]
                 ) -> None:
        self.type_parser = TypeParser(
            name, globalns, type_var_ns, self_type, 'instantiate')
        self.name = name
        self.func = func
        self.signature = signature
        self.globalns = copy(globalns)
        obj_ast, _obj_file = retrieve_ast_and_filename(func)
        # print(ast.dump(obj_ast))
        assert isinstance(obj_ast, ast.Module), f"{obj_ast} is not a module"
        if not isinstance(obj_ast.body[0], ast.FunctionDef):
            raise RuntimeError("Function definition expected.")
        self.func_def = obj_ast.body[0]
        self.vars = {}
        self.parsed_func = hir.Function(
            name, [], None, self_type is not None)
        self.type_var_ns = type_var_ns
        self.bb_stack = []
        self.break_and_continues = None
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

    def convert_constexpr(self, comptime_val: ComptimeValue, span: Optional[hir.Span] = None) -> Optional[hir.Value]:
        value = comptime_val.value
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
                return hir.FunctionValue(hir.FunctionType(dsl_func, None), span=span)
            else:
                resolved_f = dsl_func.resolve(None)
                assert not isinstance(
                    resolved_f, hir.TemplateMatchingError)
                return hir.FunctionValue(hir.FunctionType(resolved_f, None), span=span)
                # return hir.FunctionValue(resolved_f, None, span)
        else:
            try:
                hint = classinfo.parse_type_hint(value)
                parsed_type = self.parse_type(hint)
                if parsed_type is not None:
                    return hir.TypeValue(parsed_type)
            except classinfo.TypeParsingError:
                pass
        # elif isinstance(value, type):
        #     # TODO: refactor this to use parse_type...
        #     dsl_type = get_dsl_type(value)
        #     if dsl_type is None:
        #         raise hir.ParsingError(
        #             span, _friendly_error_message_for_unrecognized_type(value))

        #     return hir.TypeValue(dsl_type)
        # elif isinstance(value, (typing.TypeAliasType, typing.Annotated)):
        #     type_hint = classinfo.parse_type_hint(value)
        #     parsed_type = self.parse_type(type_hint)
        #     if parsed_type is not None:
        #         return hir.TypeValue(parsed_type)
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
        if isinstance(a, typing.TypeVar):
            if a in self.type_var_ns:
                v = self.type_var_ns[a]
                if isinstance(v, hir.Type):
                    return hir.TypeValue(v)
                return self.convert_any_to_value(v, span)

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

    def parse_name(self, name: ast.Name, new_var_hint: NewVarHint) -> hir.Var | hir.Value | ComptimeValue:
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
            elif name.id in __builtins__:  # type: ignore
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

    def parse_access(self, expr: ast.Subscript | ast.Attribute) -> hir.Value | hir.TypeValue | hir.FunctionValue | ComptimeValue:
        span = hir.Span.from_ast(expr)
        if isinstance(expr, ast.Subscript):
            value = self.parse_expr(expr.value)
            if isinstance(value, ComptimeValue):
                raise hir.ParsingError(
                    expr, "attempt to access comptime value in DSL code; wrap it in lc.comptime(...) if you intead to use it as a compile-time expression")
            if isinstance(value, hir.TypeValue):
                type_args: List[hir.Type] = []

                def parse_type_arg(expr: ast.expr) -> hir.Type:
                    type_annotation = self.eval_expr(expr)
                    type_hint = classinfo.parse_type_hint(type_annotation)
                    ty = self.parse_type(type_hint)
                    assert ty
                    return ty

                match expr.slice:
                    case ast.Tuple():
                        for e in expr.slice.elts:
                            type_args.append(parse_type_arg(e))
                    case _:
                        type_args.append(parse_type_arg(expr.slice))

                # print(f"Type args: {type_args}")
                assert isinstance(value.type, hir.TypeConstructorType)
                if isinstance(value.type.inner, hir.ParametricType):
                    return hir.TypeValue(
                        hir.BoundType(value.type.inner, type_args, value.type.inner.instantiate(type_args)))
                elif isinstance(value.type.inner, hir.RefType):
                    if len(type_args) != 1:
                        raise hir.ParsingError(
                            span, f"expected exactly one type argument for Ref, got {len(type_args)}")
                    return hir.TypeValue(hir.RefType(type_args[0]))
            index = self.parse_expr(expr.slice)
            index = self.convert_to_value(index, span)
            assert value.type
            index_ty = self.get_index_type(span, value.type, index)
            if index_ty is not None:
                return self.cur_bb().append(hir.Index(value, index, type=index_ty, span=span))
            else:
                # check __getitem__
                if (method := value.type.method("__getitem__")) and method:
                    try:
                        ret = self.parse_call_impl(
                            span, method, [value, index])
                    except hir.InlineError as e:
                        raise hir.InlineError(
                            expr, f"error during inlining of __getitem__, note that __getitem__ must be inlineable {e}") from e
                    if isinstance(ret, hir.TemplateMatchingError):
                        raise hir.TypeInferenceError(
                            expr, f"error calling __getitem__: {ret.message}")
                    if not isinstance(ret.type, hir.RefType):
                        raise hir.ParsingError(
                            span, f"__getitem__ must return a reference")
                    return ret
                else:
                    raise hir.TypeInferenceError(
                        expr, f"indexing not supported for type {value.type}")
        elif isinstance(expr, ast.Attribute):
            def do(expr: ast.Attribute):
                value: hir.Value | hir.ComptimeValue = self.parse_expr(
                    expr.value)
                if isinstance(value, ComptimeValue):
                    if isinstance(value.value, ModuleType):
                        resolved = getattr(value.value, expr.attr)
                        return ComptimeValue(resolved, None)
                    value = self.try_convert_comptime_value(value, span)
                if isinstance(value.type, hir.RefType):
                    attr_name = expr.attr
                    assert value.type
                    member_ty = value.type.member(attr_name)
                    if not member_ty:
                        raise hir.ParsingError(
                            expr, f"member {attr_name} not found in type {value.type}")
                    if isinstance(member_ty, hir.FunctionType):
                        if not isinstance(value, hir.TypeValue):
                            member_ty.bound_object = value
                        return hir.FunctionValue(member_ty)
                    return self.cur_bb().append(hir.Member(value, attr_name, type=member_ty, span=span))
                elif isinstance(value, hir.TypeValue):
                    member_ty = value.inner_type().member(expr.attr)
                    if not member_ty:
                        raise hir.ParsingError(
                            expr, f"member {expr.attr} not found in type {value.inner_type()}")
                    if isinstance(member_ty, hir.FunctionType):
                        return hir.FunctionValue(member_ty)
                    else:
                        raise hir.ParsingError(
                            expr, f"member {expr.attr} is not a function")
                elif isinstance(value, hir.FunctionValue):
                    raise hir.ParsingError(
                        expr, "function value has no attributes")
                else:
                    raise hir.ParsingError(
                        expr, f"unsupported value type {type(value)}")
            return do(expr)
        # print(type(expr), type(expr) is ast.Attribute)
        raise NotImplementedError()  # unreachable

    def parse_call_impl(self, span: hir.Span | None, f: hir.Function | hir.FunctionTemplate, args: List[hir.Value]) -> hir.Value | hir.TemplateMatchingError:

        if isinstance(f, hir.FunctionTemplate):
            if f.is_generic:
                template_resolve_args: hir.FunctionTemplateResolvingArgs = []
                template_params = f.params
                if len(template_params) != len(args):
                    return hir.TemplateMatchingError(
                        span,
                        f"Expected {len(template_params)} arguments, got {len(args)}")
                for i, (param, arg) in enumerate(zip(template_params, args)):
                    if arg.type is None:
                        raise hir.TypeInferenceError(
                            span, f"failed to infer type of argument {i}")
                    template_resolve_args.append((param, arg.type))
                try:
                    resolved_f = f.resolve(template_resolve_args)
                    if isinstance(resolved_f, hir.TemplateMatchingError):
                        return resolved_f
                except hir.TypeInferenceError as e:
                    if e.span is None:
                        e.span = span
                    raise e from e
            else:
                resolved_f = f.resolve(None)
                assert not isinstance(resolved_f, hir.TemplateMatchingError)
        else:
            resolved_f = f
        assert resolved_f.return_type
        expect_ref = isinstance(resolved_f.return_type, hir.RefType)
        inline = expect_ref or resolved_f.inline_hint == 'always'
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
            if not hir.is_type_compatible_to(arg.type.remove_ref(), param_ty):
                raise hir.TypeInferenceError(
                    span,
                    f"Argument {i} expected {param_ty}, got {arg.type}"
                )
            if resolved_f.params[i].semantic == hir.ParameterSemantic.BYREF:
                if not isinstance(arg.type, hir.RefType):
                    tmp = self.cur_bb().append(hir.Alloca(param_ty))
                    self.cur_bb().append(hir.Assign(tmp, arg))
                    args[i] = tmp
                else:
                    args[i] = arg
            else:
                if isinstance(arg.type, hir.RefType):
                    args[i] = self.cur_bb().append(hir.Load(arg))

        if not inline:
            return self.cur_bb().append(hir.Call(resolved_f, args, type=resolved_f.return_type, span=span))
        else:
            return hir.FunctionInliner.inline(resolved_f, args, self.cur_bb(), span)

    def handle_intrinsic(self, expr: ast.Call) -> hir.Value:
        intrinsic_name = expr.args[0]
        if not isinstance(intrinsic_name, ast.Constant) or not isinstance(intrinsic_name.value, str):
            raise hir.ParsingError(
                expr, "intrinsic function expects a string literal as its first argument")
        args: List[hir.Value | hir.ComptimeValue] = []
        for a in expr.args[1:]:
            if isinstance(a, ast.Call) and isinstance(a.func, ast.Name) and a.func.id == 'byref':
                r = self.parse_expr(a.args[0])
                if isinstance(r, hir.Value) and isinstance(r.type, hir.RefType):
                    args.append(r)
                else:
                    raise hir.ParsingError(
                        a, "expected reference but got value")
            else:
                args.append(self.parse_expr(a))
        ret_type = args[0]
        if isinstance(ret_type, ComptimeValue):
            ret_type = self.try_convert_comptime_value(
                ret_type, hir.Span.from_ast(expr.args[0]))
        if not isinstance(ret_type, hir.TypeValue):
            raise hir.ParsingError(
                expr, f"intrinsic function expects a type as its second argument but found {ret_type}")
        if any([not isinstance(arg, hir.Value) for arg in args[1:]]):
            raise hir.ParsingError(
                expr, "intrinsic function expects DSL values as its arguments")
        intrinsic_ret_type = ret_type.inner_type()
        return self.cur_bb().append(
            hir.Intrinsic(intrinsic_name.value, cast(List[hir.Value], args[1:]),
                          intrinsic_ret_type, hir.Span.from_ast(expr)))
        # if is_ref:
        #     return self.cur_bb().append(
        #         hir.IntrinsicRef(intrinsic_name.value, cast(List[hir.Value | hir.Ref], args[1:]),
        #                          ret_type.inner_type(), hir.Span.from_ast(expr)))
        # else:
        #     return self.cur_bb().append(
        #         hir.Intrinsic(intrinsic_name.value, cast(List[hir.Value | hir.Ref], args[1:]),
        #                       ret_type.inner_type(), hir.Span.from_ast(expr)))

    def handle_special_functions(self, f: Callable[..., Any], expr: ast.Call) -> hir.Value | ComptimeValue:
        if f is print:
            args = [self.parse_string_element(a) for a in expr.args]
            self.cur_bb().append(hir.Print(args, hir.Span.from_ast(expr)))
            return hir.Unit()
        elif f is SPECIAL_FUNCTIONS_DICT['intrinsic']:
            intrin_ret = self.handle_intrinsic(expr)
            assert isinstance(intrin_ret, hir.Value)
            return intrin_ret
        # elif f is SPECIAL_FUNCTIONS_DICT['sizeof']:
        #     if len(expr.args) != 1:
        #         raise hir.ParsingError(
        #             expr, f"lc.sizeof function expects exactly one argument")
        #     arg_ty = self.parse_expr(expr.args[0])
        #     if isinstance(arg_ty, ComptimeValue):
        #         arg_ty = self.try_convert_comptime_value(
        #             arg_ty, hir.Span.from_ast(expr.args[0]))
        #     if not isinstance(arg_ty, hir.TypeValue):
        #         raise hir.ParsingError(
        #             expr.args[0], f"expected type but got {arg_ty}")
        #     return self.cur_bb().append(hir.Constant(arg_ty.inner_type().size(), type=hir.GlobalContext().get().types[''], span=hir.Span.from_ast(expr)))
        elif f is SPECIAL_FUNCTIONS_DICT['cast'] or f is SPECIAL_FUNCTIONS_DICT['bitcast']:
            def do() -> hir.Intrinsic:
                if len(expr.args) != 2:
                    raise hir.ParsingError(
                        expr, f"lc.cast function expects exactly two arguments")

                target_ty = self.parse_expr(expr.args[0])
                value = self.parse_expr(expr.args[1])
                if isinstance(target_ty, ComptimeValue):
                    target_ty = self.try_convert_comptime_value(
                        target_ty, hir.Span.from_ast(expr.args[0]))
                if not isinstance(target_ty, hir.TypeValue):
                    raise hir.ParsingError(
                        expr.args[0], f"expected type but got {target_ty}")
                if isinstance(value, ComptimeValue):
                    value = self.try_convert_comptime_value(
                        value, hir.Span.from_ast(expr.args[1]))
                if f is SPECIAL_FUNCTIONS_DICT['cast']:
                    intrinsic_name = "cast"
                else:
                    intrinsic_name = "bitcast"
                return self.cur_bb().append(hir.Intrinsic(intrinsic_name, [value], target_ty.inner_type(), hir.Span.from_ast(expr)))
            return do()
        elif f is SPECIAL_FUNCTIONS_DICT['comptime']:
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
        elif f is SPECIAL_FUNCTIONS_DICT['range']:
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
                        # TODO: check type consistency
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

    # def parse_call_ref(self, expr: ast.Call) -> hir.Ref:
    #     func: hir.Ref | ComptimeValue | hir.TypeValue | hir.Value = self.parse_ref(
    #         expr.func)
    #     if isinstance(func, ComptimeValue):
    #         if func.value is not SPECIAL_FUNCTIONS_DICT['intrinsic']:
    #             raise hir.ParsingError(
    #                 expr, f"expected intrinsic function but got {func}")
    #         intrin_ref = self.handle_intrinsic(expr, True)
    #         assert isinstance(intrin_ref, hir.Ref)
    #         return intrin_ref

    #     span = hir.Span.from_ast(expr)
    #     if not isinstance(func, hir.FunctionValue):
    #         raise hir.ParsingError(
    #             expr, f"expected function but got {func}")
    #     raise NotImplementedError()

    def parse_call(self, expr: ast.Call) -> hir.Value | ComptimeValue:
        func: ComptimeValue | hir.TypeValue | hir.Value = self.parse_expr(
            expr.func)
        span = hir.Span.from_ast(expr)

        if isinstance(func, ComptimeValue):
            if func.value in SPECIAL_FUNCTIONS:
                return self.handle_special_functions(func.value, expr)
            func = self.try_convert_comptime_value(
                func, hir.Span.from_ast(expr))

        def collect_args() -> List[hir.Value]:
            args = [self.parse_expr(arg) for arg in expr.args]
            for i, arg in enumerate(args):
                if isinstance(arg, ComptimeValue):
                    args[i] = self.try_convert_comptime_value(
                        arg, hir.Span.from_ast(expr.args[i]))
            return cast(List[hir.Value], args)

        if isinstance(func.type, hir.TypeConstructorType):
            # TypeConstructorType is unique for each type
            # so if any value has this type, it must be referring to the same underlying type
            # even if it comes from a very complex expression, it's still fine
            cls = func.type.inner
            assert cls
            if isinstance(cls, hir.ParametricType):
                raise hir.ParsingError(
                    span, f"please provide type arguments for {cls.body}")

            init = cls.method("__init__")
            tmp = self.cur_bb().append(hir.Alloca(cls, span))
            if init is None:
                raise hir.ParsingError(
                    span, f"__init__ method not found for type {cls}")
            call = self.parse_call_impl(
                span, init,  [tmp]+collect_args())
            if isinstance(call, hir.TemplateMatchingError):
                raise hir.ParsingError(expr, call.message)
            return self.cur_bb().append(hir.Load(tmp))
        assert func.type
        if isinstance(func.type, hir.FunctionType):
            func_like = func.type.func_like
            bound_object = func.type.bound_object
            if bound_object is not None:
                ret = self.parse_call_impl(
                    span, func_like,  cast(List[hir.Value], [bound_object]) + collect_args())
            else:
                ret = self.parse_call_impl(
                    span, func_like,  collect_args())
            if isinstance(ret, hir.TemplateMatchingError):
                raise hir.ParsingError(expr, ret.message)
            return ret
        else:
            # check if __call__ is defined
            if (method := func.type.method("__call__")) and method:
                ret = self.parse_call_impl(
                    span, method, cast(List[hir.Value], [func]) + collect_args())
                if isinstance(ret, hir.TemplateMatchingError):
                    raise hir.ParsingError(expr, ret.message)
                return ret
            else:
                raise hir.ParsingError(
                    expr, f"function call not supported for type {func.type}")

    def parse_binop(self, expr: ast.BinOp | ast.Compare) -> hir.Value:
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
        op: ast.AST
        if isinstance(expr, ast.Compare):
            if len(expr.ops) != 1:
                raise hir.ParsingError(
                    expr, "only one comparison operator is allowed")
            op = expr.ops[0]
            left = expr.left
            right = expr.comparators[0]
        else:
            op = expr.op
            left = expr.left
            right = expr.right
        op_str = binop_to_op_str[type(op)]
        lhs = self.parse_expr(left)
        if isinstance(lhs, ComptimeValue):
            lhs = self.try_convert_comptime_value(lhs, hir.Span.from_ast(expr))
        if not lhs.type:
            raise hir.ParsingError(
                left, f"unable to infer type of left operand of binary operation {op_str}")
        rhs = self.parse_expr(right)
        if isinstance(rhs, ComptimeValue):
            rhs = self.try_convert_comptime_value(rhs, hir.Span.from_ast(expr))
        if not rhs.type:
            raise hir.ParsingError(
                right, f"unable to infer type of right operand of binary operation {op_str}")
        ops = BINOP_TO_METHOD_NAMES[type(op)]

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

    def parse_multi_assignment(self,
                               targets: List[ast.expr],
                               anno_ty_fn: List[Optional[Callable[..., hir.Type | None]]],
                               values: hir.Value | ComptimeValue) -> None:
        if isinstance(values, ComptimeValue):
            parsed_targets = [self.parse_expr(t, 'comptime') for t in targets]
            for i in range(len(parsed_targets)):
                if isinstance(parsed_targets[i], hir.TypeValue):
                    raise hir.ParsingError(
                        targets[i], "types cannot be reassigned")

            def do_assign(target: hir.Value | ComptimeValue, value: ComptimeValue, i: int) -> None:
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
                    assert isinstance(t, (hir.Value, ComptimeValue))
                    do_assign(t, values.value[i],
                              i)
            else:
                t = parsed_targets[0]
                assert isinstance(t, (hir.Value, ComptimeValue))
                do_assign(t, values, 0)
        else:
            parsed_targets = [self.parse_expr(t, 'dsl') for t in targets]
            is_all_dsl = all(
                isinstance(t, hir.Value) for t in parsed_targets)
            if not is_all_dsl:
                raise hir.ParsingError(
                    targets[0], "DSL value cannot be assigned to comptime variables")
            assert values.type
            ref_targets = cast(List[hir.Value], parsed_targets)

            def do_unpack(length: int, extract_fn: Callable[[hir.Value, int, ast.expr], hir.Value]) -> None:
                def check(i: int, val_type: hir.Type) -> None:
                    def do_update_type_for_var(t: hir.Value, ty: hir.Type):
                        if t.type is None:
                            assert isinstance(t, hir.VarRef)
                            t.var.type = ty
                            t.type = hir.RefType(ty)
                    if len(anno_ty_fn) > 0 and (fn := anno_ty_fn[i]) is not None:
                        ty = fn()
                        if ty is None:
                            raise hir.ParsingError(
                                targets[i], f"unable to infer type of target")
                        do_update_type_for_var(ref_targets[i], ty)
                    tt = ref_targets[i].type
                    if isinstance(val_type, hir.FunctionType) and val_type.bound_object is not None:
                        raise hir.TypeInferenceError(
                            targets[i], f"bounded method cannot be assigned to variable")
                    if not tt:
                        if val_type.is_concrete():
                            do_update_type_for_var(ref_targets[i], val_type)
                        else:
                            raise hir.TypeInferenceError(
                                targets[i], f"unable to infer type of target, cannot assign with non-concrete type {val_type}")
                    elif not hir.is_type_compatible_to(val_type, tt.remove_ref()):
                        raise hir.ParsingError(
                            targets[i], f"expected type {tt.remove_ref()}, got {val_type}")

                if len(ref_targets) == 1:
                    assert values.type
                    check(0, values.type)
                    if not isinstance(values.type, (hir.FunctionType, hir.TypeConstructorType)):
                        self.cur_bb().append(hir.Assign(
                            ref_targets[0], self.convert_to_value(values)))
                elif len(ref_targets) == length:
                    for i, t in enumerate(ref_targets):
                        e = extract_fn(values, i, targets[i])
                        assert e.type
                        check(i, e.type)
                        if not isinstance(e.type, (hir.FunctionType, hir.TypeConstructorType)):
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
                case _:
                    if len(ref_targets) == 1:
                        do_unpack(1, lambda values, i, target: exit(-1))
                    else:
                        raise hir.ParsingError(
                            targets[0], f"unsupported type for unpacking: {values.type}")

    def parse_unary(self, expr: ast.UnaryOp) -> hir.Value:
        op = expr.op
        if type(op) not in UNARY_OP_TO_METHOD_NAMES:
            raise hir.ParsingError(
                expr, f"unsupported unary operator {type(op)}")
        op_str = UNARY_OP_TO_METHOD_NAMES[type(op)]
        operand = self.parse_expr(expr.operand)
        if isinstance(operand, ComptimeValue):
            operand = self.try_convert_comptime_value(
                operand, hir.Span.from_ast(expr))
        if not operand.type:
            raise hir.ParsingError(
                expr.operand, f"unable to infer type of operand of unary operation {op_str}")
        method_name = UNARY_OP_TO_METHOD_NAMES[type(op)]
        if (method := operand.type.method(method_name)) and method:
            ret = self.parse_call_impl(
                hir.Span.from_ast(expr), method, [operand])
            if isinstance(ret, hir.TemplateMatchingError):
                raise hir.ParsingError(expr, ret.message)
            return ret
        else:
            raise hir.ParsingError(
                expr, f"operator {type(op)} not defined for type {operand.type}")

    def parse_expr(self, expr: ast.expr, new_var_hint: NewVarHint = False) -> hir.Value | ComptimeValue:
        span = hir.Span.from_ast(expr)
        match expr:
            case ast.Constant():
                return self.parse_const(expr)
            case ast.Name():
                ret = self.parse_name(expr, new_var_hint)
                if isinstance(ret, (hir.Value, hir.Var)):
                    if isinstance(ret.type, hir.TypeConstructorType):
                        assert isinstance(ret, hir.TypeValue)
                        return ret
                    if isinstance(ret.type, hir.FunctionType):
                        return hir.FunctionValue(ret.type, span)
                    # raise hir.ParsingError(
                    #     expr, f"{type(ret)} cannot be used as reference")
                    if isinstance(ret, hir.Var):
                        if ret.type is not None and not ret.type.is_addressable():
                            return self.cur_bb().append(hir.VarValue(ret, span))
                        return self.cur_bb().append(hir.VarRef(ret, span))
                    assert ret.type
                    return ret
                return ret
            case ast.Subscript() | ast.Attribute():
                return self.parse_access(expr)
            case ast.BinOp() | ast.Compare():
                return self.parse_binop(expr)
            case ast.UnaryOp():
                return self.parse_unary(expr)
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
                    return self.cur_bb().append(hir.AggregateInit(cast(List[hir.Value], elements), tt, span))
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

    def convert_to_value(self, value: hir.Value | ComptimeValue, span: Optional[hir.Span] = None) -> hir.Value:
        if isinstance(value, ComptimeValue):
            value = self.try_convert_comptime_value(value, span)
        if value.is_ref():
            value = hir.Load(value)
            self.cur_bb().append(value)
        return value

    def parse_string_element(self, v: ast.expr) -> Union[str, hir.Value]:
        span = hir.Span.from_ast(v)
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            return v.value
        return self.convert_to_value(self.parse_expr(v), span)
    
    def parse_strings(self, expr: ast.JoinedStr | ast.Constant) -> List[Union[str, hir.Value]]:
        match expr:
            case ast.JoinedStr():
                return [self.parse_string_element(v) for v in expr.values]
            case ast.Constant():
                return [self.parse_string_element(expr)]

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
                old_break_and_continues = self.break_and_continues
                self.break_and_continues = []
                for s in stmt.body:
                    self.parse_stmt(s)
                break_and_continues = self.break_and_continues
                self.break_and_continues = old_break_and_continues
                body = self.bb_stack.pop()
                update = hir.BasicBlock(span)
                merge = hir.BasicBlock(span)
                loop_node = hir.Loop(prepare, cond, body, update, merge, span)
                pred_bb.append(loop_node)
                for bc in break_and_continues:
                    bc.target = loop_node
                self.bb_stack.append(merge)
            case ast.For():
                iter_val = self.parse_expr(stmt.iter)
                if not isinstance(iter_val, hir.Value) or not isinstance(iter_val, hir.Range):
                    raise hir.ParsingError(
                        stmt, f"for loop iterable must be a range object but found {iter_val}")
                loop_range: hir.Range = iter_val
                pred_bb = self.cur_bb()
                self.bb_stack.pop()
                loop_var = self.parse_expr(stmt.target, new_var_hint='dsl')
                if not isinstance(loop_var, hir.Value):
                    raise hir.ParsingError(
                        stmt, "for loop target must be a DSL variable")
                if not loop_var.type:
                    loop_ty = loop_range.value_type()
                    if not isinstance(loop_ty, hir.GenericIntType):
                        loop_var.type = loop_ty
                    else:
                        loop_var.type = luisa_lang.typeof(luisa_lang.i32)
                if not isinstance(loop_var.type, hir.IntType):
                    raise hir.ParsingError(
                        stmt, "for loop target must be an integer variable")

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
                old_break_and_continues = self.break_and_continues
                self.break_and_continues = []
                for s in stmt.body:
                    self.parse_stmt(s)
                body = self.bb_stack.pop()
                break_and_continues = self.break_and_continues
                self.break_and_continues = old_break_and_continues
                update = hir.BasicBlock(span)
                self.bb_stack.append(update)
                inc = loop_range.step
                int_add = loop_var.type.method("__add__")
                assert int_add is not None
                add = self.parse_call_impl(
                    span, int_add, [loop_var, inc])
                assert isinstance(add, hir.Value)
                self.cur_bb().append(hir.Assign(loop_var, add))
                self.bb_stack.pop()
                merge = hir.BasicBlock(span)
                loop_node = hir.Loop(prepare, cmp_result,
                                     body, update, merge, span)
                pred_bb.append(loop_node)
                for bc in break_and_continues:
                    bc.target = loop_node
                self.bb_stack.append(merge)
            case ast.Break():
                if self.break_and_continues is None:
                    raise hir.ParsingError(
                        stmt, "break statement must be inside a loop")
                self.cur_bb().append(hir.Break(None, span))
            case ast.Continue():
                if self.break_and_continues is None:
                    raise hir.ParsingError(
                        stmt, "continue statement must be inside a loop")
                self.cur_bb().append(hir.Continue(None, span))
            case ast.Return():
                def check_return_type(ty: hir.Type) -> None:
                    assert self.parsed_func
                    if self.parsed_func.return_type is None:
                        self.parsed_func.return_type = ty
                    else:
                        if not hir.is_type_compatible_to(ty, self.parsed_func.return_type):
                            raise hir.ParsingError(
                                stmt, f"return type mismatch: expected {self.parsed_func.return_type}, got {ty}")
                if isinstance(self.signature.return_type, hir.RefType):
                    def do():
                        if not stmt.value:
                            raise hir.ParsingError(
                                stmt, "if a function is returning local references, the return value must be provided")
                        value = self.parse_expr(stmt.value)
                        if not isinstance(value, hir.Value) or not value.is_ref():
                            raise hir.ParsingError(
                                stmt, "invalid return target")
                        assert value.type
                        check_return_type(value.type)
                        self.cur_bb().append(hir.Return(value))
                    do()
                else:
                    def do():
                        if stmt.value:
                            value = self.parse_expr(stmt.value)
                            value = self.convert_to_value(value, span)
                            assert value.type is not None
                            check_return_type(value.type)
                            self.cur_bb().append(hir.Return(value))
                        else:
                            check_return_type(hir.UnitType())
                            self.cur_bb().append(hir.Return(None))
                    do()
            case ast.Assign():
                assert len(stmt.targets) == 1
                target = stmt.targets[0]
                if isinstance(target, ast.Tuple):
                    self.parse_multi_assignment(
                        target.elts, [], self.parse_expr(stmt.value))
                else:
                    self.parse_multi_assignment(
                        [target], [], self.parse_expr(stmt.value)
                    )
            case ast.Assert():
                def handle_assert():
                    test = self.parse_expr(stmt.test)
                    msg = stmt.msg
                    if isinstance(test, ComptimeValue):
                        if msg:
                            evaled_msg = f'assertion failed for comptime value {
                                self.eval_expr(msg)}'
                        else:
                            evaled_msg = f'assertion failed for comptime value {
                                test.value}'
                        assert test.value, evaled_msg
                    else:
                        sep_msg: List[Union[hir.Value, str]] = []
                        if msg is not None:
                            if not isinstance(msg, (ast.Constant, ast.JoinedStr)):
                                raise hir.ParsingError(
                                    stmt, "assert message must be a string literal")
                            sep_msg = self.parse_strings(msg)
                        self.cur_bb().append(hir.Assert(test, sep_msg, span))
                handle_assert()
            case ast.AugAssign():
                method_name = AUG_ASSIGN_TO_METHOD_NAMES[type(stmt.op)]
                var = self.parse_expr(stmt.target)
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
                else:
                    var = self.parse_expr(stmt.target, new_var_hint='dsl')
                    anno_ty = parse_anno_ty()
                    assert isinstance(var, hir.Var)
                    if not var.type:
                        var.type = anno_ty
                    else:
                        if not hir.is_type_compatible_to(var.type, anno_ty):
                            raise hir.ParsingError(
                                stmt, f"expected {anno_ty}, got {var.type}")
            case ast.Expr():
                # ignore comments
                if isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                    return
                self.parse_expr(stmt.value)
            case ast.Pass():
                return
            case _:
                raise RuntimeError(f"Unsupported statement: {ast.dump(stmt)}")

    def parse_body(self):
        FUNC_STACK.push(self)
        try:
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
            assert FUNC_STACK.pop() is self
            return self.parsed_func
        except hir.SpannedError as e:
            if e.stack_trace is None:
                e.stack_trace =  FUNC_STACK.dump_stack()
            raise e from e



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
