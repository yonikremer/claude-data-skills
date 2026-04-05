import json
import os
import requests
from typing import Dict, List, Any

class LocalLLMClient:
    """
    Client for interacting with local Ollama/vLLM models.
    Supports JSON mode for structured extraction.
    """
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url
        self.model = model

    def chat(self, messages: List[Dict[str, str]], json_mode: bool = True) -> Any:
        """
        Sends a chat request to the local LLM.
        """
        # Mock for environments where Ollama is not running
        if os.getenv("MOCK_LLM", "false").lower() == "true":
            return self._mock_response(messages)

        endpoint = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "format": "json" if json_mode else None
        }
        
        try:
            response = requests.post(endpoint, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            content = data.get("message", {}).get("content", "")
            
            if json_mode:
                return json.loads(content)
            return content
        except Exception as e:
            print(f"Error calling local LLM: {e}")
            return self._mock_response(messages)

    def _mock_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Provides a fallback mock response for testing.
        """
        system_msg = ""
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"].lower()
        
        # Mock Gate 2: Extraction
        if "librarian" in system_msg:
            last_user_msg = messages[-1]["content"].lower()
            if "prism" in last_user_msg:
                return [
                    {
                        "term": "Prism",
                        "definition": "A new security project.",
                        "anchor": "The project Prism uses port 8080 for secure communication.",
                        "is_new": True,
                        "entity_type": "PROJECT"
                    }
                ]
            if "sql" in last_user_msg:
                return [
                    {
                        "term": "SQL",
                        "definition": "A domain-specific SQL implementation.",
                        "anchor": "Project SQL is a new database system.",
                        "is_new": True,
                        "entity_type": "TECH_STACK"
                    }
                ]
            return []
        
        # Mock Gate 3: Validation
        if "reviewer" in system_msg:
            last_user_msg = messages[-1]["content"].lower()
            # Simulate a failure for 'coffee' to test negative cases
            if "coffee" in last_user_msg:
                return {
                    "is_valid": False,
                    "status": "HALLUCINATION",
                    "reasoning": "Not supported by context."
                }
            return {
                "is_valid": True,
                "status": "PASS",
                "reasoning": "Supported by context."
            }
            
        return {"error": "Mock not implemented for this prompt"}

def get_llm_client():
    return LocalLLMClient(
        base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama3")
    )
