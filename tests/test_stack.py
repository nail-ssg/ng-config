import pytest
from pack.ng_stack import Layer, Stack


def setup():
    print("basic setup into module")
    st = Stack()
    l1 = Layer({"a": {"b": "c", "d": 1}, "e": [
               2, 3, "f"], "g": "h", "i": None})
    l2 = Layer({"a": {"j": "k"}})
    l3 = Layer({"-a": None})
    l3 = Layer({"e-": ["f"]})
    st.push(l1)
    r1 = {}
    r2 = {}
    r3 = {}


def teardown():
    print("basic teardown into module")


def setup_module(module):
    print("module setup")


def teardown_module(module):
    print("module teardown")


def setup_function(function):
    print("function setup")


def teardown_function(function):
    print("function teardown")


def test_deleteproperty():
    st.push(l2)
    assert st.as_dict == r1


def test_deleteitem():
    st.push(l3)
    assert st.as_dict == r2


def test_override():
    st.push(l4)
    assert st.as_dict == r3


# def test_deleteproperty():
#     assert 1 == 2
