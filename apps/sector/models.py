from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.city.models import City

# Create your models here.
User = settings.AUTH_USER_MODEL


class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="sectors",
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_sectors",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_sectors",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
