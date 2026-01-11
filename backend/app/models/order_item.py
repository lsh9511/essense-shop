from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order
    from .product_option import ProductOption


class OrderItem(Model):
    """주문 상품 모델"""

    id = fields.IntField(pk=True)
    # 외래키
    order: fields.ForeignKeyRelation["Order"] = fields.ForeignKeyField(
        "models.Order", related_name="items", on_delete=fields.OnDelete.CASCADE, index=True
    )
    product_option: fields.ForeignKeyRelation["ProductOption"] = fields.ForeignKeyField(
        "models.ProductOption", related_name="order_items", on_delete=fields.OnDelete.RESTRICT
    )
    # 주문 시점 스냅샷 ( 상품 정보가 변경되어도 주문 당시 정보 유지 )
    product_name = fields.CharField(max_length=255)
    brand_name = fields.CharField(max_length=100)
    size = fields.CharField(max_length=20)
    color = fields.CharField(max_length=50)
    price = fields.IntField()

    # 수량 및 금액
    quantity = fields.IntField(default=1)
    subtotal = fields.IntField()

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "order_items"

    def __str__(self) -> str:
        return f"{self.product_name} x {self.quantity}"
