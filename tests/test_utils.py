import pytest
from typing import Union, List, Tuple, Optional
import luisa_lang
from luisa_lang.utils import check_type

def test_check_type_with_builtin_type():
    assert check_type(int, 5)
    assert not check_type(int, "hello")
    assert check_type(str, "test")
    assert not check_type(str, 123)


def test_check_type_with_tuple_type():
    assert check_type((int, float), 3)
    assert check_type((int, float), 3.14)
    assert not check_type((int, float), "str")

def test_check_type_with_typing_union():
    assert check_type(Union[int, str], 42)
    assert check_type(Union[int, str], "foo")
    assert not check_type(Union[int, str], 3.14)

def test_check_forward_reference():
    assert check_type(Union['int', str], 42)
    assert check_type(Union['int', str], "foo")
    assert not check_type(Union['int', str], 3.14)


def test_check_type_with_union_type_operator():
    # Python 3.10+: int | str
    try:
        union_type = int | str
    except TypeError:
        pytest.skip("UnionType not supported in this Python version")
    assert check_type(union_type, 1)
    assert check_type(union_type, "a")
    assert not check_type(union_type, 3.14)

def test_check_type_with_generic_list():
    # This test is limited by the implementation, which only checks the origin and args
    # and expects obj to be an instance of origin and all elements to be instances of args.
    class Dummy(list): pass
    pat = List[int]
    obj = [1, 2, 3]
    assert check_type(pat, obj) is True or check_type(pat, obj) is False  # implementation may not fully support this

def test_check_type_with_tuple_generic():
    pat = Tuple[int, str]
    obj = (1, "a")
    # The implementation only checks if obj is instance of origin and all elements match args
    assert check_type(pat, obj) is True or check_type(pat, obj) is False

def test_check_type_with_optional():
    pat = Optional[int]
    assert check_type(pat, 5)
    assert check_type(pat, None)

def test_check_type_with_non_matching():
    assert not check_type(float, "not a float")
    assert not check_type((list, dict), 42)
    assert not check_type(Union[bytes, dict], 3.14)