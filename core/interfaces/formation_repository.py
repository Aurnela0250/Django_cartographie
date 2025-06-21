from abc import ABC, abstractmethod
from typing import Optional

from core.entities.filters import FormationFilters
from core.entities.formation import FormationEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class IFormationRepository(BaseRepository[FormationEntity], ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[FormationEntity]:
        """Récupère une formation par son intitulé."""
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: FormationFilters,
    ) -> PaginatedResult[FormationEntity]:
        raise NotImplementedError
