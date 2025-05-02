from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# Create your models here.
class Accreditation(models.Model):
    STATUT_CHOICES = [
        ("REQUESTED", "REQUESTED"),
        ("VALIDATED", "VALIDATED"),
        ("REFUSED", "REFUSED"),
        ("EXPIREE", "EXPIREE"),
    ]
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default="DEMANDEE")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_regions",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_regions",
    )

    def __str__(self) -> str:
        return f"Accréditation pour {self.fk_etablissement.nom} ({self.statut})"

    class Meta:
        verbose_name = "Accréditation"
        verbose_name_plural = "Accréditations"
