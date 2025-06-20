import logging

from tortoise.transactions import atomic

from core.entities.city_entity import CityEntity
from core.entities.filters import CityFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.city_repository import ICityRepository
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class CityUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les villes"""

    def __init__(self, city_repository: ICityRepository):
        self.city_repository = city_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(self, city_data: CityEntity) -> CityEntity:
        try:
            existing_city = await self.city_repository.get_by_name(city_data.name)
            if existing_city:
                self.logger.warning(f"City with name '{city_data.name}' already exists")
                raise ConflictException()
            created_city = await self.city_repository.create(city_data)
            return created_city
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during city creation: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, city_id: int) -> CityEntity:
        try:
            city = await self.city_repository.get(city_id)
            if not city:
                raise NotFoundException()
            return city
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during city retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(self, city_id: int, city_data: CityEntity) -> CityEntity:
        try:
            existing_city = await self.city_repository.get(city_id)
            if not existing_city:
                raise NotFoundException()
            if city_data.name != existing_city.name:
                name_exists = await self.city_repository.get_by_name(city_data.name)
                if name_exists and name_exists.id != city_id:
                    self.logger.warning(
                        f"Cannot update: City with name '{city_data.name}' already exists"
                    )
                    raise ConflictException()
            updated_city = await self.city_repository.update(city_id, city_data)
            return updated_city
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during city update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, city_id: int) -> bool:
        try:
            existing_city = await self.city_repository.get(city_id)
            if not existing_city:
                raise NotFoundException()
            result = await self.city_repository.delete(city_id)
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during city deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[CityEntity]:
        try:
            cities = await self.city_repository.get_all(
                pagination_params=pagination_params
            )
            return cities
        except Exception as e:
            self.logger.error(f"Unexpected error during cities retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: CityFilters,
    ) -> PaginatedResult[CityEntity]:
        try:
            cities = await self.city_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return cities
        except Exception as e:
            self.logger.error(f"Unexpected error during cities filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
