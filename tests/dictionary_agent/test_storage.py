import os

from src.dictionary_agent.models import Dictionary, DictionaryEntry
from src.dictionary_agent.storage import load_dictionary, save_dictionary


def test_save_and_load_dictionary(tmp_path):
    dict_file = tmp_path / "test_dictionary.json"
    entry = DictionaryEntry(
        term="Test Term",
        definition="Test Definition",
        source_file="test.pdf"
    )
    dictionary = Dictionary(entries={"Test Term": entry})

    save_dictionary(dictionary, str(dict_file))
    assert os.path.exists(dict_file)

    loaded_dict = load_dictionary(str(dict_file))
    assert "Test Term" in loaded_dict.entries
    assert loaded_dict.entries["Test Term"].definition == "Test Definition"


def test_load_non_existent_dictionary():
    loaded_dict = load_dictionary("non_existent.json")
    assert isinstance(loaded_dict, Dictionary)
    assert len(loaded_dict.entries) == 0
