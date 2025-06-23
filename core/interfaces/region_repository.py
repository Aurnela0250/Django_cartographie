from abc import abstractmethod

from core.entities.filters import RegionFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.region import RegionEntity
from core.interfaces.base_repository import BaseRepository


class IRegionRepository(BaseRepository[RegionEntity]):
    """Repository pour les opérations sur les régions"""

    @abstractmethod
    async def get_by_name(self, name: str) -> RegionEntity:
        """Récupère une région par son nom"""
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: RegionFilters,
    ) -> PaginatedResult[RegionEntity]:
        """Récupère une région par son code"""
        raise NotImplementedError
