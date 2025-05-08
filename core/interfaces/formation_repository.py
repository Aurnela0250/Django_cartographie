from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.formation_entity import FormationEntity
from core.interfaces.base_repository import BaseRepository


class IFormationRepository(BaseRepository[FormationEntity], ABC):
    @abstractmethod
    def get_by_intitule(self, intitule: str) -> Optional[FormationEntity]:
        """Récupère une formation par son intitulé."""
        pass
