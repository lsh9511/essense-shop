from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Any
from datetime import datetime
from app.schemas import OrderCreate, OrderResponse, OrderListResponse
from app.models import (
    User,
    Order,
    OrderItem,
    ProductOption,
    Inventory,
    OrderStatus,
    ShippingStatus,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    주문 생성

    - 재고 확인
    - 금액 계산
    - OrderItem 스냅샷 저장
    - 재고 차감
    """
    # 주문 상품 검증 및 데이터 수집
    order_items_data: list[dict[str, Any]] = []
    total_product_price = 0

    for item_data in order_data.items:
        # ProductOption 조회
        option = await ProductOption.get_or_none(id=item_data.product_option_id).prefetch_related(
            "product__brand"
        )

        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"상품 옵션 {item_data.product_option_id}을(를) 찾을 수 없습니다.",
            )

        product = option.product
        brand = product.brand

        # 재고 확인
        inventory = await Inventory.get_or_none(product_option=option)
        if not inventory or inventory.quantity < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{product.name} 상품의 재고가 부족합니다. (재고: {inventory.quantity if inventory else 0}개)",
            )

        # 가격 계산 (할인가 우선)
        price = product.sale_price if product.sale_price else product.price
        subtotal = price * item_data.quantity
        total_product_price += subtotal

        # OrderItem 데이터 준비 (스냅샷)
        order_items_data.append(
            {
                "product_option_id": option.id,
                "product_name": product.name,
                "brand_name": brand.name,
                "size": option.size,
                "color": option.color,
                "price": price,
                "quantity": item_data.quantity,
                "subtotal": subtotal,
                "inventory": inventory,  # 나중에 재고 차감용
            }
        )

    # 배송비 계산 (50,000원 이상 무료)
    shipping_fee = 0 if total_product_price >= 50000 else 3000

    # 쿠폰 할인 (TODO: 나중에 구현)
    discount_amount = 0

    # 최종 금액
    final_price = total_product_price + shipping_fee - discount_amount

    # 주문번호 생성 (ORD-YYYYMMDD-NNNN)
    today = datetime.now().strftime("%Y%m%d")
    # 오늘 주문 개수 조회
    today_order_count = await Order.filter(order_number__startswith=f"ORD-{today}").count()
    order_number = f"ORD-{today}-{today_order_count + 1:04d}"

    # 주문 생성
    order = await Order.create(
        order_number=order_number,
        user=current_user,
        recipient_name=order_data.recipient_name,
        recipient_phone=order_data.recipient_phone,
        postal_code=order_data.postal_code,
        address_line1=order_data.address_line1,
        address_line2=order_data.address_line2,
        delivery_memo=order_data.delivery_memo,
        total_product_price=total_product_price,
        shipping_fee=shipping_fee,
        discount_amount=discount_amount,
        final_price=final_price,
        order_status=OrderStatus.PENDING,
        shipping_status=ShippingStatus.PENDING,
    )

    # OrderItem 생성 및 재고 차감
    created_items = []
    for item_dict in order_items_data:
        # OrderItem 생성
        order_item = await OrderItem.create(
            order=order,
            product_option_id=item_dict["product_option_id"],
            product_name=item_dict["product_name"],
            brand_name=item_dict["brand_name"],
            size=item_dict["size"],
            color=item_dict["color"],
            price=item_dict["price"],
            quantity=item_dict["quantity"],
            subtotal=item_dict["subtotal"],
        )

        # 재고 차감
        inventory = item_dict["inventory"]
        inventory.quantity -= item_dict["quantity"]
        await inventory.save()

        created_items.append(order_item)

    # 응답 데이터 구성
    items_response = [
        {
            "id": item.id,
            "product_name": item.product_name,
            "brand_name": item.brand_name,
            "size": item.size,
            "color": item.color,
            "price": item.price,
            "quantity": item.quantity,
            "subtotal": item.subtotal,
        }
        for item in created_items
    ]

    return {
        "id": order.id,
        "order_number": order.order_number,
        "order_status": order.order_status,
        "shipping_status": order.shipping_status,
        "recipient_name": order.recipient_name,
        "recipient_phone": order.recipient_phone,
        "postal_code": order.postal_code,
        "address_line1": order.address_line1,
        "address_line2": order.address_line2,
        "delivery_memo": order.delivery_memo,
        "total_product_price": order.total_product_price,
        "shipping_fee": order.shipping_fee,
        "discount_amount": order.discount_amount,
        "final_price": order.final_price,
        "items": items_response,
        "courier_company": order.courier_company,
        "tracking_number": order.tracking_number,
        "shipped_at": order.shipped_at,
        "delivered_at": order.delivered_at,
        "created_at": order.created_at,
    }


@router.get("", response_model=list[OrderListResponse])
async def get_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = 1,
    limit: int = 10,
    status: OrderStatus | None = None,
) -> list[dict]:
    """
    내 주문 목록 조회

    - 페이지네이션
    - 상태별 필터
    """
    # 쿼리 빌드
    query = Order.filter(user=current_user)

    if status:
        query = query.filter(order_status=status)

    # 정렬 및 페이지네이션
    query = query.order_by("-created_at")
    skip = (page - 1) * limit
    orders = await query.offset(skip).limit(limit).prefetch_related("items")

    # 응답 데이터 구성
    result = []
    for order in orders:
        items = await order.items.all()

        # 요약 정보 생성
        if len(items) == 0:
            items_summary = "상품 없음"
        elif len(items) == 1:
            items_summary = items[0].product_name
        else:
            items_summary = f"{items[0].product_name} 외 {len(items) - 1}건"

        result.append(
            {
                "id": order.id,
                "order_number": order.order_number,
                "order_status": order.order_status,
                "shipping_status": order.shipping_status,
                "items_summary": items_summary,
                "final_price": order.final_price,
                "created_at": order.created_at,
            }
        )

    return result


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    주문 상세 조회

    - 자신의 주문만 조회 가능
    """
    # 주문 조회
    order = await Order.filter(id=order_id, user=current_user).prefetch_related("items").first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="주문을 찾을 수 없습니다."
        )

    # OrderItem 조회
    items = await order.items.all()

    items_response = [
        {
            "id": item.id,
            "product_name": item.product_name,
            "brand_name": item.brand_name,
            "size": item.size,
            "color": item.color,
            "price": item.price,
            "quantity": item.quantity,
            "subtotal": item.subtotal,
        }
        for item in items
    ]

    return {
        "id": order.id,
        "order_number": order.order_number,
        "order_status": order.order_status,
        "shipping_status": order.shipping_status,
        "recipient_name": order.recipient_name,
        "recipient_phone": order.recipient_phone,
        "postal_code": order.postal_code,
        "address_line1": order.address_line1,
        "address_line2": order.address_line2,
        "delivery_memo": order.delivery_memo,
        "total_product_price": order.total_product_price,
        "shipping_fee": order.shipping_fee,
        "discount_amount": order.discount_amount,
        "final_price": order.final_price,
        "items": items_response,
        "courier_company": order.courier_company,
        "tracking_number": order.tracking_number,
        "shipped_at": order.shipped_at,
        "delivered_at": order.delivered_at,
        "created_at": order.created_at,
    }


@router.post("/{order_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_order(
    order_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    주문 취소

    - 자신의 주문만 취소 가능
    - 배송 전만 취소 가능
    - 재고 복구
    """
    # 주문 조회
    order = await Order.filter(id=order_id, user=current_user).prefetch_related("items").first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="주문을 찾을 수 없습니다."
        )

    # 취소 가능 상태 확인
    if order.order_status not in [OrderStatus.PENDING, OrderStatus.PAID]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 배송이 시작된 주문은 취소할 수 없습니다.",
        )

    # 재고 복구
    items = await order.items.all()
    for item in items:
        inventory = await Inventory.get_or_none(product_option=item.product_option)
        if inventory:
            inventory.quantity += item.quantity
            await inventory.save()

    # 주문 상태 변경
    order.order_status = OrderStatus.CANCELLED
    order.cancelled_at = datetime.now()
    await order.save()

    return {"message": "주문이 취소되었습니다.", "order_id": order.id}
