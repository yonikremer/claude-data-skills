import pytest
import os
import json
from graph_sieve.storage import save_dictionary, load_dictionary
from graph_sieve.models import Dictionary, DictionaryEntry

def test_save_and_load_dictionary(tmp_path):
    dict_file = tmp_path / "test_dictionary.json"
    entry = DictionaryEntry(
        term="Test Term",
        overview="Test Overview",
        source_file="test.pdf"
    )
    dictionary = Dictionary(entries={"Test Term": entry})
    
    save_dictionary(dictionary, str(dict_file))
    
    # Check if file exists
    assert os.path.exists(dict_file)
    
    # Load and verify
    loaded = load_dictionary(str(dict_file))
    assert "Test Term" in loaded.entries
    assert loaded.entries["Test Term"].overview == "Test Overview"

def test_load_nonexistent_file():
    # Should return a blank dictionary, not crash
    loaded = load_dictionary("nonexistent.json")
    assert isinstance(loaded, Dictionary)
    assert len(loaded.entries) == 0
