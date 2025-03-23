from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from core.domain.entities.school import SchoolEntity


class SchoolRepository(ABC):
    @abstractmethod
    def create(self, school_data: SchoolEntity) -> SchoolEntity:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[SchoolEntity]:
        pass

    @abstractmethod
    def get_all(self) -> List[SchoolEntity]:
        pass

    @abstractmethod
    def update(self, id: UUID, school_data: SchoolEntity) -> Optional[SchoolEntity]:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def filter(self, **kwargs) -> List[SchoolEntity]:
        pass
