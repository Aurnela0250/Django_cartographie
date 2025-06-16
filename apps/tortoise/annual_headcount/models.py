from tortoise import fields
from tortoise.models import Model


class AnnualHeadcount(Model):
    id = fields.IntField(primary_key=True)
    formation = fields.ForeignKeyField(
        "models.Formation",
        related_name="annual_headcounts",
        on_delete=fields.CASCADE,
        source_field="formation_id",
    )
    academic_year = fields.IntField()
    students = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_by = fields.ForeignKeyField(
        "models.User",
        related_name="created_annual_headcounts",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="created_by_id",
    )
    updated_by = fields.ForeignKeyField(
        "models.User",
        related_name="updated_annual_headcounts",
        on_delete=fields.SET_NULL,
        null=True,
        source_field="updated_by_id",
    )
    success_rate = fields.FloatField(null=True)

    def __str__(self) -> str:
        taux = (
            f" - {self.success_rate:.1f}% réussite"
            if self.success_rate is not None
            else ""
        )
        return f"{self.formation.intitule} - {self.academic_year} - {self.students} étudiants{taux}"

    class Meta:
        table = "annual_headcounts"
        unique_together = ("formation_id", "academic_year")
