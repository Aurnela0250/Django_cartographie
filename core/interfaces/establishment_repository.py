from abc import ABC, abstractmethod
from typing import Optional

from core.entities.establishment_entity import EstablishmentEntity
from core.entities.filters import EstablishmentFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class IEstablishmentRepository(BaseRepository[EstablishmentEntity], ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[EstablishmentEntity]:
        """Retrieves an establishment by its name"""
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: EstablishmentFilters,
    ) -> PaginatedResult[EstablishmentEntity]:
        """Checks if the establishment type with the given ID exists"""
        raise NotImplementedError
