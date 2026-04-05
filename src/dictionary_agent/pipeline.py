from typing import List, Dict
import os
from .extractor import extract_text_from_pdf, extract_text_from_pptx, extract_text_from_docx, extract_text_from_msg
from .filters import is_domain_specific
from .discovery import extract_with_anchors
from .validator import validate_definition
from .models import Dictionary, DictionaryEntry, UsageExample

class SelectiveKnowledgePipeline:
    def __init__(self, dictionary: Dictionary = None, whitelist: List[str] = None):
        self.dictionary = dictionary or Dictionary()
        self.whitelist = whitelist or []

    def process_document(self, file_path: str) -> List[str]:
        """
        Runs the full 4-gate pipeline on a document.
        Returns a list of successfully added terms.
        """
        # Gate 0: Extraction
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext == ".pptx":
            text = extract_text_from_pptx(file_path)
        elif ext == ".docx":
            text = extract_text_from_docx(file_path)
        elif ext == ".msg":
            text = extract_text_from_msg(file_path)
        else:
            # Fallback for plain text
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        added_terms = []
        
        # Gate 2: Extraction with Anchors
        discovered = extract_with_anchors(text)
        
        for item in discovered:
            term = item["term"]
            definition = item["definition"]
            anchor = item["anchor"]
            
            # Gate 1: Filter
            if not is_domain_specific(term, self.whitelist):
                continue
                
            # Gate 3: Validation
            if not validate_definition(anchor, definition):
                continue
                
            # Add to dictionary if passed all gates
            if term not in self.dictionary.entries:
                self.dictionary.entries[term] = DictionaryEntry(
                    term=term,
                    definition=definition,
                    source_file=file_path,
                    usage_examples=[UsageExample(context=anchor, source=file_path)]
                )
                added_terms.append(term)
            else:
                # Enrich existing
                entry = self.dictionary.entries[term]
                entry.usage_examples.append(UsageExample(context=anchor, source=file_path))
                
        return added_terms
