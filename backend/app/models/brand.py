from tortoise import fields
from tortoise.models import Model


class Brand(Model):
    """브랜드 모델"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True, index=True)
    name_en = fields.CharField(max_length=100, null=True)
    logo_url = fields.CharField(max_length=500, null=True)
    description = fields.TextField(null=True)
    story = fields.TextField(null=True)
    instagram = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "brands"

    def __str__(self) -> str:
        return self.name
