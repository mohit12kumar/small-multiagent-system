import os
from typing import Dict, Any, List
from backend.services.llm_factory import llm_factory

class SupervisorAgent:
    """
    Supervisor Agent (Master Orchestrator):
    - Directs dynamic multi-agent execution flow.
    - Decides next agent route based on state, candidate profile, and Critic Agent evaluations.
    - Manages parallel execution nodes and reflection self-correction loops.
    """
    def __init__(self):
        self.system_prompt = """You are the Principal Supervisor AI Orchestrator for an Enterprise Multi-Agent Interview System.
Your job is to examine the current candidate state and decide the NEXT execution step.

Available Next Agents:
- "parse_resume_and_jd": If resume or JD text is missing initial extraction.
- "match_skills": If parsing is done but skill gap matching is missing.
- "question_agent": To generate technical questions.
- "coding_agent": To generate DSA/Coding challenge.
- "hr_agent": To generate behavioral STAR questions.
- "critic_agent": To review and validate generated questions or candidate answer evaluations.
- "human_review": If critical approval queue status is pending.
- "generate_report": When all steps are complete and verified.
- "FINISH": When session is complete.

Return ONLY JSON:
{
  "next_agent": "question_agent",
  "reasoning": "Skills matched successfully. Generating questions next.",
  "confidence_score": 0.95
}
"""

    def determine_next_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        has_resume = bool(state.get("resume_skills"))
        has_jd = bool(state.get("jd_skills"))
        has_match = bool(state.get("match_percentage"))
        has_questions = len(state.get("questions", [])) >= 3
        has_feedbacks = len(state.get("question_feedbacks", [])) > 0
        has_report = bool(state.get("pdf_path"))

        if not has_resume or not has_jd:
            return {"next_agent": "parse_resume_and_jd", "reasoning": "Resume or JD requires extraction."}
        if not has_match:
            return {"next_agent": "match_skills", "reasoning": "Executing skill match agent."}
        if not has_questions:
            return {"next_agent": "question_agent", "reasoning": "Synthesizing interview questions."}
        if not has_feedbacks and not state.get("is_completed"):
            return {"next_agent": "evaluate_answers", "reasoning": "Awaiting answer evaluations."}
        if not has_report:
            return {"next_agent": "generate_report", "reasoning": "Synthesizing final report."}
            
        return {"next_agent": "FINISH", "reasoning": "All multi-agent stages complete."}

supervisor_agent = SupervisorAgent()
