from fastapi import APIRouter, Depends
from typing import Annotated
from app.schemas import UserResponse
from app.models import User
from app.utils.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    내 프로필 조회

     - 로그인한 사용자만 접근 가능
     - 자신의 정보 조회
    """
    return current_user


@router.get("/", reponse_model=list[UserResponse])
async def get_all_users(current_user: Annotated[User, Depends(get_current_admin)]) -> list[User]:
    """
    전체 사용자 조회 (관리자 전용)

    - 관리자 권한 필요
    - 모든 사용자 목록 반환
    """
    users = await User.all()
    return users
