from passlib.context import CryptContext

#bcrypt 해싱 컨텍스트 생성
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    """
    비밀번호를 bcrypt로 해싱

    Args:
        password: 평문 비밀번호

    Returns:
        해싱된 비밀번호 문자열
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호 검증

    Args:
        plain_password: 사용자가 입력한 평문 비밀번호
        hashed_password: DB에 저장된 해싱된 비밀번호

    Returns:
        일치하면 True, 아니면 False
    """
    return pwd_context.verify(plain_password, hashed_password)