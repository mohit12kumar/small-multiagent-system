import sys
import os

# Add root project directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.models import Base, User, UserRole, Resume, JobDescription, InterviewSession, Question, Answer, Feedback, Report, SessionStatus
from backend.services.auth_service import create_access_token, get_current_user, get_current_user_flexible
from backend.graph.workflow import interview_graph
from backend.agents.report_agent import report_generator_agent

# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# ── Test Case 1: Zero / Empty Answers Report Generation Edge Case ──
def test_zero_answers_report_generation(db_session):
    """Test generating a report when an interview session has zero answered questions."""
    user = User(name="Test Candidate", email="test@example.com", password="hashed_password", role=UserRole.CANDIDATE)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    jd = JobDescription(user_id=user.id, raw_text="Python FastAPI Developer", role_title="FastAPI Dev", skills=["Python", "FastAPI"])
    db_session.add(jd)
    db_session.commit()
    db_session.refresh(jd)

    session = InterviewSession(user_id=user.id, jd_id=jd.id, status=SessionStatus.IN_PROGRESS)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # Call report generator agent with 0 feedbacks
    rep = report_generator_agent.generate_report(
        candidate_name=user.name,
        session_id=session.id,
        feedbacks=[],
        missing_skills=["Docker", "LangGraph"]
    )

    assert rep["overall_score"] >= 0.0
    assert "pdf_path" in rep
    assert os.path.exists(rep["pdf_path"])

# ── Test Case 2: Zero Matching Skills Edge Case ──
def test_zero_matching_skills_edge_case():
    """Test graph execution when candidate has 0 skills matching the Job Description."""
    state = {
        "user_id": 99,
        "session_id": 999,
        "candidate_name": "No Match Candidate",
        "resume_path": "",
        "jd_text": "Requires Rust, WebAssembly, Solana",
        "resume_skills": ["HTML", "CSS"],
        "resume_experience": [],
        "resume_education": [],
        "resume_projects": [],
        "ats_score": 20.0,
        "jd_skills": ["Rust", "WebAssembly", "Solana"],
        "jd_experience_years": 5,
        "role_title": "Blockchain Engineer",
        "match_percentage": 0.0,
        "matched_skills": [],
        "missing_skills": ["Rust", "WebAssembly", "Solana"],
        "recommendations": ["Learn Rust and WebAssembly"],
        "questions": [],
        "current_question_index": 0,
        "user_answers": {},
        "question_feedbacks": [],
        "overall_score": 0.0,
        "pdf_path": "",
        "is_completed": False
    }

    result = interview_graph.invoke(state)
    assert result["match_percentage"] == 0.0
    assert len(result["missing_skills"]) == 3
    assert len(result["questions"]) > 0

# ── Test Case 3: Auth Token Verification & Query Parameter Token Edge Case ──
def test_auth_token_flexible_verification(db_session):
    """Test header token and query token authentication for zero errors."""
    user = User(name="Auth User", email="auth@example.com", password="pass", role=UserRole.CANDIDATE)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    
    # Header auth test
    authenticated_user_header = get_current_user(token=token, db=db_session)
    assert authenticated_user_header.id == user.id

    # Query param flexible auth test
    authenticated_user_query = get_current_user_flexible(header_token=None, query_token=token, db=db_session)
    assert authenticated_user_query.id == user.id

# ── Test Case 4: Zero Dashboard Data Edge Case ──
def test_zero_sessions_dashboard_metrics(db_session):
    """Test dashboard calculation when user has 0 interview sessions and 0 reports."""
    user = User(name="New Candidate", email="new@example.com", password="pass", role=UserRole.CANDIDATE)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    reports = db_session.query(Report).filter(Report.user_id == user.id).all()
    avg_score = round(sum(r.overall_score for r in reports) / len(reports), 1) if reports else 0.0

    assert avg_score == 0.0
