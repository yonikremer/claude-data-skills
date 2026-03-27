from validator import Validator

def test_compare_outputs_exact():
    v = Validator()
    assert v.compare({"a": 1}, {"a": 1}) is True
    assert v.compare({"a": 1}, {"a": 2}) is False

def test_compare_outputs_epsilon():
    v = Validator(epsilon=0.001)
    assert v.compare({"a": 1.0001}, {"a": 1.0002}) is True
    assert v.compare({"a": 1.1}, {"a": 1.2}) is False
