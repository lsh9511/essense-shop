from pydantic import BaseModel, Field
from datetime import datetime
from app.models import OrderStatus, ShippingStatus


class OrderItemCreate(BaseModel):
    """주문 상품 생성 요청"""

    product_option_id: int
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    """주문 생성 요청"""

    # 주문 상품들
    items: list[OrderItemCreate] = Field(..., min_length=1)

    # 배송지 정보
    recipient_name: str = Field(..., min_length=1, max_length=50)
    recipient_phone: str = Field(..., pattern=r"^\d{3}-\d{3,4}-\d{4}$")
    postal_code: str = Field(..., max_length=10)
    address_line1: str = Field(..., max_length=255)
    address_line2: str | None = Field(None, max_length=255)
    delivery_memo: str | None = None

    # 쿠폰 (선택)
    coupon_id: int | None = None


class OrderItemResponse(BaseModel):
    """주문 상품 응답"""

    id: int
    product_name: str
    brand_name: str
    size: str
    color: str
    price: int
    quantity: int
    subtotal: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """주문 응답"""

    id: int
    order_number: str
    order_status: OrderStatus
    shipping_status: ShippingStatus | None

    # 배송지 정보
    recipient_name: str
    recipient_phone: str
    postal_code: str
    address_line1: str
    address_line2: str | None
    delivery_memo: str | None

    # 금액 정보
    total_product_price: int
    shipping_fee: int
    discount_amount: int
    final_price: int

    # 주문 상품
    items: list[OrderItemResponse]

    # 배송 정보
    courier_company: str | None
    tracking_number: str | None
    shipped_at: datetime | None
    delivered_at: datetime | None

    created_at: datetime

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """주문 목록 응답 (간단 버전)"""

    id: int
    order_number: str
    order_status: OrderStatus
    shipping_status: ShippingStatus | None

    # 요약 정보
    items_summary: str  # "상품명 외 2건"
    final_price: int

    created_at: datetime

    class Config:
        from_attributes = True
