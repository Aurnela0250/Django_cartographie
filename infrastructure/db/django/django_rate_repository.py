import logging
from typing import Optional

from django.db import IntegrityError

from apps.rate.models import Rate
from core.domain.entities.rate_entity import RateEntity
from core.interfaces.rate_repository import IRateRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository
from infrastructure.db.django_model_to_entity import rate_to_entity
from presentation.exceptions import ConflictError, DatabaseError

logger = logging.getLogger(__name__)


class DjangoRateRepository(
    DjangoBaseRepository[RateEntity, Rate, int], IRateRepository
):
    """Django implementation of the repository for rates"""

    def __init__(self):
        super().__init__(Rate, RateEntity)

    def _to_entity(self, rate: Rate) -> RateEntity:
        """Convert a Django Rate model to a RateEntity"""
        return rate_to_entity(rate)

    def create(self, obj: RateEntity) -> RateEntity:
        try:
            rate = Rate(
                establishment_id=obj.establishment_id,
                user_id=obj.user_id,
                rating=obj.rating,
            )
            rate.save()
            return self._to_entity(rate)
        except IntegrityError as e:
            logger.error(
                f"Database integrity error creating Rate: {e}",
                exc_info=True,
            )
            raise ConflictError()
        except Exception as e:
            logger.error(
                f"Database error creating Rate: {e}",
                exc_info=True,
            )
            raise DatabaseError()

    def create_rate(self, rate: RateEntity) -> RateEntity:
        return self.create(rate)

    def get_rate_by_id(self, rate_id: int) -> Optional[RateEntity]:
        return self.get(rate_id)

    def check_if_user_already_rate(
        self,
        user_id: int,
        establishment_id: int,
    ) -> bool:
        """
        Vérifie si un utilisateur a déjà noté un établissement

        Args:
            user_id: L'ID de l'utilisateur
            establishment_id: L'ID de l'établissement

        Returns:
            bool: True si l'utilisateur a déjà noté l'établissement, False sinon
        """
        return Rate.objects.filter(
            user_id=user_id, establishment_id=establishment_id
        ).exists()
