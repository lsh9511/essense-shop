from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .order import Order


class DiscountType(str, Enum):
    """할인 타입"""

    FIXED = "fixed"  # 정액 할인 (예: 5000원)
    PERCENT = "percent"  # 정률 할인 (예 : 10%)


class Coupon(Model):
    """쿠폰 모델"""

    id = fields.IntField(pk=True)

    # 쿠폰 정보
    code = fields.CharField(max_length=50, unique=True)
    name = fields.CharField(max_length=100)

    # 할인 정보
    discount_type = fields.CharEnumField(DiscountType)
    discount_value = fields.IntField()  # 정액: 원 단위, 정률 : % 단위

    # 사용 조건
    min_order_amount = fields.IntField(default=0)  # 최소 주문 금액
    max_discount_amount = fields.IntField(null=True)  # 최대 할인 금액 (정률일 때)

    # 발급 수량
    quantity = fields.IntField(null=True)
    issued_count = fields.IntField(default=0)

    # 사용 기간
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()

    # 활성 상태
    is_active = fields.BooleanField(default=True)

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "coupons"

    def __str__(self) -> str:
        return f"Coupon {self.code}"


class UserCoupon(Model):
    """사용자 쿠폰 모델"""

    id = fields.IntField(pk=True)

    # 외래키: User, Coupon
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="User_coupons", on_delete=fields.OnDelete.CASCADE
    )
    coupon: fields.ForeignKeyRelation[Coupon] = fields.ForeignKeyField(
        "models.Coupon", related_name="User_coupons", on_delete=fields.OnDelete.CASCADE
    )

    # 사용 여부
    is_used = fields.BooleanField(default=False)
    used_at = fields.DatetimeField(null=True)

    # 사용한 주문
    order: fields.ForeignKeyRelation["Order"] | None = fields.ForeignKeyField(
        "models.Order", related_name="used_coupons", on_delete=fields.OnDelete.SET_NULL, null=True
    )

    # 발급일시
    issued_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_coupons"
        # 같은 사용자가 같은 쿠폰을 중복으로 받을 수 없음 (미사용만)
        # 하지만 Tortoise ORM은 조건부 unique를 직접 지원 안해서 API 레벨에서 체크 필요

    def __str__(self) -> str:
        return f"UserCoupon {self.id}"
