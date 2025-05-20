from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.establishment_entity import EstablishmentEntity
from core.interfaces.base_repository import BaseRepository


class IEstablishmentRepository(BaseRepository[EstablishmentEntity], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[EstablishmentEntity]:
        """Retrieves an establishment by its name"""
        pass

    @abstractmethod
    def check_establishment_type_exists(self, establishment_type_id: int) -> bool:
        """Checks if the establishment type with the given ID exists"""
        pass
