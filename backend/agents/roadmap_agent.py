import os
from typing import Dict, Any, List
from backend.services.llm_factory import query_llm_json_sync

class LearningRoadmapAgent:
    """
    30-60-90 Day Personal Skill Growth Roadmap Agent:
    Synthesizes actionable, week-by-week study milestones targeting identified skill gaps.
    """
    def __init__(self):
        self.system_prompt = """You are a Principal Engineering Career Mentor.
Given missing candidate skills and target job role, synthesize a structured 30-60-90 Day Personalized Learning Roadmap.

Return ONLY JSON:
{
  "day_30_focus": "Foundational Skill Gaps & Core DSA",
  "day_30_milestones": ["Master System Design fundamentals", "Build 5 LeetCode Medium graph problems"],
  "day_60_focus": "Advanced System Design & Distributed Services",
  "day_60_milestones": ["Implement Saga distributed transaction pattern", "Deploy Redis cache layer"],
  "day_90_focus": "Mock Interview Mastery & Offer Readiness",
  "day_90_milestones": ["Complete 3 live mock interviews under timed constraints", "Optimize resume STAR stories"],
  "recommended_courses": ["Designing Data-Intensive Applications", "Grokking System Design"]
}
"""

    def generate_roadmap(self, role_title: str, missing_skills: List[str]) -> Dict[str, Any]:
        prompt = f"TARGET ROLE: {role_title}\nMISSING SKILLS: {', '.join(missing_skills) if missing_skills else 'None'}"
        return query_llm_json_sync(self.system_prompt, prompt)

roadmap_agent = LearningRoadmapAgent()
