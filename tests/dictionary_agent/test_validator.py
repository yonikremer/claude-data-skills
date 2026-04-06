from src.dictionary_agent.validator import validate_with_llm

def test_valid_overview():
    raw_text = "Project Prism is our new internal firewall."
    extraction = {
        "term": "Prism",
        "overview": "An internal firewall project.",
        "deep_dive": "It handles network traffic filtering.",
        "anchor": "Project Prism is our new internal firewall."
    }
    # Should pass as it's consistent AND anchor exists
    result = validate_with_llm(raw_text, extraction)
    assert result["is_valid"] is True
    assert result["status"] == "PASS"

def test_invalid_overview():
    raw_text = "Project Prism is our new internal firewall."
    extraction = {
        "term": "Prism",
        "overview": "A new coffee machine in the breakroom.",
        "deep_dive": "It makes espresso.",
        "anchor": "new coffee machine" # This doesn't exist in raw_text
    }
    # Should fail as anchor doesn't exist
    result = validate_with_llm(raw_text, extraction)
    assert result["is_valid"] is False
    assert result["status"] == "HALLUCINATION"
