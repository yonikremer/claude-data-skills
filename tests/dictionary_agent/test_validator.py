from src.dictionary_agent.validator import validate_definition

def test_valid_definition():
    raw_text = "Project Prism is our new internal firewall."
    definition = "An internal firewall project named Prism."
    # Should pass as it's consistent
    assert validate_definition(raw_text, definition) is True

def test_invalid_definition():
    raw_text = "Project Prism is our new internal firewall."
    definition = "A new coffee machine in the breakroom."
    # Should fail as it's a hallucination
    assert validate_definition(raw_text, definition) is False
