from tortoise import fields
from tortoise.models import Model
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .brand import Brand
    from .product_image import ProductImage


class ProductCategory(str, Enum):
    """상품 카테고리"""

    TOPS = "tops"
    BOTTOMS = "bottoms"
    OUTERWEAR = "outerwear"
    SHOES = "shoes"
    ACCESSORIES = "accessories"


class ProductStatus(str, Enum):
    """상품 상태"""

    ACTIVE = "active"
    SOLD_OUT = "sold_out"
    INACTIVE = "inactive"


class Product(Model):
    """상품 모델"""

    id = fields.IntField(pk=True)

    # 외래키 : brand와 관계
    brand: fields.ForeignKeyRelation["Brand"] = fields.ForeignKeyField(
        "models.Brand", related_name="products", on_delete=fields.RESTRICT
    )
    # 기본 정보
    name = fields.CharField(max_length=255, index=True)
    category = fields.CharEnumField(ProductCategory, index=True)

    # 가격
    price = fields.IntField()
    sale_price = fields.IntField(null=True)

    # 상세 정보
    description = fields.TextField(null=True)
    material = fields.CharField(max_length=255, null=True)
    country_of_origin = fields.CharField(max_length=50, null=True)
    care_instructions = fields.TextField(null=True)

    # 배송 정보
    shipping_fee = fields.IntField(default=3000)
    shipping_days = fields.CharField(max_length=50, default="2-3일")

    # 모델 착용 정보
    model_height = fields.IntField(null=True)
    model_weight = fields.IntField(null=True)
    model_size = fields.CharField(max_length=10, null=True)

    # 상태
    status = fields.CharEnumField(ProductStatus, default=ProductStatus.ACTIVE, index=True)
    view_count = fields.IntField(default=0)

    # 역참조 (reverse relations) - Mypy를 위한 타입 어노테이션
    images: fields.ReverseRelation["ProductImage"]

    # 타임스탬프
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "products"

    def __str__(self) -> str:
        return self.name
