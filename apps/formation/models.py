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
