from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
User = settings.AUTH_USER_MODEL


class EstablishmentType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_establishment_types",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_establishment_types",
    )

    class Meta:
        db_table = "establishment_types"
        verbose_name = "Establishment Type"
        verbose_name_plural = "Establishment Types"

    def __str__(self) -> str:
        return f"{self.name}"
