from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.establishment_type_entity import EstablishmentTypeEntity
from core.interfaces.base_repository import BaseRepository


class IEstablishmentTypeRepository(BaseRepository[EstablishmentTypeEntity], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[EstablishmentTypeEntity]:
        """Retrieves an establishment type by its name"""
        pass
