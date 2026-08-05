from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.database.connection import get_db
from backend.database.models import (
    User, Resume, JobDescription, InterviewSession, Question, Answer, Feedback, SessionStatus
)
from backend.services.auth_service import get_current_user
from backend.agents.question_agent import question_generator_agent
from backend.agents.coding_agent import coding_agent
from backend.agents.hr_agent import hr_agent
from backend.agents.feedback_agent import feedback_agent

router = APIRouter(prefix="/interview", tags=["Interview Module"])

class StartInterviewRequest(BaseModel):
    resume_id: int
    jd_id: int

class SubmitAnswerRequest(BaseModel):
    question_id: int
    answer_text: str

@router.post("/start", status_code=status.HTTP_201_CREATED)
def start_interview_session(
    payload: StartInterviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
        
    jd = db.query(JobDescription).filter(JobDescription.id == payload.jd_id, JobDescription.user_id == current_user.id).first()
    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")
        
    session = InterviewSession(
        user_id=current_user.id,
        jd_id=jd.id,
        status=SessionStatus.IN_PROGRESS
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    import time
    import random
    
    # Fetch all historical question texts for current user to avoid duplicates
    previous_q_objs = (
        db.query(Question)
        .join(InterviewSession, Question.session_id == InterviewSession.id)
        .filter(InterviewSession.user_id == current_user.id)
        .all()
    )
    previous_questions = [pq.question_text for pq in previous_q_objs if pq.question_text]

    role_title = getattr(jd, 'role_title', None) or "Software Engineer"
    accumulated_prev = list(previous_questions)
    tech_qs = question_generator_agent.generate_questions(role_title, matched, missing, session_seed, previous_questions=accumulated_prev)
    for q in tech_qs:
        if q.get("question_text"):
            accumulated_prev.append(q["question_text"])

    code_q = coding_agent.generate_coding_question(domain=f"{role_title} & DSA", seed=session_seed, previous_questions=accumulated_prev)
    if code_q.get("question_text"):
        accumulated_prev.append(code_q["question_text"])

    hr_qs = hr_agent.generate_hr_questions(seed=session_seed, previous_questions=accumulated_prev)
    
    all_qs = tech_qs + [code_q] + hr_qs
    db_questions = []
    
    for q in all_qs:
        q_obj = Question(
            session_id=session.id,
            question_text=q.get("question_text", "Explain your software project experience."),
            difficulty=q.get("difficulty", "medium"),
            type=q.get("type", "technical")
        )
        db.add(q_obj)
        db_questions.append(q_obj)
        
    db.commit()
    for q_obj in db_questions:
        db.refresh(q_obj)
    
    questions_data = [
        {
            "id": q.id,
            "question_text": q.question_text,
            "difficulty": q.difficulty.value if hasattr(q.difficulty, 'value') else str(q.difficulty),
            "type": q.type.value if hasattr(q.type, 'value') else str(q.type)
        }
        for q in db_questions
    ]
    
    return {
        "session_id": session.id,
        "status": session.status.value if hasattr(session.status, 'value') else str(session.status),
        "total_questions": len(questions_data),
        "questions": questions_data,
        "first_question": questions_data[0] if questions_data else None
    }

@router.post("/answer")
def submit_answer(
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        
    # Check if answer exists
    existing_answer = db.query(Answer).filter(Answer.question_id == question.id).first()
    if existing_answer:
        answer_obj = existing_answer
        answer_obj.answer_text = payload.answer_text
    else:
        answer_obj = Answer(question_id=question.id, answer_text=payload.answer_text)
        db.add(answer_obj)
        
    db.commit()
    db.refresh(answer_obj)
    
    # Evaluate with Feedback Agent
    eval_res = feedback_agent.evaluate_answer(question.question_text, payload.answer_text)
    
    existing_fb = db.query(Feedback).filter(Feedback.answer_id == answer_obj.id).first()
    if existing_fb:
        fb_obj = existing_fb
        fb_obj.grammar_score = eval_res["grammar_score"]
        fb_obj.technical_score = eval_res["technical_score"]
        fb_obj.communication_score = eval_res["communication_score"]
        fb_obj.confidence_score = eval_res["confidence_score"]
        fb_obj.completeness_score = eval_res["completeness_score"]
        fb_obj.overall_score = eval_res["overall_score"]
        fb_obj.comments = eval_res["comments"]
    else:
        fb_obj = Feedback(
            answer_id=answer_obj.id,
            grammar_score=eval_res["grammar_score"],
            technical_score=eval_res["technical_score"],
            communication_score=eval_res["communication_score"],
            confidence_score=eval_res["confidence_score"],
            completeness_score=eval_res["completeness_score"],
            overall_score=eval_res["overall_score"],
            comments=eval_res["comments"]
        )
        db.add(fb_obj)
        
    db.commit()
    db.refresh(fb_obj)
    
    return {
        "message": "Answer evaluated successfully",
        "answer_id": answer_obj.id,
        "feedback": {
            "grammar_score": fb_obj.grammar_score,
            "technical_score": fb_obj.technical_score,
            "communication_score": fb_obj.communication_score,
            "confidence_score": fb_obj.confidence_score,
            "completeness_score": fb_obj.completeness_score,
            "overall_score": fb_obj.overall_score,
            "comments": fb_obj.comments
        }
    }
