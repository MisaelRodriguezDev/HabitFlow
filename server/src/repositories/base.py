from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from sqlmodel import Session, select
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session
    
    def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
    
    def get_by_id(self, id: UUID) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())
    
    def update(self, db_obj: ModelType, update_data: dict) -> ModelType:
        for field, value in update_data.items():
            if value is not None:
                setattr(db_obj, field, value)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def delete(self, db_obj: ModelType) -> None:
        self.session.delete(db_obj)
        self.session.commit()
