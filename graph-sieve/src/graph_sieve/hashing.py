import hashlib
import json
import os
from typing import Dict

class HashStore:
    """
    Stores SHA-256 hashes of processed files to prevent redundant LLM calls.
    """
    def __init__(self, file_path: str = "storage/hashes.json"):
        self.file_path = file_path
        self.hashes: Dict[str, str] = self._load()

    def _load(self) -> Dict[str, str]:
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            return {}
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.hashes, f, indent=2)

    def get_hash(self, file_path: str) -> str:
        """
        Calculates SHA-256 hash of a file.
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def has_changed(self, file_path: str) -> bool:
        """
        Returns True if the file has changed or is new.
        """
        if not os.path.exists(file_path):
            return False
        current_hash = self.get_hash(file_path)
        old_hash = self.hashes.get(file_path)
        
        if current_hash != old_hash:
            self.hashes[file_path] = current_hash
            return True
        return False
