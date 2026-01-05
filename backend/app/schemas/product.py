from pydantic import BaseModel, Field
from datetime import datetime
from app.models import ProductStatus, ProductCategory


class ProductCreate(BaseModel):
    """상품 생성 요청"""

    brand_id: int
    name: str = Field(..., min_length=1, max_length=255)
    category: ProductCategory
    price: int = Field(..., gt=0)
    sale_price: int | None = Field(..., gt=0)
    description: str | None = None
    material: str | None = Field(None, max_length=255)
    country_of_origin: str | None = Field(None, max_length=50)
    care_instructions: str | None = None
    model_height: int | None = Field(None, gt=0, lt=250)
    model_weight: int | None = Field(None, gt=0, lt=200)
    model_size: str | None = Field(None, max_length=10)
    shipping_fee: int = Field(3000, ge=0)
    shipping_days: str = Field("2-3일", max_length=50)


class ProductUpdate(BaseModel):
    """상품 수정 요청"""

    brand_id: int | None = None
    name: str | None = Field(None, min_length=1, max_length=255)
    category: ProductCategory | None = None
    price: int | None = Field(None, gt=0)
    sales_price: int | None = Field(None, gt=0)
    description: str | None = None
    material: str | None = Field(None, max_length=255)
    country_of_origin: str | None = Field(None, max_length=50)
    care_instructions: str | None = None
    model_height: int | None = Field(None, gt=0, lt=250)
    model_weight: int | None = Field(None, gt=0, lt=200)
    model_size: str | None = Field(None, max_length=10)
    shipping_fee: int | None = Field(None, ge=0)
    shipping_days: str | None = Field(None, max_length=50)
    status: ProductStatus | None = None


class ProductResponse(BaseModel):
    """상품 응답"""

    id: int
    brand_id: int
    name: str
    category: ProductCategory
    price: int
    sales_price: int | None
    description: str | None
    material: str | None
    country_of_origin: str | None
    care_instructions: str | None
    model_height: int | None
    model_weight: int | None
    model_size: str | None
    shipping_fee: int
    shipping_days: str
    status: ProductStatus
    view_count: int
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
