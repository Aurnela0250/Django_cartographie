from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    def create(self, data: T) -> T:
        pass

    @abstractmethod
    def get(self, id: UUID | int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, id: UUID | int, data: T) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: UUID | int) -> bool:
        pass

    @abstractmethod
    def filter(self, **kwargs) -> List[T]:
        pass
