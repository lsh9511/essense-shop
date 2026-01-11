from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class OrderStatus(str, Enum):
    """주문 상태"""

    PENDING = "pending"
    PAID = "paid"
    PREPARING = "preparing"
    SHIPPING = "shipping"
    DELIVERED = "delivered"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class ShippingStatus(str, Enum):
    """배송 상태"""

    PENDING = "pending"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


class Order(Model):
    """주문 모델"""

    id = fields.IntField(pk=True)
    order_number = fields.CharField(max_length=50, unique=True, index=True)

    # 외래키: User
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="orders", on_delete=fields.RESTRICT
    )
    # 수령인 정보
    recipient_name = fields.CharField(max_length=50)
    recipient_phone = fields.CharField(max_length=20)
    # 배송 주소
    postal_code = fields.CharField(max_length=10)
    address_line1 = fields.CharField(max_length=255)
    address_line2 = fields.CharField(max_length=255, null=True)
    delivery_memo = fields.TextField(null=True)
    # 가격 정보
    total_product_price = fields.IntField()
    shipping_fee = fields.IntField(default=3000)
    discount_amount = fields.IntField(default=0)
    final_price = fields.IntField()
    # 주문 상태
    order_status = fields.CharEnumField(OrderStatus, default=OrderStatus.PENDING, index=True)
    shipping_status = fields.CharEnumField(ShippingStatus, null=True)
    # 배송 정보
    courier_company = fields.CharField(max_length=50, null=True)
    tracking_number = fields.CharField(max_length=50, null=True)
    # 타임스탬프
    shipped_at = fields.DatetimeField(null=True)
    delivered_at = fields.DatetimeField(null=True)
    confirmed_at = fields.DatetimeField(null=True)
    cancelled_at = fields.DatetimeField(null=True)
    cancel_reason = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "orders"

    def __str__(self) -> str:
        return self.order_number
