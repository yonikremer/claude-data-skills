import pytest
from graph_sieve.strategic_filter import StrategicSieve

def test_decommissioned_path():
    sieve = StrategicSieve(decommissioned_keywords=["Project-Zephyr", "Legacy-Portal"])
    
    assert sieve.is_relevant("C:/Docs/Active/Prism.docx") is True
    assert sieve.is_relevant("C:/Archive/Project-Zephyr/notes.txt") is False
    assert sieve.is_relevant("C:/Legacy-Portal/index.msg") is False

def test_skip_reason():
    sieve = StrategicSieve(decommissioned_keywords=["Zephyr"])
    reason = sieve.get_reason_skipped("C:/Docs/Zephyr/final.pdf")
    assert "zephyr" in reason.lower()
