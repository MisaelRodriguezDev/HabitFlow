from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class HabitCreate(BaseModel):
    user_id: UUID
    title: str
    category: str
    goal_type: str
    goal_value: int


class HabitUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    goal_type: Optional[str] = None
    goal_value: Optional[int] = None
    enabled: Optional[bool] = None


class HabitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    title: str
    category: str
    goal_type: str
    goal_value: int
    enabled: bool
    created_at: datetime
    updated_at: datetime


class HabitLogCreate(BaseModel):
    habit_id: UUID
    user_id: UUID
    log_date: date
    progress_value: int
    status: str


class HabitLogUpdate(BaseModel):
    progress_value: Optional[int] = None
    status: Optional[str] = None


class HabitLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    habit_id: UUID
    user_id: UUID
    log_date: date
    progress_value: int
    status: str
    enabled: bool
    created_at: datetime
    updated_at: datetime
