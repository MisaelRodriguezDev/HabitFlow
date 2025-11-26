from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ChallengeCreate(BaseModel):
    created_by: UUID
    title: str
    start_date: date
    end_date: date
    is_public: bool = False


class ChallengeUpdate(BaseModel):
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_public: Optional[bool] = None
    status: Optional[str] = None
    enabled: Optional[bool] = None


class ChallengeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_by: UUID
    title: str
    start_date: date
    end_date: date
    is_public: bool
    status: str
    enabled: bool
    created_at: datetime
    updated_at: datetime


class ChallengeParticipantCreate(BaseModel):
    challenge_id: UUID
    user_id: UUID


class ChallengeParticipantUpdate(BaseModel):
    status: Optional[str] = None
    current_score: Optional[int] = None


class ChallengeParticipantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    challenge_id: UUID
    user_id: UUID
    status: str
    current_score: int
    joined_at: datetime
    enabled: bool
    created_at: datetime
    updated_at: datetime


class ChallengeHabitCreate(BaseModel):
    challenge_id: UUID
    habit_id: UUID
    points_per_completion: int = 1


class ChallengeHabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    challenge_id: UUID
    habit_id: UUID
    points_per_completion: int
    enabled: bool
    created_at: datetime
    updated_at: datetime
