# Tortoise ORM models for app: city
from tortoise import fields
from tortoise.models import Model


class City(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, unique=True)
    region = fields.ForeignKeyField("models.Region", related_name="cities")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_cities",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_cities",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "cities"
        # Tortoise ORM n'a pas de verbose_name ou verbose_name_plural direct comme Django.
        # Vous pouvez ajouter des commentaires ou utiliser d'autres moyens pour documenter cela si nécessaire.
