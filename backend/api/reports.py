from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from backend.database.connection import get_db
from backend.database.models import (
    User, Resume, JobDescription, InterviewSession, Question, Answer, Feedback, Report, SessionStatus
)
from backend.services.auth_service import get_current_user, get_current_user_flexible
from backend.agents.report_agent import report_generator_agent

router = APIRouter(prefix="/report", tags=["Report Module"])

@router.get("/{session_id}")
def generate_and_get_report(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")
        
    # Gather questions & answers & feedback
    questions = db.query(Question).filter(Question.session_id == session_id).all()
    feedbacks_list = []
    
    for q in questions:
        ans = db.query(Answer).filter(Answer.question_id == q.id).first()
        if ans:
            fb = db.query(Feedback).filter(Feedback.answer_id == ans.id).first()
            if fb:
                feedbacks_list.append({
                    "grammar_score": fb.grammar_score,
                    "technical_score": fb.technical_score,
                    "communication_score": fb.communication_score,
                    "confidence_score": fb.confidence_score,
                    "completeness_score": fb.completeness_score,
                    "overall_score": fb.overall_score
                })
                
    # Calculate missing skills dynamically from JD and user Resume
    jd = db.query(JobDescription).filter(JobDescription.id == session.jd_id).first()
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.id.desc()).first()
    
    jd_skills = jd.skills if (jd and jd.skills) else []
    resume_skills = resume.skills if (resume and resume.skills) else []
    missing_skills = list(set(jd_skills) - set(resume_skills))
    if not missing_skills:
        missing_skills = ["Advanced Architecture", "System Design"]

    candidate_name = getattr(current_user, 'name', None) or getattr(current_user, 'email', None) or "Candidate"

    rep_obj = report_generator_agent.generate_report(
        candidate_name=candidate_name,
        session_id=session.id,
        feedbacks=feedbacks_list,
        missing_skills=missing_skills
    )
    
    # Save Report record in DB
    existing_rep = db.query(Report).filter(Report.session_id == session.id).first()
    if existing_rep:
        report_record = existing_rep
        report_record.overall_score = rep_obj["overall_score"]
        report_record.pdf_path = rep_obj["pdf_path"]
    else:
        report_record = Report(
            user_id=current_user.id,
            session_id=session.id,
            overall_score=rep_obj["overall_score"],
            pdf_path=rep_obj["pdf_path"],
            skill_gap_summary=rep_obj["skill_gap_summary"],
            improvement_plan=rep_obj["improvement_plan"]
        )
        db.add(report_record)
        
    session.status = SessionStatus.COMPLETED
    db.commit()
    db.refresh(report_record)
    
    return {
        "report_id": report_record.id,
        "session_id": session.id,
        "overall_score": report_record.overall_score,
        "pdf_download_url": f"/api/v1/report/{report_record.id}/pdf",
        "skill_gap_summary": report_record.skill_gap_summary,
        "improvement_plan": report_record.improvement_plan
    }

@router.get("/{report_id}/pdf")
def download_report_pdf(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_flexible)
):
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == current_user.id).first()
    if not report or not os.path.exists(report.pdf_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report PDF file not found")
        
    return FileResponse(
        path=report.pdf_path,
        filename=os.path.basename(report.pdf_path),
        media_type="application/pdf"
    )
