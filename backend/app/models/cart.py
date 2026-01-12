from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .product_option import ProductOption


class Cart(Model):
    """장바구니 모델"""

    id = fields.IntField(pk=True)

    # 외래키 : User와 관계 (1:1)
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "model.User", related_name="cart", on_delete=fields.OnDelete.CASCADE, unique=True
    )

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "carts"

    def __str__(self) -> str:
        return f"Cart {self.id}"


class CartItem(Model):
    """장바구니 아이템 모델"""

    id = fields.IntField(pk=True)

    # 외래키 : Cart와 관계
    cart: fields.ForeignKeyRelation[Cart] = fields.ForeignKeyField(
        "models.Cart", related_name="items", on_delete=fields.OnDelete.CASCADE
    )

    # 외래키 : ProductOption과 관계
    product_option: fields.ForeignKeyRelation["ProductOption"] = fields.ForeignKeyField(
        "models.ProductOption", related_name="cart_items", on_delete=fields.OnDelete.CASCADE
    )

    quantity = fields.IntField(default=1)

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "cart_items"
        # unique_together: 같은 장바구니에 같은 옵션은 중복 불가
        unique_together = (("cart", "product_option"),)

    def __str__(self) -> str:
        return f"CartItem {self.id}"
