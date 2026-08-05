import os
from typing import Dict, Any
from backend.services.groq_service import query_groq_json

class JobDescriptionAnalyzerAgent:
    """
    Agent 2: Job Description Analyzer Agent
    Responsibilities:
    - Extract required skills
    - Extract years of experience
    - Identify core responsibilities & company keywords
    """
    def __init__(self):
        prompt_path = os.path.join("backend", "prompts", "jd_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = "You are a JD Analyzer Agent. Return JSON with required_skills, experience_years, role_title, responsibilities, company_keywords."

    def analyze_jd_text(self, jd_text: str) -> Dict[str, Any]:
        if not jd_text or len(jd_text.strip()) == 0:
            return {
                "required_skills": [],
                "experience_years": 0,
                "role_title": "General Role",
                "responsibilities": [],
                "company_keywords": []
            }
        
        user_content = f"JOB DESCRIPTION TEXT:\n{jd_text[:4000]}"
        result = query_groq_json(self.system_prompt, user_content)
        
        result.setdefault("required_skills", [])
        result.setdefault("experience_years", 1)
        result.setdefault("role_title", "Software Developer")
        result.setdefault("responsibilities", [])
        result.setdefault("company_keywords", [])
        
        return result

jd_analyzer_agent = JobDescriptionAnalyzerAgent()
