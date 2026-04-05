import json
import os

from .models import Dictionary


def load_dictionary(file_path: str) -> Dictionary:
    if not os.path.exists(file_path):
        return Dictionary()
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return Dictionary.model_validate(data)


def save_dictionary(dictionary: Dictionary, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(dictionary.model_dump_json(indent=2))
