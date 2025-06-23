import logging

from tortoise.transactions import atomic

from core.entities.city import CityEntity
from core.entities.filters import CityFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.city_repository import ICityRepository
from presentation.constants import errors_code
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class CityUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les villes"""

    def __init__(
        self,
        city_repository: ICityRepository,
    ):
        self.city_repository = city_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(self, city_data: CityEntity) -> CityEntity:
        try:
            existing_city = await self.city_repository.get_by_name(city_data.name)
            if existing_city:
                self.logger.warning(f"City with name '{city_data.name}' already exists")
                raise ConflictException(code=errors_code.CONFLICT)
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
                raise NotFoundException(code="city:not_found")
            return city
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during city retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self, city_id: int, update_data: dict, updated_by_id: int
    ) -> CityEntity:
        try:
            existing_city = await self.city_repository.get(city_id)
            if not existing_city:
                raise NotFoundException(code="city:not_found")

            # Check for name conflict if name is being updated
            new_name = update_data.get("name")
            if new_name and new_name != existing_city.name:
                name_exists = await self.city_repository.get_by_name(new_name)
                if name_exists and name_exists.id != city_id:
                    self.logger.warning(
                        f"Cannot update: City with name '{new_name}' already exists"
                    )
                    raise ConflictException(code="city:conflict")

            # Merge data and create a new entity for update
            existing_city_dict = existing_city.model_dump()
            existing_city_dict.update(update_data)
            existing_city_dict["updated_by"] = updated_by_id
            existing_city_dict["region_id"] = existing_city.region_id

            city_to_update = CityEntity(**existing_city_dict)

            updated_city = await self.city_repository.update(city_id, city_to_update)
            return updated_city
        except ConflictException as e:
            raise e
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during city update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, city_id: int) -> bool:
        try:
            existing_city = await self.city_repository.get(city_id)
            if not existing_city:
                raise NotFoundException(code="city:not_found")
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
