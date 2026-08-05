from typing import Optional, List
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.database.models import InterviewSession, Question, Answer, Feedback, Report

class SessionRepository(BaseRepository[InterviewSession]):
    """
    Session Repository: Handles specialized data access queries for Interview Sessions.
    """
    def __init__(self, db: Session):
        super().__init__(InterviewSession, db)

    def get_user_sessions(self, user_id: int) -> List[InterviewSession]:
        return self.db.query(InterviewSession).filter(InterviewSession.user_id == user_id).all()

    def get_session_with_questions(self, session_id: int) -> Optional[InterviewSession]:
        return self.db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
