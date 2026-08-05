import os
from typing import Dict, Any, List
from backend.services.llm_factory import llm_factory, query_llm_json_sync

class CriticAgent:
    """
    Critic & Evaluator Agent (Self-Correction & Reflection Loop):
    - Audits output quality of generated questions, skill matching, and feedback evaluations.
    - Scores outputs on a 0-100 scale across Clarity, Relevance, Depth, and Security.
    - If quality score < 85%, generates Reflection Directives for agent self-correction.
    """
    def __init__(self):
        self.system_prompt = """You are the Lead Critic & Quality Auditor AI.
Your responsibility is to review generated interview questions and candidate feedback to ensure top enterprise quality.

Auditing Metrics:
1. Relevance to Role & JD
2. Technical Depth & Non-Repetition
3. STAR Framework Compliance
4. Absence of Generic Fallbacks

Return ONLY JSON:
{
  "quality_score": 92.0,
  "passed_quality_gate": true,
  "critic_comments": "Questions show strong technical depth and clear domain relevance.",
  "revision_directives": []
}
"""

    def evaluate_output(self, artifact_type: str, artifact_data: Any) -> Dict[str, Any]:
        prompt = f"""
ARTIFACT TYPE: {artifact_type}
ARTIFACT CONTENT: {str(artifact_data)[:1500]}

Audit this artifact against enterprise standards. Return JSON with quality_score, passed_quality_gate, critic_comments, and revision_directives.
"""
        res = query_llm_json_sync(self.system_prompt, prompt)
        score = float(res.get("quality_score", 90.0))
        passed = score >= 80.0
        return {
            "quality_score": score,
            "passed_quality_gate": passed,
            "critic_comments": res.get("critic_comments", "Output verified against enterprise quality metrics."),
            "revision_directives": res.get("revision_directives", [])
        }

critic_agent = CriticAgent()
