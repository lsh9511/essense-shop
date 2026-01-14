from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from datetime import datetime
from app.schemas import PaymentResponse
from app.models import (
    User,
    Order,
    Payment,
    OrderStatus,
    PaymentMethod,
    PaymentStatus,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/{order_id}/complete", response_model=PaymentResponse)
async def complete_payment(
    order_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    결제 완료 처리 (STUB)

    실제 PG 연동 전까지는 자동으로 결제 승인 처리됩니다.
    - 자신의 주문만 결제 가능
    - PENDING 상태의 주문만 결제 가능
    """
    # 주문 조회
    order = await Order.filter(id=order_id, user=current_user).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="주문을 찾을 수 없습니다."
        )

    # 결제 가능 상태 확인
    if order.order_status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"결제할 수 없는 주문 상태입니다. (현재: {order.order_status})",
        )

    # 이미 결제된 주문인지 확인
    existing_payment = await Payment.get_or_none(order=order)
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 결제된 주문입니다.",
        )

    # Payment 생성 (STUB - 자동 승인)
    payment = await Payment.create(
        order=order,
        payment_method=PaymentMethod.CARD,  # STUB: 기본값으로 카드 결제
        payment_status=PaymentStatus.COMPLETED,
        amount=order.final_price,
        paid_at=datetime.now(),
        payment_key=f"STUB-{order.order_number}",  # STUB 결제 키
        pg_transaction_id=f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
    )

    # 주문 상태 변경
    order.order_status = OrderStatus.PAID
    await order.save()

    return {
        "id": payment.id,
        "order_id": order.id,
        "payment_method": payment.payment_method,
        "payment_status": payment.payment_status,
        "amount": payment.amount,
        "paid_at": payment.paid_at,
        "payment_key": payment.payment_key,
        "pg_transaction_id": payment.pg_transaction_id,
        "created_at": payment.created_at,
    }


@router.get("/{order_id}", response_model=PaymentResponse)
async def get_payment(
    order_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    결제 정보 조회

    - 자신의 주문 결제 정보만 조회 가능
    """
    # 주문 조회
    order = await Order.filter(id=order_id, user=current_user).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="주문을 찾을 수 없습니다."
        )

    # 결제 정보 조회
    payment = await Payment.get_or_none(order=order)

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="결제 정보를 찾을 수 없습니다."
        )

    return {
        "id": payment.id,
        "order_id": order.id,
        "payment_method": payment.payment_method,
        "payment_status": payment.payment_status,
        "amount": payment.amount,
        "paid_at": payment.paid_at,
        "payment_key": payment.payment_key,
        "pg_transaction_id": payment.pg_transaction_id,
        "created_at": payment.created_at,
    }
