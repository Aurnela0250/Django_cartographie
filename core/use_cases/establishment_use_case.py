import logging

from tortoise.transactions import atomic

from core.entities.establishment import EstablishmentEntity
from core.entities.filters import EstablishmentFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.rate import RateEntity
from core.interfaces.establishment_repository import IEstablishmentRepository
from core.interfaces.rate_repository import IRateRepository
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class EstablishmentUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les établissements"""

    def __init__(
        self,
        establishment_repository: IEstablishmentRepository,
        rate_repository: IRateRepository,
    ):
        self.establishment_repository = establishment_repository
        self.rate_repository = rate_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(
        self,
        establishment_data: EstablishmentEntity,
    ) -> EstablishmentEntity:
        try:
            existing_establishment = await self.establishment_repository.get_by_name(
                establishment_data.name
            )
            if existing_establishment:
                self.logger.warning(
                    f"Establishment with name '{establishment_data.name}' already exists"
                )
                raise ConflictException()
            created_establishment = await self.establishment_repository.create(
                establishment_data
            )
            return created_establishment
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment creation: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(
        self,
        establishment_id: int,
    ) -> EstablishmentEntity:
        try:
            establishment = await self.establishment_repository.get(establishment_id)
            if not establishment:
                raise NotFoundException()
            return establishment
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment retrieval: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self,
        establishment_id: int,
        establishment_data: EstablishmentEntity,
    ) -> EstablishmentEntity:
        try:
            existing_establishment = await self.establishment_repository.get(
                establishment_id
            )
            if not existing_establishment:
                raise NotFoundException()
            if establishment_data.name != existing_establishment.name:
                name_exists = await self.establishment_repository.get_by_name(
                    establishment_data.name
                )
                if name_exists and name_exists.id != establishment_id:
                    self.logger.warning(
                        f"Cannot update: Establishment with name '{establishment_data.name}' already exists"
                    )
                    raise ConflictException()
            updated_establishment = await self.establishment_repository.update(
                establishment_id,
                establishment_data,
            )
            return updated_establishment
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during establishment update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, establishment_id: int) -> bool:
        try:
            existing_establishment = await self.establishment_repository.get(
                establishment_id
            )
            if not existing_establishment:
                raise NotFoundException()
            result = await self.establishment_repository.delete(establishment_id)
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment deletion: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[EstablishmentEntity]:
        try:
            establishments = await self.establishment_repository.get_all(
                pagination_params=pagination_params,
            )
            return establishments
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishments retrieval: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: EstablishmentFilters,
    ) -> PaginatedResult[EstablishmentEntity]:
        try:
            establishments = await self.establishment_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return establishments
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishments filtering: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def rate_establishment(
        self, user_id: int, establishment_id: int, rating: float
    ) -> RateEntity:
        try:
            existing_rate = (
                await self.rate_repository.get_rate_by_user_for_establishment(
                    user_id=user_id, establishment_id=establishment_id
                )
            )

            if existing_rate:
                # Update existing rate
                existing_rate.rating = rating
                # Assert that existing_rate.id is not None, as it comes from the database
                assert existing_rate.id is not None
                updated_rate = await self.rate_repository.update(
                    existing_rate.id, existing_rate
                )
                self.logger.info(
                    f"Rate updated for user {user_id} on establishment {establishment_id}"
                )
                return updated_rate
            else:
                # Create new rate
                new_rate = RateEntity(
                    user_id=user_id, establishment_id=establishment_id, rating=rating
                )
                created_rate = await self.rate_repository.create(new_rate)
                self.logger.info(
                    f"New rate created for user {user_id} on establishment {establishment_id}"
                )
                return created_rate
        except Exception as e:
            self.logger.error(f"Unexpected error during establishment rating: {str(e)}")
            raise InternalServerErrorException(cause=e)
