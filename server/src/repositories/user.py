from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from src.models.user import User, UserProfile
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)
    
    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()


class UserProfileRepository(BaseRepository[UserProfile]):
    def __init__(self, session: Session):
        super().__init__(UserProfile, session)
    
    def get_by_user_id(self, user_id: UUID) -> Optional[UserProfile]:
        statement = select(UserProfile).where(UserProfile.user_id == user_id)
        return self.session.exec(statement).first()
