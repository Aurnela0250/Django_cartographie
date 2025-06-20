from abc import abstractmethod
from typing import Optional

from core.entities.filters import LevelFilters
from core.entities.level_entity import LevelEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class ILevelRepository(BaseRepository[LevelEntity]):
    """Repository for operations on levels"""

    @abstractmethod
    async def get_by_acronym(self, acronym: str) -> Optional[LevelEntity]:
        """Retrieves a level by its acronym"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[LevelEntity]:
        """Retrieves a level by its name"""
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: LevelFilters,
    ) -> PaginatedResult[LevelEntity]:
        """Retrieves a level by its acronym (can be None)"""
        raise NotImplementedError
