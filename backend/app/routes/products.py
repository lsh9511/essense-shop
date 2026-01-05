from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Annotated
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.models import Product, Brand, User, ProductCategory, ProductStatus
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate, current_user: Annotated[User, Depends(get_current_admin)]
) -> Product:
    """
    상품 생성 ( 관리자 전용 )

    - 관리자 권한 필요
    - 브랜드 존재 확인
    """
    # 브랜드 존재 확인
    brand = await Brand.filter(id=product_data.brand_id, is_active=True).first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="브랜드를 찾을 수 없습니다."
        )

    # 상품 생성
    product = await Product.create(**product_data.model_dump())
    return product


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = Query(20, le=100),
    category: ProductCategory | None = None,
    brand_id: int | None = None,
    status: ProductStatus | None = Query(ProductStatus.ACTIVE),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
) -> list[Product]:
    """
    상품 목록 조회

    - 모든 사용자 접근 가능
    - 필터링 및 페이지네이션 지원
    """
    query = Product.all()

    # 필터링
    if category:
        query = query.filter(category=category)

    if brand_id:
        query = query.filter(brand_id=brand_id)

    if status:
        query = query.filter(status=status)

    if min_price is not None:
        query = query.filter(price__gte=min_price)

    if max_price is not None:
        query = query.filter(price__lte=max_price)

    # 최신순 정렬
    products = await query.order_by("-created_at").offset(skip).limit(limit)
    return products


@router.get("{product_id}", response_model=ProductResponse)
async def get_product(product_id: int) -> Product:
    """
    상품 상세 조회

    - 모든 사용자 접근 가능
    - 조회수 증가
    """
    product = await Product.filter(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="상품을 찾을 수 없습니다."
        )

    # 조회수 증가
    product.view_count += 1
    await product.save()

    return product


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: Annotated[User, Depends(get_current_admin)],
) -> Product:
    """
    상품 수정 (관리자 전용)

    - 관리자 권한 필요
    """
    product = await Product.filter(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="상품을 찾을 수 없습니다."
        )

    # 입력된 필드만 업데이트
    update_data = product_data.model_dump(exclude_unset=True)

    # 브랜드 변경 시 존재 확인
    if "brand_id" in update_data:
        brand = await Brand.filter(id=update_data["brand_id"], is_active=True).first()
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="브랜드를 찾을 수 없습니다."
            )
    await product.update_from_dict(update_data).save()
    await product.refresh_from_db()
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, current_user: Annotated[User, Depends(get_current_admin)]
) -> None:
    """
    상품 삭제 (관리자 전용)

    - 관리자 권한 필요
    - Soft Delete (status를 inacitve로 변경)
    """
    product = await Product.filter(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="상품을 찾을 수 없습니다."
        )

    # Soft Delete
    product.status = ProductStatus.INACTIVE
    await product.save()
