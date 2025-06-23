from abc import ABC, abstractmethod

from core.entities.domain import DomainEntity
from core.entities.filters import DomainFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class IDomainRepository(BaseRepository[DomainEntity], ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> DomainEntity:
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: DomainFilters,
    ) -> PaginatedResult[DomainEntity]:
        """
        Filtre les domaines selon les critères fournis avec typage strict

        Args:
            pagination_params: Paramètres de pagination
            filters: Filtres typés avec validation Pydantic

        Returns:
            PaginatedResult[DomainEntity]: Résultat paginé des domaines filtrés
        """
        raise NotImplementedError
