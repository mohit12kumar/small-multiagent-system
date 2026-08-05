from typing import Dict
from backend.graph.state import InterviewState, NodeTarget, validate_state_prerequisites
from backend.agents.hierarchical_supervisor import global_supervisor

# Dictionary Mapping Router eliminating redundant if/elif chains
ROUTE_MAP: Dict[NodeTarget, str] = {
    NodeTarget.PARSE_RESUME_AND_JD: "parse_resume_and_jd_parallel",
    NodeTarget.PARSE_RESUME: "parse_resume_and_jd_parallel",
    NodeTarget.PARSE_JD: "parse_resume_and_jd_parallel",
    NodeTarget.MATCH_SKILLS: "match_skills",
    NodeTarget.GENERATE_QUESTIONS: "generate_questions",
    NodeTarget.EVALUATE_ANSWERS: "evaluate_answers",
    NodeTarget.GENERATE_REPORT: "generate_report",
    NodeTarget.CRITIC_REFLECT: "generate_report",
    NodeTarget.FINISH: "FINISH"
}

def route_next_step(state: InterviewState) -> str:
    """
    Clean Dictionary-Mapped Router:
    - Uses ROUTE_MAP dictionary for O(1) node routing.
    - Validates state prerequisites to prevent skipping required steps.
    """
    envelope = global_supervisor.determine_next_agent(state)
    target_str = envelope.output.get("next_agent", NodeTarget.GENERATE_REPORT.value)
    
    try:
        raw_enum = NodeTarget(target_str)
    except ValueError:
        raw_enum = NodeTarget.GENERATE_REPORT

    # State Guard Validation
    validated_enum = validate_state_prerequisites(state, raw_enum)
    
    return ROUTE_MAP.get(validated_enum, "generate_report")
