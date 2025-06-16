from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=255)
    acronyme = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_levels",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_levels",
    )

    class Meta:
        db_table = "levels"
        verbose_name = "Level"
        verbose_name_plural = "Levels"

    def __str__(self) -> str:
        return f"{self.acronyme} - {self.name}"
