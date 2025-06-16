# Tortoise ORM models for app: formation_authorization
from tortoise import fields
from tortoise.models import Model


class FormationAuthorization(Model):
    id = fields.IntField(primary_key=True)
    STATUS_REQUESTED = "REQUESTED"
    STATUS_VALIDATED = "VALIDATED"
    STATUS_REFUSED = "REFUSED"
    STATUS_EXPIRED = "EXPIRED"
    STATUS_CHOICES = [
        (STATUS_REQUESTED, "REQUESTED"),
        (STATUS_VALIDATED, "VALIDATED"),
        (STATUS_REFUSED, "REFUSED"),
        (STATUS_EXPIRED, "EXPIRED"),
    ]
    issued_date = fields.DateField()
    expiry_date = fields.DateField(null=True)
    status = fields.CharField(max_length=10, default=STATUS_REQUESTED)
    decree = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_formation_authorizations",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_formation_authorizations",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )

    def __str__(self) -> str:
        return f"Autorisation ({self.status} - {self.decree})"

    class Meta:
        table = "formation_authorizations"
