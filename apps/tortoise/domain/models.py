# Tortoise ORM models for app: domain
from tortoise import fields
from tortoise.models import Model


class Domain(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_domains",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_domains",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    class Meta:
        table = "domains"

    def __str__(self) -> str:
        return f"{self.name}"
