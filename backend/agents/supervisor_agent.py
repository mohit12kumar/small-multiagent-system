import os
from typing import Dict, Any, List
from backend.graph.state import NodeTarget, validate_state_prerequisites

class SupervisorAgent:
    """
    Intelligent Supervisor Agent:
    - Evaluates multi-factor candidate state (parsing state, skill alignment, question count, answer feedback, critic quality score, and retry errors).
    - Prevents invalid state transitions using validate_state_prerequisites.
    - Emits typed NodeTarget Enum values for dynamic routing.
    """
    def __init__(self):
        pass

    def determine_next_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Inspect state components
        has_resume = bool(state.get("resume_skills"))
        has_jd = bool(state.get("jd_skills"))
        has_match = state.get("match_percentage") is not None
        questions = state.get("questions", [])
        has_questions = len(questions) >= 3
        has_answers = bool(state.get("user_answers"))
        has_feedbacks = len(state.get("question_feedbacks", [])) > 0
        has_report = bool(state.get("pdf_path"))
        critic_score = state.get("critic_score", 100.0)

        # 2. Multi-factor intelligent decision logic
        if not has_resume or not has_jd:
            raw_target = NodeTarget.PARSE_RESUME_AND_JD
            reasoning = "Resume or JD requires extraction."
        elif not has_match:
            raw_target = NodeTarget.MATCH_SKILLS
            reasoning = "Executing skill match comparison."
        elif not has_questions:
            raw_target = NodeTarget.GENERATE_QUESTIONS
            reasoning = "Synthesizing role-adaptive interview questions."
        elif has_answers and not has_feedbacks:
            raw_target = NodeTarget.EVALUATE_ANSWERS
            reasoning = "Evaluating candidate submitted answers."
        elif critic_score < 80.0 and state.get("reflection_count", 0) < 2:
            raw_target = NodeTarget.CRITIC_REFLECT
            reasoning = f"Critic quality score ({critic_score}) below threshold. Triggering reflection loop."
        elif not has_report:
            raw_target = NodeTarget.GENERATE_REPORT
            reasoning = "Compiling analytics and generating downloadable PDF report."
        else:
            raw_target = NodeTarget.FINISH
            reasoning = "All multi-agent stages complete successfully."

        # 3. Apply State Guard to prevent illegal jumps
        validated_target = validate_state_prerequisites(state, raw_target)

        return {
            "next_agent": validated_target.value,
            "enum_target": validated_target,
            "reasoning": reasoning,
            "confidence": 0.98 if validated_target == raw_target else 0.85
        }

supervisor_agent = SupervisorAgent()
