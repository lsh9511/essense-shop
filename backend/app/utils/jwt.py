from datetime import datetime, timedelta
from typing import Any
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: dict[str, Any]) -> str:
    """
    JWT Access Token 생성

    Args:
        data: 토큰에 담을 데이터 (예: {"user_id":1, "role":"customer"})

    Returns:
        인코딩된 JWT 토큰 문자열
    """

    to_encode = data.copy()

    # 만료 시간 설정
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # JWT 인코딩
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    JWT 토큰 디코딩 및 검증

    Args:
        token: JWT 토큰 문자열
    Returns:
        성공 시 payload dict, 실패 시 None
    """
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
