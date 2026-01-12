from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas import CartItemResponse, CartResponse, CartItemCreate, CartItemUpdate
from app.models import User, Cart, CartItem, ProductOption, Inventory
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
async def get_cart(current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    """
    장바구니 조회

    - 로그인한 사용자만 접근 가능
    - 장바구니가 없으면 빈 장바구니 반환
    """
    # 장바구니 조회
    cart = await Cart.get_or_none(user=current_user).prefetch_related(
        "items__product_option__product__brand"
    )

    if not cart:
        # 장바구니가 없으면 빈 응답
        return {
            "items": [],
            "total_product_price": 0,
            "shipping_fee": 0,
            "final_price": 0,
        }
    # 장바구니 아이템 조회
    items = await CartItem.filter(cart=cart).prefetch_related(
        "product_option__product__brand", "product_option__product__images"
    )

    # 응답 데이터 구성
    items_data = []
    total_product_price = 0

    for item in items:
        option = item.product_option
        product = option.product
        brand = product.brand

        # 가격 계산 (할인가 우선)
        price = product.sale_price if product.sale_price else product.price
        subtotal = price * item.quantity
        total_product_price += subtotal

        # 썸네일 이미지 찾기
        images = await product.images.filter(is_thumbnail=True).first()
        thumbnail_url = images.image_url if images else None

        items_data.append(
            {
                "id": item.id,
                "product_option_id": option.id,
                "quantity": item.quantity,
                "product_name": product.name,
                "brand_name": brand.name,
                "size": option.size,
                "color": option.color,
                "price": price,
                "thumbnail_url": thumbnail_url,
                "created_at": item.created_at,
            }
        )

    # 배송비 계산 ( 50,000원 이상 무료)
    shipping_fee = 0 if total_product_price >= 50000 else 3000
    final_price = total_product_price + shipping_fee

    return {
        "items": items_data,
        "total_product_price": total_product_price,
        "shipping_fee": shipping_fee,
        "final_price": final_price,
    }


@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item_data: CartItemCreate, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    장바구니에 상품 추가

    - 재고 확인
    - 이미 담긴 상품이면 수량 증가
    - 장바구니가 없으면 자동 생성
    """
    # ProductOption 존재 확인
    option = await ProductOption.get_or_none(id=item_data.product_option_id).prefetch_related(
        "product__brand"
    )
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="상품 옵션을 찾을 수 없습니다."
        )

    # 재고 확인
    inventory = await Inventory.get_or_none(product_option=option)
    if not inventory or inventory.quantity < item_data.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="재고가 부족합니다.")

    # 장바구니 조회 또는 생성
    cart = await Cart.get_or_none(user=current_user)
    if not cart:
        cart = await Cart.create(user=current_user)

    # 이미 담긴 상품인지 확인
    existing_item = await CartItem.get_or_none(cart=cart, product_option=option)

    if existing_item:
        # 수량 증가
        new_quantity = existing_item.quantity + item_data.quantity

        # 재고 재확인
        if inventory.quantity < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"재고가 부족합니다. (현재 재고: {inventory.quantity}개)",
            )

        existing_item.quantity = new_quantity
        await existing_item.save()
        cart_item = existing_item
    else:
        # 새로 추가
        cart_item = await CartItem.create(
            cart=cart, product_option=option, quantity=item_data.quantity
        )
    # 응답 데이터 구성
    product = option.product
    brand = product.brand
    price = product.sale_price if product.sale_price else product.price

    images = await product.images.filter(is_thumbnail=True).first()
    thumbnail_url = images.image_url if images else None

    return {
        "id": cart_item.id,
        "product_option_id": option.id,
        "quantity": cart_item.quantity,
        "product_name": product.name,
        "brand_name": brand.name,
        "size": option.size,
        "color": option.color,
        "price": price,
        "thumbnail_url": thumbnail_url,
        "created_at": cart_item.created_at,
    }


@router.patch("/items/{item_id}", response_model=CartItemResponse)
async def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """
    장바구니 상품 수량 변경

    - 재고 확인
    - 자신의 장바구니 아이템만 수정가능
    """
    # CartItem 조회
    cart_item = await CartItem.get_or_none(id=item_id).prefetch_related(
        "cart__user", "product_option__product__brand"
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="장바구니 아이템을 찾을 수 없습니다."
        )

    # 권한 확인
    if cart_item.cart.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다.")

    # 재고 확인
    inventory = await Inventory.get_or_none(product_option=cart_item.product_option)
    if not inventory or inventory.quantity < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"재고가 부족합니다. (현재 재고: {inventory.quantity if inventory else 0}개)",
        )

    # 수량 변경
    cart_item.quantity = item_data.quantity
    await cart_item.save()

    # 응답 데이터 구성
    option = cart_item.product_option
    product = option.product
    brand = product.brand
    price = product.sale_price if product.sale_price else product.price

    images = await product.images.filter(is_thumbnail=True).first()
    thumbnail_url = images.image_url if images else None

    return {
        "id": cart_item.id,
        "product_option_id": option.id,
        "quantity": cart_item.quantity,
        "product_name": product.name,
        "brand_name": brand.name,
        "size": option.size,
        "color": option.color,
        "price": price,
        "thumbnail_url": thumbnail_url,
        "created_at": cart_item.created_at,
    }


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    item_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> None:
    """
    장바구니 상품 삭제

    - 자신의 장바구니 아이템만 삭제 가능
    """
    # CartItem 조회
    cart_item = await CartItem.get_or_none(id=item_id).prefetch_related("cart__user")

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="장바구니 아이템을 찾을 수 없습니다."
        )

    # 권한 확인
    if cart_item.cart.user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다.")

    # 삭제
    await cart_item.delete()
