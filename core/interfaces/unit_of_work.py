from abc import ABC, abstractmethod
from typing import Type, TypeVar

from core.interfaces.base_repository import BaseRepository

T = TypeVar("T", bound=BaseRepository)


class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self) -> "UnitOfWork":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def get_repository(
        self,
        repository_class: Type[T],
    ) -> T:
        pass
