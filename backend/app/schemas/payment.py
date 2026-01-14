from pydantic import BaseModel
from datetime import datetime
from app.models import PaymentMethod, PaymentStatus


class PaymentResponse(BaseModel):
    """결제 응답"""

    id: int
    order_id: int
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    amount: int
    paid_at: datetime | None
    payment_key: str | None
    pg_transaction_id: str | None

    created_at: datetime

    class Config:
        from_attributes = True
