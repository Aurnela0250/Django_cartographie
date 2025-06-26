import logging

from tortoise.transactions import atomic

from core.entities.filters import LevelFilters
from core.entities.level import LevelEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.level_repository import ILevelRepository
from presentation.exceptions import (
    ConflictException,
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
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
            created_level = await self.level_repository.create(level_data)
            return created_level
        except DatabaseIntegrityException as e:
            self.logger.warning(f"Conflict during level creation: {e}")
            raise ConflictException(str(e)) from e
        except Exception as e:
            self.logger.error(f"Unexpected error during level creation: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get(self, level_id: int) -> LevelEntity:
        try:
            return await self.level_repository.get(level_id)
        except DatabaseDoesNotExistException as e:
            raise NotFoundException(cause=e) from e
        except Exception as e:
            self.logger.error(f"Unexpected error during level retrieval: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def update(
        self,
        level_id: int,
        level_data: dict,
    ) -> LevelEntity:
        try:
            await self.level_repository.get(level_id)
            level_entity = LevelEntity(**level_data)
            updated_level = await self.level_repository.update(level_id, level_entity)
            return updated_level
        except DatabaseDoesNotExistException as e:
            self.logger.warning(f"Level with ID {level_id} not found for update.")
            raise NotFoundException(cause=e)
        except DatabaseIntegrityException as e:
            self.logger.error(
                f"Error updating level with ID {level_id} due to integrity error: {e}"
            )
            raise ConflictException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during level update: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def delete(self, level_id: int) -> bool:
        try:
            return await self.level_repository.delete(level_id)
        except DatabaseDoesNotExistException as e:
            self.logger.error(f"Level with id {level_id} not found")
            raise NotFoundException(cause=e)
        except DatabaseException as e:
            self.logger.error(f"Database error during Level deletion: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during Level deletion: {str(e)}")
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
