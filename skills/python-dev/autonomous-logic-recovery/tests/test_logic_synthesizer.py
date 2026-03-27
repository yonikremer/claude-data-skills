import json
from logic_synthesizer import LogicSynthesizer

def test_parse_trace():
    logs = [
        "DEBUG: if (x > 0) entered",
        "Result: 42"
    ]
    synthesizer = LogicSynthesizer()
    parsed = synthesizer.parse(logs)
    assert parsed[0]['decision'] == "if (x > 0)"
    assert parsed[1]['result'] == "42"

def test_generate_pytest():
    trace = [
        {"input": {"x": 1}, "output": 42}
    ]
    synthesizer = LogicSynthesizer()
    test_code = synthesizer.generate_test(trace)
    assert "expected = 42" in test_code
    assert "assert result == expected" in test_code
    assert "input_data = {'x': 1}" in test_code
