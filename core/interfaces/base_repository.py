from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar
from uuid import UUID

from core.entities.pagination import (
    PaginatedResult,
    PaginationParams,
)

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def create(self, data: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID | int) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[T]:
        pass

    @abstractmethod
    async def update(self, id: UUID | int, data: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: UUID | int) -> bool:
        pass

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        **kwargs,
    ) -> PaginatedResult[T]:
        pass

    @abstractmethod
    async def count(self, **kwargs) -> int:
        """
        Compte le nombre d'entités dans la base de données

        Args:
            **kwargs: Filtres optionnels pour la requête

        Returns:
            int: Le nombre d'entités correspondant aux critères
        """
        pass
