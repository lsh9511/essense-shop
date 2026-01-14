from pydantic import BaseModel, Field
from datetime import datetime
from app.models import SizeSatisfaction


class ReviewCreate(BaseModel):
    """리뷰 생성 요청"""

    order_item_id: int
    rating: int = Field(..., ge=1, le=5)
    content: str = Field(..., min_length=10, max_length=1000)

    # 선택 정보
    user_height: int | None = Field(None, ge=100, le=250)
    user_weight: int | None = Field(None, ge=30, le=200)
    purchase_size: str | None = Field(None, max_length=20)
    size_satisfaction: SizeSatisfaction | None = None


class ReviewUpdate(BaseModel):
    """리뷰 수정 요청"""

    rating: int | None = Field(None, ge=1, le=5)
    content: str | None = Field(None, min_length=10, max_length=1000)

    user_height: int | None = Field(None, ge=100, le=250)
    user_weight: int | None = Field(None, ge=30, le=200)
    purchase_size: str | None = Field(None, max_length=20)
    size_satisfaction: SizeSatisfaction | None = None


class ReviewImageResponse(BaseModel):
    """리뷰 이미지 응답"""

    id: int
    image_url: str
    display_order: int

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    """리뷰 응답"""

    id: int
    user_id: int
    product_id: int
    order_item_id: int

    rating: int
    content: str

    user_height: int | None
    user_weight: int | None
    purchase_size: str | None
    size_satisfaction: SizeSatisfaction | None

    is_visible: bool

    # 이미지 (나중에 구현)
    # images: list[ReviewImageResponse]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    """리뷰 목록 응답 (간단 버전)"""

    id: int
    user_id: int
    rating: int
    content: str
    is_visible: bool
    created_at: datetime

    class Config:
        from_attributes = True
