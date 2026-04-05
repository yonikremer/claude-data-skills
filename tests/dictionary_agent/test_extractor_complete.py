import pytest
import os
from src.dictionary_agent.extractor import extract_all
from unittest.mock import MagicMock, patch

def test_extract_txt():
    path = "tests/data/test.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("This is a plain text file with project Prism.")
    
    text = extract_all(path)
    assert "project Prism" in text

def test_extract_docx_unified():
    # sample.docx exists from baseline setup in worktree
    path = ".worktrees/feat/multi-format-graph-rag/tests/data/sample.docx"
    if not os.path.exists(path):
        path = "tests/data/sample.docx"
    text = extract_all(path)
    assert "Project Prism" in text

def test_extract_msg_unified():
    with patch("extract_msg.Message") as mock_msg_class:
        mock_msg = MagicMock()
        mock_msg.subject = "Unified Test"
        mock_msg.body = "Body of msg"
        mock_msg_class.return_value = mock_msg
        
        text = extract_all("tests/data/fake.msg")
        assert "Unified Test" in text

def test_extract_one_unified():
    with patch("pyOneNote.Main.OneDocment") as mock_one_class:
        # Since pyOneNote structure is complex, we mock the high level 
        # or the specific function we use.
        # If we use a simpler mock for now:
        with patch("src.dictionary_agent.extractor.extract_text_from_one") as mock_extract:
            mock_extract.return_value = "OneNote content with project Cortex"
            text = extract_all("tests/data/test.one")
            assert "project Cortex" in text
