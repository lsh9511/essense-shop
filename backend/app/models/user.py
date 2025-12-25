from tortoise import fields
from tortoise.models import Model
from enum import Enum
import uuid

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class User(Model):

    # 기본키: 내부용 Int + 외부용 UUID
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid.uuid4, unique=True, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    password_hash = fields.CharField(max_length=255,null=True) # 소셜 로그인 시 NULL
    name = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=20)
    birth_date = fields.DateField(null=True)
    gender = fields.CharEnumField(Gender)
    role = fields.CharEnumField(UserRole, default=UserRole.CUSTOMER)
    provider = fields.CharField(max_length=20, null=True) # kakao, naver, google
    provider_id = fields.CharField(max_length=255, null=True)
    marketing_agree = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.name} ({self.email})"