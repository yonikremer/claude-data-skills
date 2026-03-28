import os
import json
from .storage import load_dictionary, save_dictionary
from .extractor import extract_text_from_pdf, extract_text_from_pptx
from .ai_discovery import process_discovered_terms
from typing import List, Dict

class DictionaryAgent:
    def __init__(self, dictionary_path: str):
        self.dictionary_path = dictionary_path
        self.dictionary = load_dictionary(dictionary_path)
    
    def scan_file(self, file_path: str):
        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".pptx"):
            text = extract_text_from_pptx(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            return
        
        # In a real agent workflow, this would be an LLM call.
        # For the framework, we provide the logic to process discovered terms.
        # The terms themselves should come from the AI during execution.
        return text
    
    def update_dictionary(self, discovered_terms: List[Dict], source_file: str):
        process_discovered_terms(discovered_terms, self.dictionary, source_file)
        save_dictionary(self.dictionary, self.dictionary_path)
