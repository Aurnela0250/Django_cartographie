# Tortoise ORM models for app: establishment
from tortoise import fields
from tortoise.models import Model


class Establishment(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    acronym = fields.CharField(max_length=50, unique=True, null=True)
    address = fields.CharField(max_length=255, null=True)
    contacts = fields.JSONField(null=True)
    website = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)
    latitude = fields.FloatField(null=True)
    longitude = fields.FloatField(null=True)
    establishment_type = fields.ForeignKeyField(
        "models.EstablishmentType",
        related_name="establishments",
        on_delete=fields.CASCADE,
        source_field="establishment_type_id",
    )
    city = fields.ForeignKeyField(
        "models.City",
        related_name="establishments",
        on_delete=fields.CASCADE,
        source_field="city_id",
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_establishments",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_establishments",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    class Meta:
        table = "establishments"

    def __str__(self) -> str:
        return f"{self.name}"
