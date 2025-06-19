from abc import abstractmethod
from typing import Optional

from core.entities.filters import RegionFilters
from core.entities.pagination import PaginationParams
from core.entities.region_entity import RegionEntity
from core.interfaces.base_repository import BaseRepository


class RegionRepository(BaseRepository[RegionEntity]):
    """Repository pour les opérations sur les régions"""

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[RegionEntity]:
        """Récupère une région par son nom"""
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: RegionFilters,
    ) -> Optional[RegionEntity]:
        """Récupère une région par son code"""
        raise NotImplementedError
