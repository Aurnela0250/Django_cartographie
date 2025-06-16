# Tortoise ORM models for app: sector
from tortoise import fields
from tortoise.models import Model


class Sector(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, unique=True)
    city = fields.ForeignKeyField(
        "models.City",
        related_name="sectors",
        on_delete=fields.CASCADE,
        source_field="city_id",
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_sectors",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_sectors",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "sectors"
