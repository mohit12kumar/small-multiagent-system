import enum
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class NodeTarget(str, enum.Enum):
    PARSE_RESUME_AND_JD = "parse_resume_and_jd"
    PARSE_RESUME = "parse_resume"
    PARSE_JD = "parse_jd"
    MATCH_SKILLS = "match_skills"
    GENERATE_QUESTIONS = "generate_questions"
    EVALUATE_ANSWERS = "evaluate_answers"
    GENERATE_REPORT = "generate_report"
    CRITIC_REFLECT = "critic_agent"
    FINISH = "FINISH"

class InterviewState(TypedDict, total=False):
    user_id: int
    session_id: int
    candidate_name: str
    resume_path: str
    jd_text: str
    
    # Resume Analyzer Agent Outputs
    resume_skills: List[str]
    resume_experience: List[Dict[str, Any]]
    resume_education: List[Dict[str, Any]]
    resume_projects: List[Dict[str, Any]]
    ats_score: float
    
    # JD Analyzer Agent Outputs
    jd_skills: List[str]
    jd_experience_years: int
    role_title: str
    
    # Skill Match Agent Outputs
    match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    
    # Question Generator Outputs
    questions: List[Dict[str, Any]]
    current_question_index: int
    previous_questions: List[str]
    
    # User Submissions & Feedback Agent
    user_answers: Dict[Any, str]
    question_feedbacks: List[Dict[str, Any]]
    
    # Supervisor & Reflection Telemetry
    supervisor_next: str
    critic_score: float
    reflection_count: int
    errors: List[str]
    
    # Final Report Output
    overall_score: float
    pdf_path: str
    is_completed: bool

def validate_state_prerequisites(state: InterviewState, target_node: NodeTarget) -> NodeTarget:
    """
    State Guard: Validates that state prerequisites are met before allowing a node transition.
    If prerequisites are missing, automatically reroutes to the missing prerequisite node.
    """
    has_resume = bool(state.get("resume_skills"))
    has_jd = bool(state.get("jd_skills"))
    has_match = bool(state.get("match_percentage") is not None)
    has_questions = len(state.get("questions", [])) > 0
    has_feedbacks = len(state.get("question_feedbacks", [])) > 0

    if target_node == NodeTarget.MATCH_SKILLS and (not has_resume or not has_jd):
        print(f"[State Guard]: Missing resume or JD data. Redirecting target from MATCH_SKILLS to PARSE_RESUME_AND_JD.")
        return NodeTarget.PARSE_RESUME_AND_JD

    if target_node == NodeTarget.GENERATE_QUESTIONS and not has_match:
        print(f"[State Guard]: Missing skill match calculation. Redirecting target to MATCH_SKILLS.")
        return NodeTarget.MATCH_SKILLS

    if target_node == NodeTarget.EVALUATE_ANSWERS and not has_questions:
        print(f"[State Guard]: Missing interview questions. Redirecting target to GENERATE_QUESTIONS.")
        return NodeTarget.GENERATE_QUESTIONS

    if target_node == NodeTarget.GENERATE_REPORT and not has_feedbacks and not state.get("user_answers"):
        print(f"[State Guard]: Missing candidate answers/feedbacks. Rerouting to EVALUATE_ANSWERS.")
        return NodeTarget.EVALUATE_ANSWERS

    return target_node
