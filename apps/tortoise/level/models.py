# Tortoise ORM models for app: levels
from tortoise import fields
from tortoise.models import Model


class Level(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    acronym = fields.CharField(max_length=50, unique=True, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_levels",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_levels",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    class Meta:
        table = "levels"

    def __str__(self) -> str:
        return f"{self.acronym} - {self.name}"
