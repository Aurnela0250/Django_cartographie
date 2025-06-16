# Tortoise ORM models for app: establishment_type
from tortoise import fields
from tortoise.models import Model


class EstablishmentType(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_establishment_types",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_establishment_types",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    class Meta:
        table = "establishment_types"

    def __str__(self) -> str:
        return f"{self.name}"
