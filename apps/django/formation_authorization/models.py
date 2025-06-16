from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# Create your models here.
class FormationAuthorization(models.Model):
    STATUS_CHOICES = [
        ("REQUESTED", "REQUESTED"),
        ("VALIDATED", "VALIDATED"),
        ("REFUSED", "REFUSED"),
        ("EXPIRED", "EXPIRED"),
    ]
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="REQUESTED",
    )
    arrete = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_formation_authorizations",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_formation_authorizations",
    )

    def __str__(self) -> str:
        return f"Accréditation ({self.status})"

    class Meta:
        verbose_name = "Formation Authorization"
        verbose_name_plural = "Formation Authorizations"
        db_table = "formation_authorizations"
