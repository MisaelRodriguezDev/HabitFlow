from typing import Optional, List
from uuid import UUID
from sqlmodel import Session
from src.models.user import User, UserProfile
from src.schemas.user import UserCreate, UserUpdate, UserProfileCreate, UserProfileUpdate
from src.repositories.user import UserRepository, UserProfileRepository
from fastapi import HTTPException, status
from src.core.security import verify_password

class UserService:
    def __init__(self, session: Session):
        self.repository = UserRepository(session)


    def login(self, email: str, password: str):
        user = self.repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario no encontrado"
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Credenciales incorrectas"
            )
        return user
    
    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = self.repository.get_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        user = User(**user_data.model_dump())
        return self.repository.create(user)
    
    def get_user(self, user_id: UUID) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.repository.get_all(skip=skip, limit=limit)
    
    def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        user = self.get_user(user_id)
        return self.repository.update(user, user_data.model_dump(exclude_unset=True))
    
    def delete_user(self, user_id: UUID) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user)


class UserProfileService:
    def __init__(self, session: Session):
        self.repository = UserProfileRepository(session)
    
    def create_profile(self, profile_data: UserProfileCreate) -> UserProfile:
        existing_profile = self.repository.get_by_user_id(profile_data.user_id)
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile already exists for this user"
            )
        
        profile = UserProfile(**profile_data.model_dump())
        return self.repository.create(profile)
    
    def get_profile(self, profile_id: UUID) -> UserProfile:
        profile = self.repository.get_by_id(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        return profile
    
    def get_profile_by_user_id(self, user_id: UUID) -> Optional[UserProfile]:
        return self.repository.get_by_user_id(user_id)
    
    def update_profile(self, profile_id: UUID, profile_data: UserProfileUpdate) -> UserProfile:
        profile = self.get_profile(profile_id)
        return self.repository.update(profile, profile_data.model_dump(exclude_unset=True))
    
    def delete_profile(self, profile_id: UUID) -> None:
        profile = self.get_profile(profile_id)
        self.repository.delete(profile)
