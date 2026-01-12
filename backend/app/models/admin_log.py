from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class AdminAction(str, Enum):
    """어드민 작업"""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"


class AdminLog(Model):
    """어드민 로그 모델"""

    id = fields.IntField(pk=True)

    # 외래키: User(Admin)와 관계
    admin: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="admin_logs", on_delete=fields.OnDelete.CASCADE
    )

    # 작업 정보
    action = fields.CharEnumField(AdminAction)
    target_type = fields.CharField(max_length=50)
    target_id = fields.IntField(null=True)
    description = fields.TextField(null=True)

    # IP 주소
    ip_address = fields.CharField(max_length=45, null=True)  # IPv6 대응 (최대 45자)

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admin_logs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"AdminLog {self.action} {self.target_type}"
