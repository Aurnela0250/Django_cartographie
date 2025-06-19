from abc import abstractmethod
from typing import Optional

from core.entities.city_entity import CityEntity
from core.entities.filters import CityFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class ICityRepository(BaseRepository[CityEntity]):
    """Repository pour les opérations sur les villes"""

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[CityEntity]:
        """Récupère une ville par son nom"""
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: CityFilters,
    ) -> PaginatedResult[CityEntity]:
        """
        Filtre les villes selon les critères fournis

        Args:
            pagination_params: Paramètres de pagination
            filters: Dictionnaire de filtres

        Returns:
            PaginatedResult[CityEntity]: Résultat paginé des villes filtrées
        """
        raise NotImplementedError
