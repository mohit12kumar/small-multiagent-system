from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.database.connection import get_db
from backend.database.models import User, JobDescription
from backend.services.auth_service import get_current_user
from backend.agents.jd_agent import jd_analyzer_agent

router = APIRouter(prefix="/jd", tags=["Job Description Module"])

class JDUploadRequest(BaseModel):
    description: str

@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_jd(
    payload: JDUploadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not payload.description or len(payload.description.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description text is too short or empty."
        )
        
    # Analyze JD text with Agent 2
    analysis = jd_analyzer_agent.analyze_jd_text(payload.description)
    
    new_jd = JobDescription(
        user_id=current_user.id,
        description=payload.description,
        skills=analysis.get("required_skills", []),
        experience_years=analysis.get("experience_years", 0)
    )
    db.add(new_jd)
    db.commit()
    db.refresh(new_jd)
    
    return {
        "message": "Job description analyzed and saved successfully",
        "jd_id": new_jd.id,
        "required_skills": new_jd.skills,
        "experience_years": new_jd.experience_years,
        "role_title": analysis.get("role_title", "Software Developer"),
        "responsibilities": analysis.get("responsibilities", []),
        "company_keywords": analysis.get("company_keywords", [])
    }

@router.get("/")
def get_user_jds(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jds = db.query(JobDescription).filter(JobDescription.user_id == current_user.id).order_by(JobDescription.created_at.desc()).all()
    return jds
