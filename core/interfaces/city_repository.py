from typing import Optional

from core.domain.entities.city_entity import CityEntity
from core.domain.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class ICityRepository(BaseRepository[CityEntity]):
    """Repository pour les opérations sur les villes"""

    def get_by_name(self, name: str) -> Optional[CityEntity]:
        """Récupère une ville par son nom"""
        raise NotImplementedError

    def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[CityEntity]:
        """Récupère toutes les villes avec pagination"""
        raise NotImplementedError

    def get_by_region_id(
        self,
        region_id: int,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[CityEntity]:
        """Récupère toutes les villes d'une région spécifique avec pagination"""
        raise NotImplementedError
