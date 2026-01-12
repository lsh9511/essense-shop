from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class NotificationType(str, Enum):
    """알림 타입"""

    ORDER = "order"
    SHIPPING = "shipping"
    RESTOCK = "restock"
    COUPON = "coupon"
    REVIEW = "review"
    RETURN = "return"
    MARKETING = "marketing"


class Notification(Model):
    """알림 모델"""

    id = fields.IntField(pk=True)

    # 외래키: User와 관계 (NULL이면 어드민 알림)
    user: fields.ForeignKeyRelation["User"] | None = fields.ForeignKeyField(
        "models.User", related_name="notifications", on_delete=fields.OnDelete.CASCADE, null=True
    )

    # 알림 정보
    type = fields.CharEnumField(NotificationType)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    link_url = fields.CharField(max_length=500, null=True)

    # 읽음 여부
    is_read = fields.BooleanField(default=False)
    read_at = fields.DatetimeField(null=True)

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "notifications"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Notification {self.title}"
