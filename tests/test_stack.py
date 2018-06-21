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
    return Layer({"-!a": None})


@pytest.fixture
def l3(request):
    return Layer({"e!-": ["f"]})


@pytest.fixture
def l4(request):
    return Layer({"e": ["-!f"]})


@pytest.fixture
def l5(request):
    return Layer({"-!a": None, "a": {"j": "k"}})


@pytest.fixture
def l6(request):
    return Layer({"a": ["-!b"]})


@pytest.fixture
def l7(request):
    return Layer({"i": 1})


@pytest.fixture
def l8(request):
    return Layer({"e": ['x']})


def test_add(stack, l1, d0):
    result = d0
    result["a"]["j"] = "k"
    stack.push(l1)
    assert stack.as_dict() == result


def test_add2(stack, l8, d0):
    result = d0
    result["e"] += ["x"]
    stack.push(l8)
    assert stack.as_dict() == result


def test_override(stack, l5, d0):
    result = d0
    result["a"] = {"j": "k"}
    stack.push(l5)
    assert stack.as_dict() == result


def test_override2(stack, l7, d0):
    result = d0
    result["i"] = 1
    stack.push(l7)
    assert stack.as_dict() == result


def test_deleteproperty(stack, l2, d0):
    result = d0
    del result["a"]
    stack.push(l2)
    assert stack.as_dict() == result


def test_deleteproperty2(stack, l6, d0):
    result = d0
    del result["a"]["b"]
    stack.push(l6)
    assert stack.as_dict() == result


def test_deleteitem(stack, l3, d0):
    result = d0
    result["e"].remove("f")
    stack.push(l3)
    assert stack.as_dict() == result


def test_deleteitem2(stack, l4, d0):
    result = d0
    result["e"].remove("f")
    stack.push(l4)
    assert stack.as_dict() == result
