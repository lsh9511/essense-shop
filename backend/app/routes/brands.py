from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from app.schemas import BrandUpdate, BrandResponse, BrandCreate
from app.models import Brand, User
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand_data: BrandCreate, current_user: Annotated[User, Depends(get_current_admin)]
) -> Brand:
    """
    브랜드 생성 (관리자 전용)

    - 관리자 권한 필요
    - 브랜드명 중복 체크
    """
    # 중복 체크
    existing = await Brand.filter(name=brand_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 브랜드명입니다."
        )
    # 브랜드 생성
    brand = await Brand.create(**brand_data.model_dump())
    return brand


@router.get("/", response_model=list[BrandResponse])
async def get_brands(skip: int = 0, limit: int = 20, active_only: bool = True) -> list[Brand]:
    """
    브랜드 목록 조회

    - 모든 사용자 접근 가능
    - 페이지네이션 지원
    """
    query = Brand.all()

    if active_only:
        query = query.filter(is_active=True)

    brands = await query.offset(skip).limit(limit)
    return brands


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: int) -> Brand:
    """
    브랜드 상세 조회

    - 모든 사용자 접근 가능
    """
    brand = await Brand.filter(id=brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="브랜드를 찾을 수 없습니다."
        )

    return brand


@router.patch("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: int,
    brand_data: BrandUpdate,
    current_user: Annotated[User, Depends(get_current_admin)],
) -> Brand:
    """
    브랜드 수정 ( 관리자 전용 )

    - 관리자 권한 필요
    """
    brand = await Brand.filter(id=brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="브랜드를 찾을 수 없습니다."
        )

    # 입력된 필드만 업데이트
    update_data = brand_data.model_dump(exclude_unset=True)

    # 이름 중복 체크 (이름 변경 시)
    if "name" in update_data and update_data["name"] != brand.name:
        existing = await Brand.filter(name=update_data["name"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 브랜드명입니다."
            )

    await brand.update_from_dict(update_data).save()
    await brand.refresh_from_db()
    return brand


@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    brand_id: int, current_user: Annotated[User, Depends(get_current_admin)]
) -> None:
    """
    브랜드 삭제 ( 관리자 전용)

    - 관리자 권한 필요
    - 실제로는 is_active=False 로 변경 (소프트 삭제)
    """
    brand = await Brand.filter(id=brand_id).first()
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="브랜드를 찾을 수 없습니다."
        )

    # 소프트 삭제
    brand.is_active = False
    await brand.save()
