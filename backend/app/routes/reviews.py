from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas import ReviewCreate, ReviewUpdate, ReviewResponse, ReviewListResponse
from app.models import User, Review, OrderItem, Product, OrderStatus
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    리뷰 작성

    - 구매 확정된 상품만 리뷰 작성 가능
    - 한 주문 상품당 리뷰 1개만 작성 가능
    """
    # OrderItem 조회
    order_item = (
        await OrderItem.filter(id=review_data.order_item_id)
        .prefetch_related("order", "product_option__product")
        .first()
    )

    if not order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="주문 상품을 찾을 수 없습니다."
        )

    # 자신의 주문인지 확인
    order = order_item.order
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="본인의 주문만 리뷰 작성이 가능합니다."
        )

    # 배송 완료된 주문인지 확인
    if order.order_status not in [OrderStatus.DELIVERED, OrderStatus.CONFIRMED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="배송 완료된 상품만 리뷰를 작성할 수 있습니다.",
        )

    # 이미 리뷰 작성했는지 확인
    existing_review = await Review.get_or_none(order_item=order_item)
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 리뷰를 작성한 상품입니다."
        )

    # Product 가져오기
    product = order_item.product_option.product

    # 리뷰 생성
    review = await Review.create(
        user=current_user,
        product=product,
        order_item=order_item,
        rating=review_data.rating,
        content=review_data.content,
        user_height=review_data.user_height,
        user_weight=review_data.user_weight,
        purchase_size=review_data.purchase_size,
        size_satisfaction=review_data.size_satisfaction,
        is_visible=False,  # 관리자 승인 전까지 비공개
    )

    return {
        "id": review.id,
        "user_id": current_user.id,
        "product_id": product.id,
        "order_item_id": order_item.id,
        "rating": review.rating,
        "content": review.content,
        "user_height": review.user_height,
        "user_weight": review.user_weight,
        "purchase_size": review.purchase_size,
        "size_satisfaction": review.size_satisfaction,
        "is_visible": review.is_visible,
        "created_at": review.created_at,
        "updated_at": review.updated_at,
    }


@router.get("", response_model=list[ReviewListResponse])
async def get_my_reviews(
    current_user: Annotated[User, Depends(get_current_user)], page: int = 1, limit: int = 10
) -> list[dict]:
    """
    내 리뷰 목록 조회

    - 페이지네이션
    """
    skip = (page - 1) * limit
    reviews = (
        await Review.filter(user=current_user).order_by("-created_at").offset(skip).limit(limit)
    )

    return [
        {
            "id": review.id,
            "user_id": review.user_id,
            "rating": review.rating,
            "content": review.content,
            "is_visible": review.is_visible,
            "created_at": review.created_at,
        }
        for review in reviews
    ]


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    리뷰 상세 조회

    - 자신의 리뷰만 조회 가능
    """
    review = await Review.filter(id=review_id, user=current_user).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="리뷰를 찾을 수 없습니다."
        )

    return {
        "id": review.id,
        "user_id": review.user_id,
        "product_id": review.product_id,
        "order_item_id": review.order_item_id,
        "rating": review.rating,
        "content": review.content,
        "user_height": review.user_height,
        "user_weight": review.user_weight,
        "purchase_size": review.purchase_size,
        "size_satisfaction": review.size_satisfaction,
        "is_visible": review.is_visible,
        "created_at": review.created_at,
        "updated_at": review.updated_at,
    }


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """
    리뷰 수정

    - 자신의 리뷰만 수정 가능
    """
    review = await Review.filter(id=review_id, user=current_user).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="리뷰를 찾을 수 없습니다."
        )

    # 필드 업데이트
    if review_data.rating is not None:
        review.rating = review_data.rating
    if review_data.content is not None:
        review.content = review_data.content
    if review_data.user_height is not None:
        review.user_height = review_data.user_height
    if review_data.user_weight is not None:
        review.user_weight = review_data.user_weight
    if review_data.purchase_size is not None:
        review.purchase_size = review_data.purchase_size
    if review_data.size_satisfaction is not None:
        review.size_satisfaction = review_data.size_satisfaction

    # 수정 후 재승인 대기
    review.is_visible = False
    await review.save()

    return {
        "id": review.id,
        "user_id": review.user_id,
        "product_id": review.product_id,
        "order_item_id": review.order_item_id,
        "rating": review.rating,
        "content": review.content,
        "user_height": review.user_height,
        "user_weight": review.user_weight,
        "purchase_size": review.purchase_size,
        "size_satisfaction": review.size_satisfaction,
        "is_visible": review.is_visible,
        "created_at": review.created_at,
        "updated_at": review.updated_at,
    }


@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(
    review_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    리뷰 삭제

    - 자신의 리뷰만 삭제 가능
    """
    review = await Review.filter(id=review_id, user=current_user).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="리뷰를 찾을 수 없습니다."
        )

    await review.delete()

    return {"message": "리뷰가 삭제되었습니다.", "review_id": review_id}


@router.get("/products/{product_id}", response_model=list[ReviewListResponse])
async def get_product_reviews(
    product_id: int, page: int = 1, limit: int = 10, rating: int | None = None
) -> list[dict]:
    """
    상품별 리뷰 조회 (공개된 리뷰만)

    - 페이지네이션
    - 평점 필터링
    """
    # 상품 확인
    product = await Product.get_or_none(id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="상품을 찾을 수 없습니다."
        )

    # 쿼리 빌드 (공개된 리뷰만)
    query = Review.filter(product=product, is_visible=True)

    if rating is not None:
        query = query.filter(rating=rating)

    # 페이지네이션
    skip = (page - 1) * limit
    reviews = await query.order_by("-created_at").offset(skip).limit(limit)

    return [
        {
            "id": review.id,
            "user_id": review.user_id,
            "rating": review.rating,
            "content": review.content,
            "is_visible": review.is_visible,
            "created_at": review.created_at,
        }
        for review in reviews
    ]
