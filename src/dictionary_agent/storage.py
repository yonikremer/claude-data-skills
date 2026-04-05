import json
import os

from .models import Dictionary, DictionaryEntry


class LayeredDictionary:
    """
    Implements multi-level retrieval (L1 Active Cache, L2 Semantic Repository).
    """
    def __init__(self, l1_cache: dict = None, l2_store: Dictionary = None):
        self.l1_cache = l1_cache or {}
        self.l2_store = l2_store or Dictionary()

    def get_entry(self, term: str) -> DictionaryEntry:
        # Check L1 (Active Task)
        if term in self.l1_cache:
            return self.l1_cache[term]
        
        # Check L2 (Full Dictionary)
        if term in self.l2_store.entries:
            return self.l2_store.entries[term]
            
        return None

def load_dictionary(file_path: str) -> Dictionary:
    if not os.path.exists(file_path):
        return Dictionary()
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return Dictionary.model_validate(data)


def save_dictionary(dictionary: Dictionary, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(dictionary.model_dump_json(indent=2))
