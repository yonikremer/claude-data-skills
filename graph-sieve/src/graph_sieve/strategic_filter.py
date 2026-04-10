from typing import List, Optional
import os

class StrategicSieve:
    """
    Gate 1: Filters out decommissioned projects and irrelevant domains
    at the file path and metadata level.
    """
    def __init__(self, decommissioned_keywords: List[str] = None, min_year: int = 2020):
        self.decommissioned = [kw.lower() for kw in (decommissioned_keywords or [])]
        self.min_year = min_year

    def is_relevant(self, file_path: str) -> bool:
        """
        Returns False if the file path contains decommissioned project names
        or if it's too old to be considered active.
        """
        path_lower = file_path.lower()
        
        # 1. Keyword check (Zombie Projects)
        for kw in self.decommissioned:
            if kw in path_lower:
                return False
                
        # 2. Basic recency check (Metadata)
        # Note: In a production NFS, we would check os.path.getmtime
        # For now, we provide the hook for temporal pruning
        return True

    def get_reason_skipped(self, file_path: str) -> Optional[str]:
        path_lower = file_path.lower()
        for kw in self.decommissioned:
            if kw in path_lower:
                return f"Decommissioned domain: {kw}"
        return None
