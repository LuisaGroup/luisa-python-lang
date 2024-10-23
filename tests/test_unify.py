import luisa_lang
import luisa_lang.lang as lc
from luisa_lang.hir import *


def test_unify_simple():
    generic_params = {
        'T': GenericParameter('T', ''),
        'U': GenericParameter('U', '')
    }
    t = SymbolicType(generic_params['T'])
    u = SymbolicType(generic_params['U'])
    vt = VectorType(t, 4)
    ut = VectorType(u, 4)
    f32 = lc.typeof(lc.f32)
    i32 = lc.typeof(lc.i32)
    float4 = VectorType(f32, 4)
    int4 = VectorType(i32, 4)
    mapping = match_template_args(
        [('x', t), ('y', f32)], [f32, f32])
    assert mapping == {generic_params['T']: f32}

    mapping = match_template_args(
        [('x', f32), ('y', t)], [f32, f32])
    assert mapping == {generic_params['T']: f32}

    mapping = match_template_args(
        [('x', u), ('y', t)], [f32, f32])
    assert mapping == {generic_params['T']: f32, generic_params['U']: f32}

    mapping = match_template_args(
        [('x', vt), ('y', t)], [float4, f32])
    assert mapping == {generic_params['T']: f32}

    mapping = match_template_args(
        [('y', t), ('x', vt)], [f32, float4])
    assert mapping == {generic_params['T']: f32}

    mapping = match_template_args(
        [('x', vt), ('y', ut)], [int4, float4])
    assert mapping == {generic_params['T']: i32, generic_params['U']: f32}
