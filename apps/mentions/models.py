from django.conf import settings
from django.db import models
from django.utils import timezone

# Import the Domain model
from apps.domain.models import Domain

User = settings.AUTH_USER_MODEL


# Create your models here.
class Mention(models.Model):
    name = models.CharField(max_length=255)
    # Add the ForeignKey to Domain
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, related_name="mentions"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_mentions",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_mentions",
    )

    class Meta:
        db_table = "mentions"
        verbose_name = "Mention"
        verbose_name_plural = "Mentions"

    def __str__(self) -> str:
        # Optionally update the string representation to include the domain
        return f"{self.name} ({self.domain.name})"
