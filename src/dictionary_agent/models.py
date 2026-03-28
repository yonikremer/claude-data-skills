from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class UsageExample(BaseModel):
    context: str
    source: str
    date_added: str = Field(default_factory=lambda: datetime.now().isoformat())

class DictionaryEntry(BaseModel):
    term: str
    definition: str
    source_file: str
    usage_examples: List[UsageExample] = []
    related_terms: List[str] = []
    is_golden: bool = False

class Dictionary(BaseModel):
    entries: Dict[str, DictionaryEntry] = {}
