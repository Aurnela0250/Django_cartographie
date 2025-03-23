from abc import ABC, abstractmethod
from typing import List, Optional

from core.domain.entities.school_year import SchoolYearEntity


class SchoolYearRepository(ABC):
    @abstractmethod
    def create(self, school_year_data: SchoolYearEntity) -> SchoolYearEntity:
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[SchoolYearEntity]:
        pass

    @abstractmethod
    def get_all(self) -> List[SchoolYearEntity]:
        pass

    @abstractmethod
    def update(self, id: int, school_year_data: SchoolYearEntity) -> SchoolYearEntity:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    def filter(self, **kwargs) -> List[SchoolYearEntity]:
        pass
