import logging
from typing import Optional
from uuid import UUID

from tortoise.exceptions import DoesNotExist, IntegrityError

from apps.tortoise.rate.models import Rate as TortoiseRate
from core.entities.rate import RateEntity
from core.interfaces.rate_repository import IRateRepository
from infrastructure.db.tortoise.model_to_entity import rate_to_entity
from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
)

logger = logging.getLogger(__name__)


class RateRepository(IRateRepository):
    """
    Implémentation du repository pour les notes utilisant Tortoise ORM
    """

    async def _to_entity(self, rate_model: TortoiseRate) -> RateEntity:
        try:
            logger.debug(
                f"Converting rate model to entity for rate ID: {rate_model.id}"
            )
            return await rate_to_entity(rate_model)
        except Exception as e:
            logger.error(f"Error converting rate model to entity: {e}")
            raise DatabaseException("Error converting rate model to entity") from e

    async def create(self, data: RateEntity) -> RateEntity:
        try:
            logger.info(
                f"Creating new rate for user {data.user_id} and establishment {data.establishment_id}"
            )
            rate_model = await TortoiseRate.create(
                rating=data.rating,
                user_id=data.user_id,
                establishment_id=data.establishment_id,
            )
            result = await self._to_entity(rate_model)
            logger.info(f"Rate created successfully with ID: {result.id}")
            return result
        except IntegrityError as e:
            logger.error(f"Error creating rate due to integrity error: {e}")
            raise DatabaseIntegrityException("Error creating rate") from e
        except Exception as e:
            logger.error(f"Error creating rate: {e}")
            raise DatabaseException("Error creating rate") from e

    async def get(self, id: UUID | int) -> Optional[RateEntity]:
        try:
            logger.debug(f"Getting rate by ID: {id}")
            rate_model = await TortoiseRate.get(id=id).prefetch_related(
                "user", "establishment", "created_by", "updated_by"
            )
            result = await self._to_entity(rate_model)
            logger.debug(f"Rate found: {result.id}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Rate with ID {id} not found: {e}")
            raise DatabaseDoesNotExistException(f"Rate with ID {id} not found") from e
        except Exception as e:
            logger.error(f"Error getting rate with ID {id}: {e}")
            raise DatabaseException(f"Error getting rate with ID {id}") from e

    async def get_all(self, pagination_params):
        # Non implémenté car non demandé dans l'interface
        raise NotImplementedError

    async def update(self, id: UUID | int, data: RateEntity) -> RateEntity:
        try:
            logger.info(f"Updating rate with ID: {id}")
            rate_model = await TortoiseRate.get(id=id)

            rate_model.rating = data.rating
            if data.user_id is not None:
                rate_model.user_id = data.user_id
            if data.establishment_id is not None:
                rate_model.establishment_id = data.establishment_id

            await rate_model.save()
            await rate_model.refresh_from_db()

            result = await self._to_entity(rate_model)
            logger.info(f"Rate updated successfully: {result.id}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Rate with ID {id} not found for update: {e}")
            raise DatabaseDoesNotExistException(
                f"Rate with ID {id} not found for update"
            ) from e
        except IntegrityError as e:
            logger.error(f"Error updating rate {id} due to integrity error: {e}")
            raise DatabaseIntegrityException(f"Error updating rate {id}") from e
        except Exception as e:
            logger.error(f"Error updating rate {id}: {e}")
            raise DatabaseException(f"Error updating rate {id}") from e

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting rate with ID: {id}")
            rate_model = await TortoiseRate.get(id=id)
            await rate_model.delete()
            logger.info(f"Rate with ID {id} deleted successfully")
            return True
        except DoesNotExist as e:
            logger.warning(f"Rate with ID {id} not found for deletion: {e}")
            raise DatabaseDoesNotExistException(
                f"Rate with ID {id} not found for deletion"
            ) from e
        except Exception as e:
            logger.error(f"Error deleting rate {id}: {e}")
            raise DatabaseException(f"Error deleting rate {id}") from e

    async def get_rate_by_user_for_establishment(
        self,
        user_id: int,
        establishment_id: int,
    ) -> Optional[RateEntity]:
        try:
            logger.debug(
                f"Getting rate for user {user_id} and establishment {establishment_id}"
            )
            rate_model = await TortoiseRate.get(
                user_id=user_id, establishment_id=establishment_id
            ).prefetch_related("user", "establishment", "created_by", "updated_by")
            result = await self._to_entity(rate_model)
            logger.debug(
                f"Rate found for user {user_id} and establishment {establishment_id}"
            )
            return result
        except DoesNotExist as e:
            logger.warning(
                f"Rate for user {user_id} and establishment {establishment_id} not found: {e}"
            )
            raise DatabaseDoesNotExistException("Rate not found") from e
        except Exception as e:
            logger.error(
                f"Error getting rate for user {user_id} and establishment {establishment_id}: {e}"
            )
            raise DatabaseException("Error getting rate") from e
