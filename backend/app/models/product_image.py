from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class ProductImage(Model):
    """상품 이미지 모델"""

    id = fields.IntField(pk=True)

    # 외래키: Product와 관계
    product: fields.ForeignKeyRelation["Product"] = fields.ForeignKeyField(
        "models.Product", related_name="images", on_delete=fields.OnDelete.CASCADE
    )
    image_url = fields.CharField(max_length=500)
    display_order = fields.IntField(default=0)
    is_thumbnail = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "product_images"
        ordering = ["display_order"]

    def __str__(self) -> str:
        return f"Image {self.display_order}"
