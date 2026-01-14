from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order


class PaymentMethod(str, Enum):
    """결제 수단"""

    CARD = "card"
    TRANSFER = "transfer"
    TOSS = "toss"
    NAVERPAY = "naverpay"
    KAKAOPAY = "kakaopay"


class PaymentStatus(str, Enum):
    """결제 상태"""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"


class Payment(Model):
    """결제 모델"""

    id = fields.IntField(pk=True)

    # 외래키: Order와 1:1 관계
    order: fields.OneToOneRelation["Order"] = fields.OneToOneField(
        "models.Order", related_name="payment", on_delete=fields.OnDelete.RESTRICT
    )

    # 결제 정보
    payment_key = fields.CharField(max_length=255, unique=True)
    payment_method = fields.CharEnumField(PaymentMethod)
    amount = fields.IntField()
    pg_transaction_id = fields.CharField(max_length=255, null=True)

    # 상태
    payment_status = fields.CharEnumField(PaymentStatus, default=PaymentStatus.PENDING)

    # 타임 스탬프
    paid_at = fields.DatetimeField(null=True)
    cancelled_at = fields.DatetimeField(null=True)
    refunded_at = fields.DatetimeField(null=True)

    # 실패 사유
    failure_reason = fields.TextField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "payments"

    def __str__(self) -> str:
        return f"Payment {self.payment_key}"
