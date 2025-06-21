import logging

from tortoise.transactions import atomic

from core.entities.filters import RegionFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.region import RegionEntity
from core.interfaces.region_repository import IRegionRepository
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class RegionUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les régions"""

    def __init__(
        self,
        region_repository: IRegionRepository,
    ):
        self.region_repository = region_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(self, region_data: RegionEntity) -> RegionEntity:
        try:
            existing_region = await self.region_repository.get_by_name(region_data.name)
            if existing_region:
                self.logger.warning(
                    f"Region with name '{region_data.name}' already exists"
                )
                raise ConflictException()
            # Suppression de la vérification d'unicité sur le code, car l'attribut 'code' n'existe pas
            created_region = await self.region_repository.create(region_data)
            return created_region
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during region creation: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, region_id: int) -> RegionEntity:
        try:
            region = await self.region_repository.get(region_id)
            if not region:
                raise NotFoundException()
            return region
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during region retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(self, region_id: int, region_data: RegionEntity) -> RegionEntity:
        try:
            existing_region = await self.region_repository.get(region_id)
            if not existing_region:
                raise NotFoundException()
            if region_data.name != existing_region.name:
                name_exists = await self.region_repository.get_by_name(region_data.name)
                if name_exists and name_exists.id != region_id:
                    self.logger.warning(
                        f"Cannot update: Region with name '{region_data.name}' already exists"
                    )
                    raise ConflictException()
            # Suppression de la vérification d'unicité sur le code, car l'attribut 'code' n'existe pas
            updated_region = await self.region_repository.update(region_id, region_data)
            return updated_region
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during region update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, region_id: int) -> bool:
        try:
            existing_region = await self.region_repository.get(region_id)
            if not existing_region:
                raise NotFoundException()
            result = await self.region_repository.delete(region_id)
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during region deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[RegionEntity]:
        try:
            regions = await self.region_repository.get_all(
                pagination_params=pagination_params
            )
            return regions
        except Exception as e:
            self.logger.error(f"Unexpected error during regions retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: RegionFilters,
    ) -> PaginatedResult[RegionEntity]:
        try:
            regions = await self.region_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return regions
        except Exception as e:
            self.logger.error(f"Unexpected error during regions filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
