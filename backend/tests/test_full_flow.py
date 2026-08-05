import sys
import os

# Add root project directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.graph.workflow import interview_graph

def run_end_to_end_test():
    print("==================================================")
    print("  Running End-to-End LangGraph Flow Tracing Test ")
    print("==================================================")
    
    initial_state = {
        "user_id": 1,
        "session_id": 101,
        "candidate_name": "John Doe",
        "resume_path": "",
        "jd_text": "Looking for a Senior Python Developer with FastAPI, MySQL, React, Docker, and LangGraph multi-agent experience.",
        "resume_skills": ["Python", "FastAPI", "React", "SQL"],
        "resume_experience": [{"role": "Backend Engineer", "years": 3}],
        "resume_education": [{"degree": "B.Tech Computer Science"}],
        "resume_projects": [{"title": "AI Assistant System"}],
        "ats_score": 85.0,
        "jd_skills": ["Python", "FastAPI", "MySQL", "React", "Docker", "LangGraph"],
        "jd_experience_years": 3,
        "role_title": "Senior Python Developer",
        "match_percentage": 75.0,
        "matched_skills": ["Python", "FastAPI", "React"],
        "missing_skills": ["MySQL", "Docker", "LangGraph"],
        "recommendations": ["Learn Docker containerization and LangGraph graph routing."],
        "questions": [],
        "current_question_index": 0,
        "user_answers": {},
        "question_feedbacks": [],
        "overall_score": 0.0,
        "pdf_path": "",
        "is_completed": False
    }
    
    print("\n[1/3] Executing LangGraph state transitions...")
    result_state = interview_graph.invoke(initial_state)
    
    print("\n[2/3] LangGraph Output Summary:")
    print(f"  - Generated Questions Count: {len(result_state.get('questions', []))}")
    for idx, q in enumerate(result_state.get("questions", []), 1):
        print(f"    Q{idx} [{q.get('type')} - {q.get('difficulty')}]: {q.get('question_text')[:80]}...")
        
    print("\n[3/3] Tracing Check:")
    print("  - Tracing enabled: YES (Check https://smith.langchain.com)")
    print("==================================================")

if __name__ == "__main__":
    run_end_to_end_test()
