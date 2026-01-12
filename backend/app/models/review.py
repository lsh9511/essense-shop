from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .product import Product
    from .order_item import OrderItem


class SizeSatisfaction(str, Enum):
    """사이즈 만족도"""

    SMALL = "small"
    PERFECT = "perfect"
    LARGE = "large"


class Review(Model):
    """리뷰 모델"""

    id = fields.IntField(pk=True)

    # 외래키: User, Product, OrderItem
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="reviews", on_delete=fields.OnDelete.CASCADE
    )
    product: fields.ForeignKeyRelation["Product"] = fields.ForeignKeyField(
        "models.Product", related_name="reviews", on_delete=fields.OnDelete.CASCADE
    )
    order_item: fields.OneToOneRelation["OrderItem"] = fields.OneToOneField(
        "models.OrderItem", related_name="review", on_delete=fields.OnDelete.CASCADE, unique=True
    )

    # 리뷰 내용
    rating = fields.IntField()
    content = fields.TextField()

    # 작성자 정보 (선택)
    user_height = fields.IntField(null=True)
    user_weight = fields.IntField(null=True)
    purchase_size = fields.CharField(max_length=20, null=True)
    size_satisfaction = fields.CharEnumField(SizeSatisfaction, null=True)

    # 노출 여부
    is_visible = fields.BooleanField(default=False)

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "reviews"

    def __str__(self) -> str:
        return f"Review {self.id}"


class ReviewImage(Model):
    """리뷰 이미지 모델"""

    id = fields.IntField(pk=True)

    # 외래키: Review와 관계
    review: fields.ForeignKeyRelation[Review] = fields.ForeignKeyField(
        "models.Review", related_name="images", on_delete=fields.OnDelete.CASCADE
    )

    image_url = fields.CharField(max_length=500)
    display_order = fields.IntField(default=0)

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "review_images"
        ordering = ["display_order"]

    def __str__(self) -> str:
        return f"ReviewImage {self.id}"
