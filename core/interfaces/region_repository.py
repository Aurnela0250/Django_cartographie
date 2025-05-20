from typing import Optional

from core.domain.entities.region_entity import RegionEntity
from core.interfaces.base_repository import BaseRepository


class RegionRepository(BaseRepository[RegionEntity]):
    """Repository pour les opérations sur les régions"""

    def get_by_name(self, name: str) -> Optional[RegionEntity]:
        """Récupère une région par son nom"""
        pass

    def get_by_code(self, code: str) -> Optional[RegionEntity]:
        """Récupère une région par son code"""
        pass
