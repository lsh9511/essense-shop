from fastapi import APIRouter, HTTPException, status
from app.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.models import User
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token

# 라우터 생성
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister) -> User:
    """
    회원가입
    - 이메일 중복 체크
    - 비밀번호 해싱 후 저장
    - 새 사용자 생성
    """

    # 1. 이메일 중복 체크
    existing_user = await User.filter(email=user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 사용 중인 이메일입니다."
        )

    # 2. 전화번호 중복 체크
    existing_phone = await User.filter(phone=user_data.phone).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 사용 중인 전화번호입니다."
        )
    # 3. 비밀번호 해싱
    hashed_pw = hash_password(user_data.password)

    # 4. 사용자 생성
    user = await User.create(
        email=user_data.email,
        password_hash=hashed_pw,
        name=user_data.name,
        phone=user_data.phone,
        gender=user_data.gender,
        marketing_agree=user_data.marketing_agree,
    )

    return user


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin) -> TokenResponse:
    """
    로그인
    - 이메일/비밀번호 검증
    - JWT 토큰 발급
    """

    # 1. 사용자 조회
    user = await User.filter(email=login_data.email).first()

    # 2. 사용자 존재 여부 및 비밀번호 확인
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 비활성화된 사용자 체크
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비활성화된 계정입니다.")

    # 4. JWT 토큰 생성
    access_token = create_access_token(
        data={"user_id": user.id, "uuid": str(user.uuid), "role": user.role.value}
    )

    # 5. 응답
    return TokenResponse(
        access_token=access_token, token_type="bearer", user=UserResponse.from_orm(user)
    )
