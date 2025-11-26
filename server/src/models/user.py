from sqlmodel import Field, Relationship
from sqlalchemy import event, inspect
from typing import Optional, List
from uuid import UUID
from .common import Base
from src.core.security import hash_password

IMAGE = "https://i.pinimg.com/550x/a8/0e/36/a80e3690318c08114011145fdcfa3ddb.jpg"

class User(Base, table=True):
    """User table representation in the database.

    Args:
        Base (Base): Common base for all tables
        table (bool, optional): SQLModel option to indicate it's a database table. True by default.
    """

    __tablename__ = "tbl_users"
    
    first_name: str = Field(nullable=False, min_length=2, max_length=100)
    last_name: str = Field(nullable=False, min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=50, index=True, unique=True)
    email: str = Field(nullable=False, index=True, unique=True, max_length=255)
    phone: Optional[str] = Field(default=None, min_length=10, max_length=13)
    password: str = Field(nullable=False, min_length=8, max_length=255)
    is_confirmed: bool = Field(default=False)
    image_url: str = Field(default=IMAGE, nullable=False, max_length=255)
    
    profile: Optional["UserProfile"] = Relationship(back_populates="user")
    habits: List["Habit"] = Relationship(back_populates="user")
    habit_logs: List["HabitLog"] = Relationship(back_populates="user")
    created_challenges: List["Challenge"] = Relationship(back_populates="creator")
    challenge_participations: List["ChallengeParticipant"] = Relationship(back_populates="user")


class UserProfile(Base, table=True):
    """User profile table representation in the database."""
    
    __tablename__ = "tbl_user_profiles"
    
    user_id: UUID = Field(foreign_key="tbl_users.id", unique=True, index=True)
    display_name: Optional[str] = Field(default=None, max_length=100)
    avatar_url: Optional[str] = Field(default=None, max_length=255)
    timezone: str = Field(default="UTC", max_length=50)
    
    user: Optional["User"] = Relationship(back_populates="profile")


@event.listens_for(User, "before_insert")
def hash_password_on_insert(mapper, connection, target: User):
    """Hash password before user creation"""
    target.password = hash_password(target.password)

@event.listens_for(User, "before_update")
def hash_password_on_update(mapper, connection, target: User):
    """Hash password only if changed during updates"""
    insp = inspect(target)
    if insp.attrs.password.history.has_changes():
        target.password = hash_password(target.password)
