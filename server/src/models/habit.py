from datetime import date
from typing import Optional, List
from uuid import UUID
from sqlmodel import Field, Relationship
from .common import Base


class Habit(Base, table=True):
    """Habit table representation in the database."""
    
    __tablename__ = "tbl_habits"
    
    user_id: UUID = Field(foreign_key="tbl_users.id", index=True)
    title: str = Field(max_length=200)
    category: str = Field(max_length=100)
    goal_type: str = Field(max_length=50)
    goal_value: int
    
    user: Optional["User"] = Relationship(back_populates="habits")
    habit_logs: List["HabitLog"] = Relationship(back_populates="habit", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    challenge_habits: List["ChallengeHabit"] = Relationship(back_populates="habit")


class HabitLog(Base, table=True):
    """Habit log table representation in the database."""
    
    __tablename__ = "tbl_habit_logs"
    
    habit_id: UUID = Field(foreign_key="tbl_habits.id", index=True)
    user_id: UUID = Field(foreign_key="tbl_users.id", index=True)
    log_date: date
    progress_value: int
    status: str = Field(max_length=50)
    
    habit: Optional["Habit"] = Relationship(back_populates="habit_logs")
    user: Optional["User"] = Relationship(back_populates="habit_logs")
