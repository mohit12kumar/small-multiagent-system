from backend.graph.state import InterviewState, NodeTarget, validate_state_prerequisites
from backend.agents.supervisor_agent import supervisor_agent

def route_next_step(state: InterviewState) -> str:
    """
    Typed Dynamic Router:
    - Uses NodeTarget Enum instead of string literals.
    - Validates state prerequisites to prevent skipping required steps.
    """
    decision = supervisor_agent.determine_next_agent(state)
    target_enum = decision.get("enum_target", NodeTarget.GENERATE_REPORT)
    
    # State Guard Validation
    validated_enum = validate_state_prerequisites(state, target_enum)
    
    if validated_enum in [NodeTarget.PARSE_RESUME_AND_JD, NodeTarget.PARSE_RESUME, NodeTarget.PARSE_JD]:
        return NodeTarget.PARSE_RESUME.value
    elif validated_enum == NodeTarget.MATCH_SKILLS:
        return NodeTarget.MATCH_SKILLS.value
    elif validated_enum == NodeTarget.GENERATE_QUESTIONS:
        return NodeTarget.GENERATE_QUESTIONS.value
    elif validated_enum == NodeTarget.EVALUATE_ANSWERS:
        return NodeTarget.EVALUATE_ANSWERS.value
    elif validated_enum in [NodeTarget.GENERATE_REPORT, NodeTarget.CRITIC_REFLECT]:
        return NodeTarget.GENERATE_REPORT.value
    elif validated_enum == NodeTarget.FINISH:
        return NodeTarget.FINISH.value

    return NodeTarget.GENERATE_REPORT.value
