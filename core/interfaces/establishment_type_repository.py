from abc import ABC, abstractmethod
from typing import Optional

from core.entities.establishment_type_entity import EstablishmentTypeEntity
from core.entities.filters import EstablishmentTypeFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class IEstablishmentTypeRepository(BaseRepository[EstablishmentTypeEntity], ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[EstablishmentTypeEntity]:
        """Retrieves an establishment type by its name"""
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: EstablishmentTypeFilters,
    ) -> PaginatedResult[EstablishmentTypeEntity]:
        """Filters establishment types based on the provided criteria"""
        raise NotImplementedError
