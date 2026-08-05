import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from backend.config import settings
from backend.database.connection import get_db
from backend.database.models import User, Resume
from backend.services.auth_service import get_current_user
from backend.agents.resume_agent import resume_analyzer_agent

router = APIRouter(prefix="/resume", tags=["Resume Module"])

@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate file extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Only .pdf, .docx, and .txt files are allowed."
        )
    
    # Save file to disk
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(settings.RESUME_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Analyze resume with Agent 1
    analysis = resume_analyzer_agent.analyze_resume_file(file_path)
    
    # Save to database
    new_resume = Resume(
        user_id=current_user.id,
        resume_path=file_path,
        skills=analysis.get("skills", []),
        education=analysis.get("education", []),
        experience=analysis.get("experience", []),
        projects=analysis.get("projects", []),
        ats_score=analysis.get("ats_score", 75.0)
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    return {
        "message": "Resume uploaded and analyzed successfully",
        "resume_id": new_resume.id,
        "ats_score": new_resume.ats_score,
        "skills": new_resume.skills,
        "experience": new_resume.experience,
        "education": new_resume.education,
        "projects": new_resume.projects
    }

@router.get("/")
def get_user_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()
    return resumes

@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
        
    if os.path.exists(resume.resume_path):
        try:
            os.remove(resume.resume_path)
        except Exception:
            pass
            
    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted successfully"}
