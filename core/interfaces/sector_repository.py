# Interface du repository pour Sector
from typing import Optional

from core.domain.entities.sector_entity import SectorEntity
from core.interfaces.base_repository import BaseRepository


class SectorRepository(BaseRepository[SectorEntity]):
    """Repository pour les opérations sur les secteurs"""

    def get_by_name(self, name: str) -> Optional[SectorEntity]:
        """Récupère un secteur par son nom"""
        return None

    def get_by_region(self, region_id: int) -> list[SectorEntity]:
        """Récupère tous les secteurs d'une région donnée"""
        return []
