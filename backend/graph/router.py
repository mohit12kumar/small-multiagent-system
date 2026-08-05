from backend.graph.state import InterviewState

def route_next_step(state: InterviewState) -> str:
    """
    Determines whether there are remaining questions to evaluate or to proceed to report generation.
    """
    current_idx = state.get("current_question_index", 0)
    total_qs = len(state.get("questions", []))
    
    if current_idx < total_qs:
        return "continue_interview"
    else:
        return "generate_report"
