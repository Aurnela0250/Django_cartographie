from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar
from uuid import UUID

from core.domain.entities.pagination import (
    PaginatedResult,
    PaginationParams,
)

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    def create(self, data: T) -> T:
        pass

    @abstractmethod
    def get(self, id: UUID | int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[T]:
        pass

    @abstractmethod
    def update(self, id: UUID | int, data: T) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: UUID | int) -> bool:
        pass

    @abstractmethod
    def filter(
        self,
        pagination_params: PaginationParams,
        **kwargs,
    ) -> PaginatedResult[T]:
        pass
