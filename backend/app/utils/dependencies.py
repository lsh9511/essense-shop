from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from app.models import User, UserRole
from app.utils.jwt import decode_access_token

# HTTP Bearer 토큰 스키마
security = HTTPBearer()

async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User:
    """
    현재 로그인한 사용자 가져오기

     - Authorization 헤더에서 토큰 추출
     - 토큰 검증 및 디코딩
     - DB에서 사용자 조회

    Returns :
        User: 현재 로그인한 사용자

    Raises:
        HTTPException: 토큰이 유효하지 않거나 사용자를 찾을 수 없을 때
    """
    # 1. 토큰 추출
    token = credentials.credentials

    # 2. 토큰 디코딩
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    #3. user_id 추출
    user_id : int | None = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "토큰에 사용자 정보가 없습니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    #4. DB에서 사용자 조회
    user = await User.filter(id=user_id, is_active=True).first()
    if user is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "사용자를 찾을 수 없습니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

async def get_current_admin(
        current_user: Annotated[User,Depends(get_current_user)]
) -> User:
    """
    현재 로그인한 관리자 가져오기

     - get_current_user로 사용자 확인
     - 관리자 권한 체크

    Returns :
        User : 현재 로그인한 관리자

    Raises:
        HTTPException: 관리자 권한이 없을 때
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="관리자 권한이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return current_user

