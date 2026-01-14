from pydantic import BaseModel
from datetime import datetime


class WishlistCreate(BaseModel):
    """찜 추가 요청"""

    product_id: int


class WishlistResponse(BaseModel):
    """찜 응답"""

    id: int
    user_id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True
