from tortoise import fields
from tortoise.models import Model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Address(Model):
    """배송지 모델"""

    id = fields.IntField(pk=True)

    # 외래키: User와 관계
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="addresses", on_delete=fields.OnDelete.CASCADE
    )
    # 배송지 정보
    recipient_name = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=20)
    postal_code = fields.CharField(max_length=10)
    address_line1 = fields.CharField(max_length=255)
    address_line2 = fields.CharField(max_length=255, null=True)

    # 기본 배송지 여부
    is_default = fields.BooleanField(default=False)

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "addresses"

    def __str__(self) -> str:
        return f"Address {self.recipient_name}"