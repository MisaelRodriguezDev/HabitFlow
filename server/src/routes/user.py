from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from src.core.database import get_session
from src.schemas.user import (
    UserCreate, UserUpdate, UserRead,
    UserProfileCreate, UserProfileUpdate, UserProfileRead
)
from src.services.user import UserService, UserProfileService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.create_user(user_data)


@router.get("", response_model=List[UserRead])
def get_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_all_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, user_data: UserUpdate, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    service = UserService(session)
    service.delete_user(user_id)


@router.post("/profiles", response_model=UserProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(profile_data: UserProfileCreate, session: Session = Depends(get_session)):
    service = UserProfileService(session)
    return service.create_profile(profile_data)


@router.get("/profiles/{profile_id}", response_model=UserProfileRead)
def get_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = UserProfileService(session)
    return service.get_profile(profile_id)


@router.get("/{user_id}/profile", response_model=UserProfileRead)
def get_profile_by_user(user_id: UUID, session: Session = Depends(get_session)):
    service = UserProfileService(session)
    profile = service.get_profile_by_user_id(user_id)
    if not profile:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/profiles/{profile_id}", response_model=UserProfileRead)
def update_profile(
    profile_id: UUID, 
    profile_data: UserProfileUpdate, 
    session: Session = Depends(get_session)
):
    service = UserProfileService(session)
    return service.update_profile(profile_id, profile_data)


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: UUID, session: Session = Depends(get_session)):
    service = UserProfileService(session)
    service.delete_profile(profile_id)
