from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")

class TokenData(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone: Optional[str] = None
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    enabled: Optional[bool] = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    phone: Optional[str]
    is_confirmed: bool
    image_url: str
    enabled: bool
    created_at: datetime
    updated_at: datetime


class UserProfileCreate(BaseModel):
    user_id: UUID
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    timezone: str = "UTC"


class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    timezone: Optional[str] = None


class UserProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    display_name: Optional[str]
    avatar_url: Optional[str]
    timezone: str
    enabled: bool
    created_at: datetime
    updated_at: datetime
