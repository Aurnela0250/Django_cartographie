import logging

from tortoise.transactions import atomic

from core.entities.filters import LevelFilters
from core.entities.level_entity import LevelEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.level_repository import ILevelRepository
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class LevelUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les niveaux"""

    def __init__(self, level_repository: ILevelRepository):
        self.level_repository = level_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def create(self, level_data: LevelEntity) -> LevelEntity:
        try:
            existing_level = await self.level_repository.get_by_name(level_data.name)
            if existing_level:
                self.logger.warning(
                    f"Level with name '{level_data.name}' already exists"
                )
                raise ConflictException()
            if level_data.acronym is not None:
                existing_level_acronym = await self.level_repository.get_by_acronym(
                    level_data.acronym
                )
                if existing_level_acronym:
                    self.logger.warning(
                        f"Level with acronym '{level_data.acronym}' already exists"
                    )
                    raise ConflictException()
            created_level = await self.level_repository.create(level_data)
            return created_level
        except ConflictException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during level creation: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, level_id: int) -> LevelEntity:
        try:
            level = await self.level_repository.get(level_id)
            if not level:
                raise NotFoundException()
            return level
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during level retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self,
        level_id: int,
        level_data: LevelEntity,
    ) -> LevelEntity:
        try:
            existing_level = await self.level_repository.get(level_id)
            if not existing_level:
                raise NotFoundException()
            if level_data.name != existing_level.name:
                name_exists = await self.level_repository.get_by_name(level_data.name)
                if name_exists and name_exists.id != level_id:
                    self.logger.warning(
                        f"Cannot update: Level with name '{level_data.name}' already exists"
                    )
                    raise ConflictException()
            if (
                level_data.acronym is not None
                and level_data.acronym != existing_level.acronym
            ):
                acronym_exists = await self.level_repository.get_by_acronym(
                    level_data.acronym
                )
                if acronym_exists and acronym_exists.id != level_id:
                    self.logger.warning(
                        f"Cannot update: Level with acronym '{level_data.acronym}' already exists"
                    )
                    raise ConflictException()
            updated_level = await self.level_repository.update(level_id, level_data)
            return updated_level
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during level update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, level_id: int) -> bool:
        try:
            existing_level = await self.level_repository.get(level_id)
            if not existing_level:
                raise NotFoundException()
            result = await self.level_repository.delete(level_id)
            return result
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during level deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[LevelEntity]:
        try:
            levels = await self.level_repository.get_all(
                pagination_params=pagination_params
            )
            return levels
        except Exception as e:
            self.logger.error(f"Unexpected error during levels retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: LevelFilters,
    ) -> PaginatedResult[LevelEntity]:
        try:
            levels = await self.level_repository.filter(
                pagination_params=pagination_params,
                filters=filters,
            )
            return levels
        except Exception as e:
            self.logger.error(f"Unexpected error during levels filtering: {str(e)}")
            raise InternalServerErrorException(cause=e)
