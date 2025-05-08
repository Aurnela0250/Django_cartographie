from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.establishment.models import Establishment

User = settings.AUTH_USER_MODEL


class Rate(models.Model):
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name="rates",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rates",
    )
    rating = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rates"
        verbose_name = "Rate"
        verbose_name_plural = "Rates"
        unique_together = [["establishment", "user"]]

    def __str__(self):
        return f"{self.user} a voté {self.establishment} avec {self.rating}/5"
