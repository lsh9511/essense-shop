from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class ReturnType(str, Enum):
    """반품 타입"""

    RETURN = "return"  # 반품
    EXCHANGE = "exchange"  # 교환


class ReturnStatus(str, Enum):
    """반품 상태"""

    REQUESTED = "requested"  # 신청
    APPROVED = "approved"  # 승인
    COLLECTING = "collecting"  # 수거 중
    COLLECTED = "collected"  # 수거 완료
    COMPLETED = "completed"  # 처리 완료
    REJECTED = "rejected"  # 거부


class ReturnRequest(Model):
    """교환 반품 모델"""

    id = fields.IntField(pk=True)

    # 외래키: Order와 관계
    order: fields.ForeignKeyRelation["Order"] = fields.ForeignKeyField(
        "models.Order", related_name="returns", on_delete=fields.CASCADE
    )

    # 반품 정보
    return_type = fields.CharEnumField(ReturnType)
    reason = fields.CharField(max_length=100)  # 사유 (단순변심, 사이즈 불만족, 불량 등)
    detailed_reason = fields.TextField(null=True)  # 상세 사유

    # 이미지 URL (JSON 배열)
    image_urls: list[str] | None = fields.JSONField(null=True)

    # 상태
    status = fields.CharEnumField(ReturnStatus, default=ReturnStatus.REQUESTED)

    # 환불 금액
    refund_amount = fields.IntField(null=True)

    # 수거 정보
    courier_company = fields.CharField(max_length=50, null=True)
    tracking_number = fields.CharField(max_length=50, null=True)

    # 타임스탬프
    approved_at = fields.DatetimeField(null=True)
    collected_at = fields.DatetimeField(null=True)
    completed_at = fields.DatetimeField(null=True)

    # 거부 사유
    rejected_reason = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "returns"

    def __str__(self) -> str:
        return f"Return {self.id}"
