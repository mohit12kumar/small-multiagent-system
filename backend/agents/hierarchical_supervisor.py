import os
from typing import Dict, Any, List
from backend.graph.state import NodeTarget, validate_state_prerequisites
from backend.schemas.agent_schemas import AgentResponseEnvelope

class InterviewSupervisorAgent:
    """Sub-Supervisor: Orchestrates technical and behavioral question generation."""
    def decide(self, state: Dict[str, Any]) -> str:
        if not state.get("questions"):
            return NodeTarget.GENERATE_QUESTIONS.value
        return NodeTarget.EVALUATE_ANSWERS.value

class CodingSupervisorAgent:
    """Sub-Supervisor: Manages DSA problem synthesis and execution sandbox validation."""
    def decide(self, state: Dict[str, Any]) -> str:
        return NodeTarget.GENERATE_QUESTIONS.value

class ReportSupervisorAgent:
    """Sub-Supervisor: Coordinates score aggregation, Critic evaluation, and PDF synthesis."""
    def decide(self, state: Dict[str, Any]) -> str:
        return NodeTarget.GENERATE_REPORT.value

class GlobalSupervisorAgent:
    """
    Master Hierarchical Supervisor Tree:
    - Global Supervisor delegates domain execution to sub-supervisors.
    - Emits structured AgentResponseEnvelope with confidence metrics and explainability reasoning.
    """
    def __init__(self):
        self.interview_sup = InterviewSupervisorAgent()
        self.coding_sup = CodingSupervisorAgent()
        self.report_sup = ReportSupervisorAgent()

    def determine_next_agent(self, state: Dict[str, Any]) -> AgentResponseEnvelope:
        has_resume = bool(state.get("resume_skills"))
        has_jd = bool(state.get("jd_skills"))
        has_match = state.get("match_percentage") is not None
        questions = state.get("questions", [])
        has_answers = bool(state.get("user_answers"))
        has_feedbacks = len(state.get("question_feedbacks", [])) > 0
        has_report = bool(state.get("pdf_path"))

        if not has_resume or not has_jd:
            raw_target = NodeTarget.PARSE_RESUME_AND_JD
            sub_sup = "Parsing Domain Supervisor"
            reason = "Resume experience and Job Description competencies require initial extraction."
        elif not has_match:
            raw_target = NodeTarget.MATCH_SKILLS
            sub_sup = "Skill Alignment Supervisor"
            reason = "Comparing candidate resume skills against target job description requirements."
        elif not questions:
            target_str = self.interview_sup.decide(state)
            raw_target = NodeTarget(target_str)
            sub_sup = "Interview Domain Supervisor"
            reason = "Delegating question synthesis to Interview Domain Supervisor."
        elif has_answers and not has_feedbacks:
            raw_target = NodeTarget.EVALUATE_ANSWERS
            sub_sup = "Evaluation Domain Supervisor"
            reason = "Evaluating submitted candidate answers on 5 scoring axes."
        elif not has_report:
            target_str = self.report_sup.decide(state)
            raw_target = NodeTarget(target_str)
            sub_sup = "Reporting Domain Supervisor"
            reason = "Delegating PDF report compilation to Report Domain Supervisor."
        else:
            raw_target = NodeTarget.FINISH
            sub_sup = "Master Global Supervisor"
            reason = "All multi-agent interview preparation stages complete."

        # Apply State Guard Validation
        validated_target = validate_state_prerequisites(state, raw_target)
        confidence = 0.98 if validated_target == raw_target else 0.85

        return AgentResponseEnvelope(
            output={"next_agent": validated_target.value, "sub_supervisor": sub_sup},
            confidence=confidence,
            reasoning=reason,
            needs_review=confidence < 0.90,
            agent_name="GlobalSupervisorAgent"
        )

global_supervisor = GlobalSupervisorAgent()
