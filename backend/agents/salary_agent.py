import os
from typing import Dict, Any
from backend.services.llm_factory import query_llm_json_sync

class SalaryEstimatorAgent:
    """
    Salary & Compensation Estimator Agent:
    Estimates market base salary, equity stock grants, performance bonus, and total compensation (TC)
    based on role title, experience level, location, and candidate skill match score.
    """
    def __init__(self):
        self.system_prompt = """You are a Principal Executive Compensation Analyst & Tech Recruiter.
Analyze role title, experience level, location, and skill match percentage to calculate market compensation estimates.

Return ONLY JSON:
{
  "role": "Senior Software Engineer",
  "currency": "USD",
  "base_salary_range": "$160,000 - $195,000",
  "equity_range": "$40,000 - $75,000 / yr",
  "bonus_range": "$20,000 - $35,000",
  "total_compensation": "$220,000 - $305,000",
  "market_percentile": "75th Percentile",
  "negotiation_tips": [
    "Highlight full-stack FastAPI + React expertise to negotiate upper band.",
    "Leverage competing market offers during final recruiter screen."
  ]
}
"""

    def estimate_compensation(self, role_title: str, experience_years: int = 3, match_score: float = 85.0, location: str = "United States / Remote") -> Dict[str, Any]:
        prompt = f"ROLE: {role_title}\nEXPERIENCE: {experience_years} years\nSKILL MATCH: {match_score}%\nLOCATION: {location}"
        return query_llm_json_sync(self.system_prompt, prompt)

salary_agent = SalaryEstimatorAgent()
