from backend.graph.state import InterviewState
from backend.agents.resume_agent import resume_analyzer_agent
from backend.agents.jd_agent import jd_analyzer_agent
from backend.agents.skill_match_agent import skill_matching_agent
from backend.agents.question_agent import question_generator_agent
from backend.agents.coding_agent import coding_agent
from backend.agents.hr_agent import hr_agent
from backend.agents.feedback_agent import feedback_agent
from backend.agents.report_agent import report_generator_agent

def parse_resume_node(state: InterviewState) -> InterviewState:
    analysis = resume_analyzer_agent.analyze_resume_file(state["resume_path"])
    state["resume_skills"] = analysis.get("skills", [])
    state["resume_experience"] = analysis.get("experience", [])
    state["resume_education"] = analysis.get("education", [])
    state["resume_projects"] = analysis.get("projects", [])
    state["ats_score"] = analysis.get("ats_score", 75.0)
    return state

def parse_jd_node(state: InterviewState) -> InterviewState:
    analysis = jd_analyzer_agent.analyze_jd_text(state["jd_text"])
    state["jd_skills"] = analysis.get("required_skills", [])
    state["jd_experience_years"] = analysis.get("experience_years", 0)
    state["role_title"] = analysis.get("role_title", "Software Developer")
    return state

def match_skills_node(state: InterviewState) -> InterviewState:
    res = skill_matching_agent.compare_skills(state["resume_skills"], state["jd_skills"])
    state["match_percentage"] = res["match_percentage"]
    state["matched_skills"] = res["matched_skills"]
    state["missing_skills"] = res["missing_skills"]
    state["recommendations"] = res["recommendations"]
    return state

def generate_questions_node(state: InterviewState) -> InterviewState:
    accumulated_prev = list(state.get("previous_questions", []))
    role = state.get("role_title", "Software Developer")
    
    tech_qs = question_generator_agent.generate_questions(
        role_title=role,
        matched_skills=state.get("matched_skills", []),
        missing_skills=state.get("missing_skills", []),
        previous_questions=accumulated_prev
    )
    for q in tech_qs:
        if q.get("question_text"):
            accumulated_prev.append(q["question_text"])

    code_q = coding_agent.generate_coding_question(domain=f"{role} & Algorithms", previous_questions=accumulated_prev)
    if code_q.get("question_text"):
        accumulated_prev.append(code_q["question_text"])

    hr_qs = hr_agent.generate_hr_questions(previous_questions=accumulated_prev)
    
    all_questions = tech_qs + [code_q] + hr_qs
    state["questions"] = all_questions
    state["current_question_index"] = 0
    return state

def generate_report_node(state: InterviewState) -> InterviewState:
    res = report_generator_agent.generate_report(
        candidate_name=state.get("candidate_name", "Candidate"),
        session_id=state.get("session_id", 1),
        feedbacks=state.get("question_feedbacks", []),
        missing_skills=state.get("missing_skills", [])
    )
    state["overall_score"] = res["overall_score"]
    state["pdf_path"] = res["pdf_path"]
    state["is_completed"] = True
    return state
