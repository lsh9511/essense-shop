from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.schemas import WishlistCreate, WishlistResponse
from app.models import User, Wishlist, Product
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/wishlists", tags=["Wishlists"])


@router.post("", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(
    wishlist_data: WishlistCreate, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    찜 추가

    - 이미 찜한 상품인 경우 에러 반환
    """
    # 상품 확인
    product = await Product.get_or_none(id=wishlist_data.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="상품을 찾을 수 없습니다."
        )

    # 이미 찜한 상품인지 확인
    existing = await Wishlist.get_or_none(user=current_user, product=product)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 찜한 상품입니다.")

    # 찜 추가
    wishlist = await Wishlist.create(user=current_user, product=product)

    return {
        "id": wishlist.id,
        "user_id": current_user.id,
        "product_id": product.id,
        "created_at": wishlist.created_at,
    }


@router.get("", response_model=list[WishlistResponse])
async def get_my_wishlists(
    current_user: Annotated[User, Depends(get_current_user)], page: int = 1, limit: int = 20
) -> list[dict]:
    """
    내 찜 목록 조회

    - 페이지네이션
    """
    skip = (page - 1) * limit
    wishlists = (
        await Wishlist.filter(user=current_user).order_by("-created_at").offset(skip).limit(limit)
    )

    return [
        {
            "id": wishlist.id,
            "user_id": wishlist.user_id,
            "product_id": wishlist.product_id,
            "created_at": wishlist.created_at,
        }
        for wishlist in wishlists
    ]


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def remove_from_wishlist(
    product_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    찜 삭제

    - 상품 ID로 찜 삭제
    """
    # 찜 조회
    wishlist = await Wishlist.get_or_none(user=current_user, product_id=product_id)

    if not wishlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="찜한 상품이 아닙니다.")

    await wishlist.delete()

    return {"message": "찜이 삭제되었습니다.", "product_id": product_id}


@router.get("/check/{product_id}", response_model=dict)
async def check_wishlist(
    product_id: int, current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    """
    상품 찜 여부 확인

    - 해당 상품을 찜했는지 여부 반환
    """
    wishlist = await Wishlist.get_or_none(user=current_user, product_id=product_id)

    return {"is_wishlisted": wishlist is not None}
