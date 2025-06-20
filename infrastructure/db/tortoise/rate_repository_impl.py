import logging
from typing import Optional
from uuid import UUID

from apps.tortoise.rate.models import Rate as TortoiseRate
from core.entities.rate_entity import RateEntity
from core.interfaces.rate_repository import IRateRepository
from infrastructure.db.tortoise.model_to_entity import rate_to_entity

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
            raise

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
        except Exception as e:
            logger.error(f"Error creating rate: {e}")
            raise

    async def get(self, id: UUID | int) -> Optional[RateEntity]:
        try:
            logger.debug(f"Getting rate by ID: {id}")
            rate_model = await TortoiseRate.get(id=id).prefetch_related(
                "user", "establishment", "created_by", "updated_by"
            )
            result = await self._to_entity(rate_model)
            logger.debug(f"Rate found: {result.id}")
            return result
        except Exception as e:
            logger.warning(f"Rate with ID {id} not found or error occurred: {e}")
            return None

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
        except Exception as e:
            logger.warning(
                f"Rate with ID {id} not found or error occurred during update: {e}"
            )
            raise

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting rate with ID: {id}")
            rate_model = await TortoiseRate.get(id=id)
            await rate_model.delete()
            logger.info(f"Rate with ID {id} deleted successfully")
            return True
        except Exception as e:
            logger.warning(
                f"Rate with ID {id} not found or error occurred during deletion: {e}"
            )
            raise

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
        except Exception as e:
            logger.warning(
                f"Rate for user {user_id} and establishment {establishment_id} not found or error occurred: {e}"
            )
            return None
