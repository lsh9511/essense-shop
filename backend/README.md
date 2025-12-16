# ESSENCE Backend

FastAPI 기반의 ESSENCE 백엔드 서버입니다.

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/                    # API 엔드포인트
│   │   └── v1/
│   │       ├── endpoints/      # 각 리소스별 엔드포인트
│   │       │   ├── auth.py
│   │       │   ├── products.py
│   │       │   ├── orders.py
│   │       │   └── ...
│   │       └── router.py       # API v1 라우터
│   ├── core/                   # 핵심 설정
│   │   ├── config.py           # 환경 설정
│   │   ├── security.py         # JWT, 암호화
│   │   └── deps.py             # 의존성 주입
│   ├── db/                     # 데이터베이스
│   │   ├── base.py             # Base 클래스
│   │   └── session.py          # DB 세션
│   ├── models/                 # SQLAlchemy 모델
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── brand.py
│   │   ├── order.py
│   │   └── ...
│   ├── schemas/                # Pydantic 스키마
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── auth.py
│   │   └── ...
│   ├── services/               # 비즈니스 로직
│   ├── utils/                  # 유틸리티 함수
│   └── main.py                 # FastAPI 앱 엔트리포인트
├── alembic/                    # DB 마이그레이션
├── tests/                      # 테스트
├── .env.example                # 환경 변수 예시
└── pyproject.toml              # 프로젝트 설정
```

## 시작하기

### 1. 가상환경 활성화

프로젝트 루트에서:
```bash
source .venv/bin/activate
```

### 2. 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일 생성:
```bash
cd backend
cp .env.example .env
```

`.env` 파일을 열어 필요한 값 설정:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/essence_db
# 또는 개발 시 SQLite 사용
# DATABASE_URL=sqlite:///./essence.db
```

### 3. 데이터베이스 설정

PostgreSQL 사용 시:
```bash
# PostgreSQL 설치 (macOS)
brew install postgresql
brew services start postgresql

# 데이터베이스 생성
createdb essence_db
```

SQLite 사용 시 (개발):
- 별도 설치 불필요
- `.env`에서 `DATABASE_URL=sqlite:///./essence.db` 설정

### 4. 서버 실행

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

또는 간단하게:
```bash
cd backend
uvicorn app.main:app --reload
```

### 5. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 개발 가이드

### 모델 작성

`docs/DATABASE_SCHEMA.md` 참고하여 `app/models/` 에 작성

### 스키마 작성

`docs/API_SPEC.md` 참고하여 `app/schemas/` 에 작성

### API 엔드포인트 작성

1. `app/api/v1/endpoints/` 에 파일 생성
2. `app/api/v1/router.py` 에 라우터 등록

### DB 마이그레이션 (Alembic)

```bash
# Alembic 초기화
alembic init alembic

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "설명"

# 마이그레이션 실행
alembic upgrade head
```

## 테스트

```bash
# 모든 테스트 실행
pytest

# 특정 파일 테스트
pytest tests/test_auth.py

# 커버리지와 함께
pytest --cov=app tests/
```

## 코드 포맷팅

```bash
# Black 포맷터
black app/

# Ruff 린터
ruff check app/

# 타입 체크
mypy app/
```

## 참고 문서

- `../docs/DATABASE_SCHEMA.md` - 데이터베이스 스키마
- `../docs/API_SPEC.md` - API 명세서
- `../docs/PRD.md` - 제품 요구사항
- `../docs/DEVELOPMENT_TIMELINE.md` - 개발 일정