# Tortoise ORM models for app: formation
from tortoise import fields
from tortoise.models import Model


class Formation(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    duration = fields.IntField()
    level = fields.ForeignKeyField(
        "models.Level",
        on_delete=fields.CASCADE,
        source_field="level_id",
    )
    mention = fields.ForeignKeyField(
        "models.Mention",
        on_delete=fields.CASCADE,
        source_field="mention_id",
    )
    establishment = fields.ForeignKeyField(
        "models.Establishment",
        on_delete=fields.CASCADE,
        source_field="establishment_id",
    )
    authorization = fields.ForeignKeyField(
        "models.FormationAuthorization",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="authorization_id",
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_formations",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_formations",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        table = "formations"
        # Tortoise ORM n'a pas de verbose_name ou verbose_name_plural direct comme Django.
        # Vous pouvez ajouter des commentaires ou utiliser d'autres moyens pour documenter cela si nécessaire.
