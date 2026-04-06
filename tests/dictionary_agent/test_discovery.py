import pytest
import os
from src.dictionary_agent.discovery import extract_with_anchors

def test_anchored_extraction():
    # Sample text with a clear term and context
    text = "The project Prism uses port 8080 for secure communication."

    # Force mock LLM for local test
    os.environ["MOCK_LLM"] = "true"
    result = extract_with_anchors(text)

    assert len(result) > 0
    assert "term" in result[0]
    assert "overview" in result[0]
    assert "anchor" in result[0]
    assert "Prism" in result[0]["term"]

def test_no_extraction_on_empty_text():
    text = ""
    result = extract_with_anchors(text)
    assert len(result) == 0
