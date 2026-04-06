from datetime import datetime
from typing import List, Dict, Literal, Optional
from pydantic import BaseModel, Field

ENTITY_TYPES = Literal["PROJECT", "COMPONENT", "TECH_STACK", "PERSON", "ORG"]
RELATION_TYPES = Literal[
    "SUB_PROJECT_OF", "HAS_SUB_PROJECT",
    "DEPENDS_ON", "IS_DEPENDED_ON_BY",
    "USES", "IS_USED_BY",
    "MANAGED_BY", "MANAGES",
    "REPLACES", "IS_REPLACED_BY",
    "ALIAS_OF",
    "IS_MANAGER_OF", "IS_MANAGED_BY",
    "IS_SUB_ORGANIZATION_OF", "HAS_SUB_ORGANIZATION",
    "IS_FEATURE_OF", "HAS_FEATURE",
    "IS_MEANT_TO_DEAL_WITH", "IS_DEALT_WITH_BY",
    "IS_ISSUE_OF", "HAS_ISSUE",
    "STORES_DATA_IN", "STORES_DATA_FOR",
    "SUPERSEDES", "IS_SUPERSEDED_BY",
    "IS_EXPERT_OF", "HAS_EXPERT",
    "MIGRATED_FROM", "MIGRATED_TO",
    "MONITORED_BY", "MONITORS",
    "ENRICHES", "IS_ENRICHED_BY",
    "PART_OF_INITIATIVE", "HAS_PART_PROJECT",
    "MANDATED_BY", "MANDATES",
    "MENTORS", "IS_MENTORED_BY",
    "BEST_PRACTICE_FOR", "HAS_BEST_PRACTICE",
    "INTERNAL_CUSTOMER_OF", "HAS_INTERNAL_CUSTOMER",
    "REPORTS_TO", "HAS_DIRECT_REPORT"
]

RELATION_INVERSES = {
    "SUB_PROJECT_OF": "HAS_SUB_PROJECT",
    "HAS_SUB_PROJECT": "SUB_PROJECT_OF",
    "DEPENDS_ON": "IS_DEPENDED_ON_BY",
    "IS_DEPENDED_ON_BY": "DEPENDS_ON",
    "USES": "IS_USED_BY",
    "IS_USED_BY": "USES",
    "MANAGED_BY": "MANAGES",
    "MANAGES": "MANAGED_BY",
    "REPLACES": "IS_REPLACED_BY",
    "IS_REPLACED_BY": "REPLACES",
    "ALIAS_OF": "ALIAS_OF",
    "IS_MANAGER_OF": "IS_MANAGED_BY",
    "IS_MANAGED_BY": "IS_MANAGER_OF",
    "IS_SUB_ORGANIZATION_OF": "HAS_SUB_ORGANIZATION",
    "HAS_SUB_ORGANIZATION": "IS_SUB_ORGANIZATION_OF",
    "IS_FEATURE_OF": "HAS_FEATURE",
    "HAS_FEATURE": "IS_FEATURE_OF",
    "IS_MEANT_TO_DEAL_WITH": "IS_DEALT_WITH_BY",
    "IS_DEALT_WITH_BY": "IS_MEANT_TO_DEAL_WITH",
    "IS_ISSUE_OF": "HAS_ISSUE",
    "HAS_ISSUE": "IS_ISSUE_OF",
    "STORES_DATA_IN": "STORES_DATA_FOR",
    "STORES_DATA_FOR": "STORES_DATA_IN",
    "SUPERSEDES": "IS_SUPERSEDED_BY",
    "IS_SUPERSEDED_BY": "SUPERSEDES",
    "IS_EXPERT_OF": "HAS_EXPERT",
    "HAS_EXPERT": "IS_EXPERT_OF",
    "MIGRATED_FROM": "MIGRATED_TO",
    "MIGRATED_TO": "MIGRATED_FROM",
    "MONITORED_BY": "MONITORS",
    "MONITORS": "MONITORED_BY",
    "ENRICHES": "IS_ENRICHED_BY",
    "IS_ENRICHED_BY": "ENRICHES",
    "PART_OF_INITIATIVE": "HAS_PART_PROJECT",
    "HAS_PART_PROJECT": "PART_OF_INITIATIVE",
    "MANDATED_BY": "MANDATES",
    "MANDATES": "MANDATED_BY",
    "MENTORS": "IS_MENTORED_BY",
    "IS_MENTORED_BY": "MENTORS",
    "BEST_PRACTICE_FOR": "HAS_BEST_PRACTICE",
    "HAS_BEST_PRACTICE": "BEST_PRACTICE_FOR",
    "INTERNAL_CUSTOMER_OF": "HAS_INTERNAL_CUSTOMER",
    "HAS_INTERNAL_CUSTOMER": "INTERNAL_CUSTOMER_OF",
    "REPORTS_TO": "HAS_DIRECT_REPORT",
    "HAS_DIRECT_REPORT": "REPORTS_TO"
}

STATUS_TYPES = Literal["ACTIVE", "LEGACY", "DORMANT", "PROPOSED", "PENDING_DEFINITION"]
AUTHORITY_LEVELS = Literal["SEED", "DISCOVERED"]
CONFIDENCE_LEVELS = Literal["GOLD", "SILVER", "BRONZE", "PENDING"]

RELATION_WEIGHTS = {
    "ALIAS_OF": 1.0,
    "SUPERSEDES": 0.9,
    "IS_SUPERSEDED_BY": 0.9,
    "SUB_PROJECT_OF": 0.8,
    "HAS_SUB_PROJECT": 0.8,
    "IS_SUB_ORGANIZATION_OF": 0.8,
    "HAS_SUB_ORGANIZATION": 0.8,
    "PART_OF_INITIATIVE": 0.8,
    "HAS_PART_PROJECT": 0.8,
    "MANDATED_BY": 0.8,
    "MANDATES": 0.8,
    "IS_FEATURE_OF": 0.7,
    "HAS_FEATURE": 0.7,
    "IS_MANAGER_OF": 0.7,
    "IS_MANAGED_BY": 0.7,
    "IS_EXPERT_OF": 0.7,
    "HAS_EXPERT": 0.7,
    "REPORTS_TO": 0.7,
    "HAS_DIRECT_REPORT": 0.7,
    "DEPENDS_ON": 0.6,
    "IS_DEPENDED_ON_BY": 0.6,
    "STORES_DATA_IN": 0.6,
    "STORES_DATA_FOR": 0.6,
    "ENRICHES": 0.6,
    "IS_ENRICHED_BY": 0.6,
    "MENTORS": 0.6,
    "IS_MENTORED_BY": 0.6,
    "IS_MEANT_TO_DEAL_WITH": 0.5,
    "IS_DEALT_WITH_BY": 0.5,
    "IS_ISSUE_OF": 0.5,
    "HAS_ISSUE": 0.5,
    "MIGRATED_FROM": 0.5,
    "MIGRATED_TO": 0.5,
    "MONITORED_BY": 0.5,
    "MONITORS": 0.5,
    "MANAGED_BY": 0.4,
    "MANAGES": 0.4,
    "USES": 0.3,
    "IS_USED_BY": 0.3,
    "REPLACES": 0.2,
    "IS_REPLACED_BY": 0.2
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
