from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class BrandCreate(BaseModel):
    """브랜드 생성 요청"""

    name: str = Field(..., min_length=1, max_length=100)
    name_en: str | None = Field(None, max_length=100)
    logo_url: str | None = Field(None, max_length=500)
    description: str | None = None
    story: str | None = None
    instagram: str | None = Field(None, max_length=255)
    contact_name: str | None = Field(None, max_length=50)
    contact_phone: str | None = Field(None, max_length=20)
    contact_email: EmailStr | None = None
    commission_rate: Decimal = Field(default=Decimal("0.00"),ge=0, le=100)


class BrandUpdate(BaseModel):
    """브랜드 업데이트"""

    name: str | None = Field(None, min_length=1, max_length=100)
    name_en: str | None = Field(None, max_length=100)
    logo_url: str | None = Field(None, max_length=500)
    description: str | None = None
    story: str | None = None
    instagram: str | None = Field(None, max_length=255)
    is_active: bool | None = None
    contact_name: str | None = Field(None, max_length=50)
    contact_phone: str | None = Field(None, max_length=20)
    contact_email: EmailStr | None = None
    commission_rate: Decimal | None = Field(None, ge=0, le=100)


class BrandResponse(BaseModel):
    """브랜드 응답"""

    id: int
    name: str
    name_en: str | None
    logo_url: str | None
    description: str | None
    story: str | None
    instagram: str | None
    contact_name: str | None
    contact_phone: str | None
    contact_email : str | None
    commission_rate: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
