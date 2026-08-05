import json
import os
from typing import Dict, Any
from groq import Groq
from backend.config import settings

from backend.services.llm_factory import llm_factory, query_llm_json_sync

def get_groq_client() -> Groq:
    api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
    return Groq(api_key=api_key)

def query_groq_json(system_prompt: str, user_content: str, max_retries: int = 3) -> Dict[str, Any]:
    """
    Delegates to MultiProviderLLMFactory for fallback resiliency and backward compatibility.
    """
    return query_llm_json_sync(system_prompt, user_content)
