from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.establishment.models import Establishment
from apps.formation_authorization.models import FormationAuthorization
from apps.levels.models import Level
from apps.mentions.models import Mention

User = settings.AUTH_USER_MODEL


# Create your models here.
class Formation(models.Model):
    intitule = models.CharField(max_length=255)
    description = models.TextField(
        null=True,
        blank=True,
    )
    duration = models.IntegerField()
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
    )
    mention = models.ForeignKey(
        Mention,
        on_delete=models.CASCADE,
    )
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
    )
    authorization = models.ForeignKey(
        FormationAuthorization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_formations",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_formations",
    )

    def __str__(self) -> str:
        return self.intitule

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        db_table = "formations"


class AnnualHeadcount(models.Model):
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name="annual_headcounts",
    )
    academic_year = models.PositiveIntegerField(
        help_text="Année de début de l'année universitaire (ex: 2023 pour 2023-2024)",
    )
    students = models.PositiveIntegerField(
        default=0,
        help_text="Nombre d'étudiants inscrits pour cette année universitaire",
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_annual_headcounts",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_annual_headcounts",
    )

    success_rate = models.FloatField(
        null=True,
        blank=True,
        help_text="Taux de réussite en pourcentage (ex: 85.5 pour 85,5%)",
    )

    def __str__(self) -> str:
        taux = (
            f" - {self.success_rate:.1f}% réussite"
            if self.success_rate is not None
            else ""
        )
        return f"{self.formation.intitule} - {self.academic_year} - {self.students} étudiants{taux}"

    class Meta:
        verbose_name = "Annual Headcount"
        verbose_name_plural = "Annual Headcounts"
        db_table = "annual_headcounts"
        unique_together = (("formation", "academic_year"),)
