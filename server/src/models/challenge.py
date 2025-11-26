from datetime import date, datetime, timezone
from typing import Optional, List
from uuid import UUID
from sqlmodel import Field, Relationship
from .common import Base


class Challenge(Base, table=True):
    """Challenge table representation in the database."""
    
    __tablename__ = "tbl_challenges"
    
    created_by: UUID = Field(foreign_key="tbl_users.id", index=True)
    title: str = Field(max_length=200)
    start_date: date
    end_date: date
    is_public: bool = Field(default=True)
    status: str = Field(default="active", max_length=50)
    
    creator: Optional["User"] = Relationship(back_populates="created_challenges")
    participants: List["ChallengeParticipant"] = Relationship(back_populates="challenge")
    challenge_habits: List["ChallengeHabit"] = Relationship(back_populates="challenge")


class ChallengeParticipant(Base, table=True):
    """Challenge participant table representation in the database."""
    
    __tablename__ = "tbl_challenge_participants"
    
    challenge_id: UUID = Field(foreign_key="tbl_challenges.id", index=True)
    user_id: UUID = Field(foreign_key="tbl_users.id", index=True)
    status: str = Field(default="active", max_length=50)
    current_score: int = Field(default=0)
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    challenge: Optional["Challenge"] = Relationship(back_populates="participants")
    user: Optional["User"] = Relationship(back_populates="challenge_participations")


class ChallengeHabit(Base, table=True):
    """Challenge habit table representation in the database."""
    
    __tablename__ = "tbl_challenge_habits"
    
    challenge_id: UUID = Field(foreign_key="tbl_challenges.id", index=True)
    habit_id: UUID = Field(foreign_key="tbl_habits.id", index=True)
    points_per_completion: int = Field(default=1)
    
    challenge: Optional["Challenge"] = Relationship(back_populates="challenge_habits")
    habit: Optional["Habit"] = Relationship(back_populates="challenge_habits")
