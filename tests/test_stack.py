import pytest
from pack.ng_stack import Layer, Stack


@pytest.fixture
def d0(request):
    return {"a": {"b": "c", "d": 1}, "e": [
        2, 3, "f"], "g": "h", "i": None}


@pytest.fixture
def stack(request, d0):
    st = Stack()
    l0 = Layer(d0)
    st.push(l0)
    return st


@pytest.fixture
def l1(request):
    return Layer({"a": {"j": "k"}})


@pytest.fixture
def l2(request):
    return Layer({"-a": None})


@pytest.fixture
def l3(request):
    return Layer({"e-": ["f"]})


def test_override(stack, l1, d0):
    result = d0
    result["a"] = {"j": "k"}
    stack.push(l1)
    assert stack.as_dict == result


def test_deleteproperty(stack, l2, d0):
    result = d0
    del result["a"]
    stack.push(l2)
    assert stack.as_dict() == result


def test_deleteitem():
    result = d0
    result["e"].remove("f")
    st.push(l3)
    assert st.as_dict == result
