from backend.graph.state import InterviewState
from backend.agents.supervisor_agent import supervisor_agent

def route_next_step(state: InterviewState) -> str:
    """
    Dynamic Router: Consults SupervisorAgent to determine the next graph node.
    """
    sup_decision = supervisor_agent.determine_next_agent(state)
    target = sup_decision.get("next_agent", "generate_report")
    
    if target in ["parse_resume_and_jd", "parse_resume"]:
        return "parse_resume"
    elif target == "match_skills":
        return "match_skills"
    elif target == "question_agent":
        return "generate_questions"
    elif target == "evaluate_answers":
        return "evaluate_answers"
    elif target in ["generate_report", "critic_agent"]:
        return "generate_report"
    elif target == "FINISH":
        return "FINISH"
    
    return "generate_report"
