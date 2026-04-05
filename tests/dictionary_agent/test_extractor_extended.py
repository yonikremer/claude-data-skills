import pytest
import os
from src.dictionary_agent.extractor import extract_text_from_docx, extract_text_from_msg
from unittest.mock import MagicMock, patch

def test_extract_docx():
    # sample.docx was created in previous step in worktree
    path = ".worktrees/feat/selective-knowledge-injection/tests/data/sample.docx"
    if not os.path.exists(path):
        # Fallback if running inside worktree already
        path = "tests/data/sample.docx"
    assert os.path.exists(path)
    text = extract_text_from_docx(path)
    assert "Project Prism" in text
    assert "8080" in text

def test_extract_msg():
    # We mock extract_msg since creating a real .msg is hard
    with patch("extract_msg.Message") as mock_msg_class:
        mock_msg = MagicMock()
        mock_msg.subject = "Test Subject"
        mock_msg.body = "This is a test body with project Cortex."
        mock_msg_class.return_value = mock_msg
        
        text = extract_text_from_msg("tests/data/fake.msg")
        assert "Subject: Test Subject" in text
        assert "project Cortex" in text
