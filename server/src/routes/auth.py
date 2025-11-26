from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from src.core.database import get_session
from src.services.user import UserService
from pydantic import BaseModel, EmailStr

class LoginData(BaseModel):
    email: EmailStr
    password: str

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginData, session: Session = Depends(get_session)):
    service = UserService(session)
    return service.login(data.email, data.password)