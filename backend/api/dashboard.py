from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User, Resume, JobDescription, InterviewSession, Report
from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard Module"])

@router.get("/")
def get_candidate_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    latest_resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()
    latest_jd = db.query(JobDescription).filter(JobDescription.user_id == current_user.id).order_by(JobDescription.created_at.desc()).first()
    recent_sessions = db.query(InterviewSession).filter(InterviewSession.user_id == current_user.id).order_by(InterviewSession.date.desc()).limit(5).all()
    reports = db.query(Report).filter(Report.user_id == current_user.id).all()
    
    avg_score = round(sum(r.overall_score for r in reports) / len(reports), 1) if reports else 0.0
    
    return {
        "candidate_name": current_user.name,
        "resume_ats_score": latest_resume.ats_score if latest_resume else 0.0,
        "skill_match_percentage": 85.0,
        "overall_readiness_score": avg_score if avg_score > 0 else 78.5,
        "metrics": {
            "technical_score": 84.0,
            "coding_score": 80.0,
            "hr_score": 88.0,
            "communication_score": 86.0,
            "grammar_score": 92.0,
            "confidence_score": 78.0
        },
        "weak_skills": ["Docker", "Kubernetes", "GraphQL", "Redis"],
        "recommended_topics": [
            "Containerization & Microservices Deployment",
            "Async State Management in React",
            "SQL Query Indexing & Performance Tuning"
        ],
        "recent_sessions": [
            {
                "id": s.id,
                "date": s.date.strftime("%Y-%m-%d %H:%M"),
                "status": s.status.value,
                "report_id": db.query(Report.id).filter(Report.session_id == s.id).scalar()
            }
            for s in recent_sessions
        ]
    }
