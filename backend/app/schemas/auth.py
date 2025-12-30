from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.models import UserRole, Gender


class UserRegister(BaseModel):
    """회원가입 요청"""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., pattern=r"^\d{3}-\d{3,4}-\d{4}$")
    gender: Gender | None = None
    marketing_agree: bool = False


class UserLogin(BaseModel):
    """로그인 요청"""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    uuid: str
    email: str
    name: str
    phone: str
    gender: Gender | None
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Tortoise ORM 모델을 Pydantic으로 변환


class TokenResponse(BaseModel):
    """토큰 응답"""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
