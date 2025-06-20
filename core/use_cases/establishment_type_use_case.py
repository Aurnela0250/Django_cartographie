import logging

from tortoise.transactions import atomic

from core.entities.establishment_type_entity import EstablishmentTypeEntity
from core.entities.filters import EstablishmentTypeFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.establishment_type_repository import IEstablishmentTypeRepository
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class EstablishmentTypeUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les types d'établissements"""

    def __init__(
        self,
        establishment_type_repository: IEstablishmentTypeRepository,
    ):
        self.establishment_type_repository = establishment_type_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(
        self, establishment_type_data: EstablishmentTypeEntity
    ) -> EstablishmentTypeEntity:
        try:
            existing_type = await self.establishment_type_repository.get_by_name(
                establishment_type_data.name
            )
            if existing_type:
                self.logger.warning(
                    f"Establishment type with name '{establishment_type_data.name}' already exists"
                )
                raise ConflictException()
            created_type = await self.establishment_type_repository.create(
                establishment_type_data
            )
            return created_type
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment type creation: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, establishment_type_id: int) -> EstablishmentTypeEntity:
        try:
            establishment_type = await self.establishment_type_repository.get(
                establishment_type_id
            )
            if not establishment_type:
                raise NotFoundException()
            return establishment_type
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment type retrieval: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self,
        establishment_type_id: int,
        establishment_type_data: EstablishmentTypeEntity,
    ) -> EstablishmentTypeEntity:
        try:
            existing_type = await self.establishment_type_repository.get(
                establishment_type_id
            )
            if not existing_type:
                raise NotFoundException()
            if establishment_type_data.name != existing_type.name:
                name_exists = await self.establishment_type_repository.get_by_name(
                    establishment_type_data.name
                )
                if name_exists and name_exists.id != establishment_type_id:
                    self.logger.warning(
                        f"Cannot update: Establishment type with name '{establishment_type_data.name}' already exists"
                    )
                    raise ConflictException()
            updated_type = await self.establishment_type_repository.update(
                establishment_type_id, establishment_type_data
            )
            return updated_type
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment type update: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, establishment_type_id: int) -> bool:
        try:
            existing_type = await self.establishment_type_repository.get(
                establishment_type_id
            )
            if not existing_type:
                raise NotFoundException()
            result = await self.establishment_type_repository.delete(
                establishment_type_id
            )
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment type deletion: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[EstablishmentTypeEntity]:
        try:
            types = await self.establishment_type_repository.get_all(
                pagination_params=pagination_params
            )
            return types
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment types retrieval: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: EstablishmentTypeFilters,
    ) -> PaginatedResult[EstablishmentTypeEntity]:
        try:
            types = await self.establishment_type_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return types
        except Exception as e:
            self.logger.error(
                f"Unexpected error during establishment types filtering: {str(e)}"
            )
            raise InternalServerErrorException(cause=e)
