from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from backend.database.connection import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    """
    Generic Repository Pattern Base Class:
    Decouples database CRUD operations from FastAPI controllers and services.
    """
    def __init__(self, model_class: Type[T], db_session: Session):
        self.model_class = model_class
        self.db = db_session

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.db.query(self.model_class).filter(self.model_class.id == entity_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model_class).offset(skip).limit(limit).all()

    def create(self, entity: T) -> T:
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False
