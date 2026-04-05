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

    def chat(self, messages: List[Dict[str, str]], json_mode: bool = True) -> Dict[str, Any]:
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
        last_msg = messages[-1]["content"].lower()
        
        # Mock Gate 2: Extraction
        if "extract" in last_msg:
            return [
                {
                    "term": "Prism",
                    "definition": "A new security project.",
                    "anchor": "Project Prism uses port 8080.",
                    "is_new": True,
                    "entity_type": "PROJECT"
                }
            ]
        
        # Mock Gate 3: Validation
        if "validate" in last_msg:
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
