from typing import AsyncGenerator

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db, close_db
from app.routes import auth, users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    print("Database connected")
    yield
    await close_db()
    print("Database disconnected")


# FastAPI 앱 생성
app = FastAPI(
    title="ESSENCE API", description="프리미엄 편집샵", version="1.0.0", lifespan=lifespan
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "ESSENCE API is running", "status": "healthy"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "database": "connected"}
