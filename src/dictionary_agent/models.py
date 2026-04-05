from datetime import datetime
from typing import List, Dict, Literal, Optional
from pydantic import BaseModel, Field

ENTITY_TYPES = Literal["PROJECT", "COMPONENT", "TECH_STACK", "PERSON", "ORG"]
RELATION_TYPES = Literal["SUB_PROJECT_OF", "DEPENDS_ON", "USES", "MANAGED_BY", "REPLACES"]

class UsageExample(BaseModel):
    context: str
    source: str
    date_added: str = Field(default_factory=lambda: datetime.now().isoformat())

class DictionaryEntry(BaseModel):
    term: str
    definition: str
    source_file: str
    entity_type: Optional[ENTITY_TYPES] = None
    usage_examples: List[UsageExample] = []
    related_terms: List[str] = []
    is_golden: bool = False

class GraphTriplet(BaseModel):
    subject: str
    relationship: RELATION_TYPES
    object: str
    anchor: str
    source_file: str
    date_added: str = Field(default_factory=lambda: datetime.now().isoformat())

class Dictionary(BaseModel):
    entries: Dict[str, DictionaryEntry] = {}
    relationships: List[GraphTriplet] = []
