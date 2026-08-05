from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class InterviewState(TypedDict):
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
    
    # User Submissions & Feedback Agent
    user_answers: Dict[int, str]
    question_feedbacks: List[Dict[str, Any]]
    
    # Final Report Output
    overall_score: float
    pdf_path: str
    is_completed: bool
