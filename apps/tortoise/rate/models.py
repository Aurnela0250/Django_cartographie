# Tortoise ORM models for app: rate
from tortoise import fields
from tortoise.models import Model


class Rate(Model):
    id = fields.IntField(primary_key=True)
    establishment = fields.ForeignKeyField(
        "models.Establishment",
        related_name="rates",
        on_delete=fields.CASCADE,
        source_field="establishment_id",
    )
    user = fields.ForeignKeyField(
        "models.User",
        related_name="rates",
        on_delete=fields.CASCADE,
        source_field="user_id",
    )
    rating = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "rates"
        unique_together = ("establishment_id", "user_id")
        # Tortoise ORM n'a pas de verbose_name ou verbose_name_plural direct comme Django.
        # Vous pouvez ajouter des commentaires ou utiliser d'autres moyens pour documenter cela si nécessaire.

    def __str__(self):
        return f"{self.user} a voté {self.establishment} avec {self.rating}/5"
