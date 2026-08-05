import os
from typing import Dict, Any
from backend.services.llm_factory import query_llm_json_sync

class CompanyResearchAgent:
    """
    Company Research Agent:
    Provides company tech stack breakdown, engineering culture principles, recent tech blog topics, and interview tips.
    """
    def __init__(self):
        self.system_prompt = """You are a Lead Tech Recruiter & Company Intelligence Analyst.
Analyze company name and return tech stack details, engineering culture principles, and interview prep strategy.

Return ONLY JSON:
{
  "company_name": "Amazon",
  "tech_stack": ["Java", "Python", "AWS DynamoDB", "AWS Lambda", "React"],
  "culture_focus": "16 Leadership Principles (Customer Obsession, Ownership, Bias for Action)",
  "interview_rounds": ["Recruiter Screen", "Technical Phone Screen", "Loop Interview (4-5 rounds)"],
  "key_prep_tips": [
    "Format ALL behavioral answers strictly using STAR method.",
    "Be prepared to answer 'Why Amazon?' with specific tech blog or customer impact examples."
  ]
}
"""

    def research_company(self, company_name: str) -> Dict[str, Any]:
        prompt = f"TARGET COMPANY: {company_name}"
        return query_llm_json_sync(self.system_prompt, prompt)

company_research_agent = CompanyResearchAgent()
