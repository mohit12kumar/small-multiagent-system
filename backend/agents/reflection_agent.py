import os
from typing import Dict, Any, List
from backend.services.llm_factory import query_llm_json_sync

class ReflectionAgent:
    """
    Reflection & Self-Correction Agent:
    Takes Critic Agent directives and revises generated content to eliminate hallucinations,
    improve technical depth, and ensure enterprise standard compliance.
    """
    def __init__(self):
        self.system_prompt = """You are a Lead AI Quality & Reflection Specialist.
Given original content and Critic Agent directives, rewrite and improve the content to address all feedback.

Return ONLY JSON:
{
  "improved_content": {},
  "applied_revisions": ["Enhanced technical depth", "Eliminated redundant phrasing"],
  "reflection_score": 95.0
}
"""

    def reflect_and_improve(self, original_content: Any, critic_directives: List[str]) -> Dict[str, Any]:
        prompt = f"ORIGINAL CONTENT:\n{str(original_content)[:1500]}\n\nCRITIC DIRECTIVES:\n{', '.join(critic_directives) if critic_directives else 'Improve technical depth.'}"
        return query_llm_json_sync(self.system_prompt, prompt)

reflection_agent = ReflectionAgent()
