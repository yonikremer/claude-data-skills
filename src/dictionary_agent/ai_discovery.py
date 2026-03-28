from typing import List, Dict, Optional
from .models import DictionaryEntry, UsageExample, Dictionary
from datetime import datetime

# In a real implementation, this would call an LLM API.
# Here we provide the logic that an agent (like Gemini) would use.

def get_extraction_prompt(text: str, existing_terms: List[str]) -> str:
    prompt = f"""
Identify all technical terms, internal project names, and domain-specific acronyms in the following text.
For each term, provide a concise, AI-ready definition based on the context.

Existing terms already in the dictionary: {', '.join(existing_terms)}

For existing terms:
- If the text provides new context or a different meaning, provide a 'refined definition' or 'new usage example'.
- If the text just confirms existing knowledge, ignore it.

For new terms:
- Provide the term name and its definition.

Text:
{text}

Format the response as a JSON list of objects:
[
  {{
    "term": "Term Name",
    "definition": "Clear concise definition",
    "is_new": true,
    "usage_context": "The sentence where it was found"
  }}
]
"""
    return prompt

def process_discovered_terms(discovered_terms: List[Dict], dictionary: Dictionary, source_file: str):
    for item in discovered_terms:
        term = item["term"]
        definition = item["definition"]
        usage_context = item.get("usage_context", "")
        
        if term in dictionary.entries:
            # Enrich existing term
            entry = dictionary.entries[term]
            # Add usage example if not already there
            new_example = UsageExample(context=usage_context, source=source_file)
            entry.usage_examples.append(new_example)
            # Potentially update definition if it's "better" or just append?
            # For now, we append usage context.
        else:
            # Create new entry
            entry = DictionaryEntry(
                term=term,
                definition=definition,
                source_file=source_file,
                usage_examples=[UsageExample(context=usage_context, source=source_file)]
            )
            dictionary.entries[term] = entry
