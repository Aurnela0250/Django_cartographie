from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=50, null=True, blank=True, unique=True
    )  # e.g., INSEE code
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
        return self.name

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
