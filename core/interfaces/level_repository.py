from typing import Optional

from core.domain.entities.level_entity import LevelEntity
from core.interfaces.base_repository import BaseRepository


class LevelRepository(BaseRepository[LevelEntity]):
    """Repository for operations on levels"""

    def get_by_name(self, name: str) -> Optional[LevelEntity]:
        """Retrieves a level by its name"""
        pass

    def get_by_acronyme(self, acronyme: Optional[str]) -> Optional[LevelEntity]:
        """Retrieves a level by its acronym (can be None)"""
        pass
