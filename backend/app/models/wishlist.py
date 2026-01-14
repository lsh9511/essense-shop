from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .product import Product


class Wishlist(Model):
    """위시리스트 모델"""

    id = fields.IntField(pk=True)

    # 외래키: User와 관계
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="wishlists", on_delete=fields.OnDelete.CASCADE
    )
    user_id: int
    # 외래키: Product와 관계
    product: fields.ForeignKeyRelation["Product"] = fields.ForeignKeyField(
        "models.Product", related_name="wishlists", on_delete=fields.OnDelete.CASCADE
    )
    product_id: int
    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "wishlists"
        # unique_together: 같은 사용자가 같은 상품을 중복으로 찜할 수 없음
        unique_together = (("user", "product"),)

    def __str__(self) -> str:
        return f"Wishlist: {self.id}"
