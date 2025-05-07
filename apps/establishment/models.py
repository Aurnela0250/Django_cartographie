from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from apps.establishment_type.models import EstablishmentType

# Create your models here.
User = settings.AUTH_USER_MODEL


class Establishment(models.Model):
    name = models.CharField(max_length=255)
    acronyme = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255)
    code_postal = models.IntegerField()
    ville = models.CharField(max_length=100)
    contacts = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
    )
    site_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # Relation one-to-one with EstablishmentType
    establishment_type = models.OneToOneField(
        EstablishmentType,
        on_delete=models.CASCADE,
        related_name="establishment",
    )

    # Tracking fields
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_establishments",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_establishments",
    )

    class Meta:
        db_table = "establishments"
        verbose_name = "Establishment"
        verbose_name_plural = "Establishments"

    def __str__(self) -> str:
        return f"{self.name}"
