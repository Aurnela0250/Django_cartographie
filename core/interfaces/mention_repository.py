from abc import ABC, abstractmethod
from typing import Optional

from core.entities.filters import MentionFilters
from core.entities.mention_entity import MentionEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.base_repository import BaseRepository


class IMentionRepository(BaseRepository[MentionEntity], ABC):

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[MentionEntity]:
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: MentionFilters,
    ) -> PaginatedResult[MentionEntity]:
        raise NotImplementedError
