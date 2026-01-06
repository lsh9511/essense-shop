from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class ProductOption(Model):
    """상품 옵션 모델 (사이즈/컬러)"""

    id = fields.IntField(pk=True)

    # 외래키: Product와 관계
    product: fields.ForeignKeyRelation["Product"] = fields.ForeignKeyField(
        "models.Product", related_name="options", on_delete=fields.CASCADE
    )
    size = fields.CharField(max_length=20)
    color = fields.CharField(max_length=50)
    color_code = fields.CharField(max_length=7, null=True)
    additional_price = fields.IntField(default=0)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "product_options"
        unique_together = (("product", "size", "color"),)

    def __str__(self):
        return f"{self.size} / {self.color}"
