from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.student


class LoginRequest(BaseModel):
    email: EmailStr
    password: str