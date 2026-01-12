from pydantic import BaseModel, Field
from datetime import datetime


class CartItemCreate(BaseModel):
    """장바구니에 상품 추가 요청"""

    product_option_id: int
    quantity: int = Field(default=1, ge=1)  # 최소 1개 이상


class CartItemUpdate(BaseModel):
    """장바구느 수량 변경 요청"""

    quantity: int = Field(..., ge=1)


class CartItemResponse(BaseModel):
    """장바구니 아이템 응답"""

    id: int
    product_option_id: int
    quantity: int

    # 상품 정보 (nested)
    product_name: str
    brand_name: str
    size: str
    color: str
    price: int
    thumbnail_url: str | None

    created_at: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """장바구니 전체 응답"""

    items: list[CartItemResponse]

    # 요약 정보
    total_product_price: int
    shipping_fee: int
    final_price: int
