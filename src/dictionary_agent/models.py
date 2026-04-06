from datetime import datetime
from typing import List, Dict, Literal, Optional
from pydantic import BaseModel, Field

ENTITY_TYPES = Literal["PROJECT", "COMPONENT", "TECH_STACK", "PERSON", "ORG"]
RELATION_TYPES = Literal["SUB_PROJECT_OF", "DEPENDS_ON", "USES", "MANAGED_BY", "REPLACES", "ALIAS_OF"]
STATUS_TYPES = Literal["ACTIVE", "LEGACY", "DORMANT", "PROPOSED", "PENDING_DEFINITION"]
AUTHORITY_LEVELS = Literal["SEED", "DISCOVERED"]
CONFIDENCE_LEVELS = Literal["GOLD", "SILVER", "BRONZE", "PENDING"]

RELATION_WEIGHTS = {
    "ALIAS_OF": 1.0,
    "SUB_PROJECT_OF": 0.8,
    "DEPENDS_ON": 0.6,
    "MANAGED_BY": 0.4,
    "USES": 0.3,
    "REPLACES": 0.2
}

class UsageExample(BaseModel):
    context: str
    source: str
    date_added: str = Field(default_factory=lambda: datetime.now().isoformat())

class DictionaryEntry(BaseModel):
    term: str
    overview: str = Field(description="A concise, 1-sentence executive summary.")
    deep_dive: Optional[str] = Field(default=None, description="Detailed technical information, formulas, or implementation specifics.")
    source_file: str
    entity_type: Optional[ENTITY_TYPES] = None
    usage_examples: List[UsageExample] = []
    related_terms: List[str] = []
    is_golden: bool = False
    status: STATUS_TYPES = "ACTIVE"
    authority_level: AUTHORITY_LEVELS = "DISCOVERED"
    confidence_level: CONFIDENCE_LEVELS = "BRONZE"
    last_seen: str = Field(default_factory=lambda: datetime.now().isoformat())
    document_count: int = 0
    is_bounty: bool = False

class GraphTriplet(BaseModel):
    subject: str
    relationship: RELATION_TYPES
    object: str
    anchor: str
    source_file: str
    weight: float = 0.5
    date_added: str = Field(default_factory=lambda: datetime.now().isoformat())
    status: STATUS_TYPES = "ACTIVE"

class CommunityReport(BaseModel):
    community_id: str
    title: str
    summary: str
    nodes: List[str]
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())

class Dictionary(BaseModel):
    entries: Dict[str, DictionaryEntry] = {}
    relationships: List[GraphTriplet] = []
    community_reports: List[CommunityReport] = []
