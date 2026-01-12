from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product_option import ProductOption


class Inventory(Model):
    """재고 모델"""

    id = fields.IntField(pk=True)

    # 외래키: ProductOption과 1대1 관계
    product_option: fields.OneToOneRelation["ProductOption"] = fields.OneToOneField(
        "models.ProductOption", related_name="inventory", on_delete=fields.OnDelete.CASCADE
    )
    quantity = fields.IntField(default=0)
    safe_stock = fields.IntField(default=5)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "inventory"

    def __str__(self) -> str:
        return f"Stock: {self.quantity}"

    @property
    def is_low_stock(self) -> bool:
        """재고 부족 여부"""
        return self.quantity <= self.safe_stock

    @property
    def is_out_of_stock(self) -> bool:
        """품절 여부"""
        return self.quantity == 0
