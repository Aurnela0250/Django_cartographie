from typing import Optional

from apps.levels.models import Level
from core.domain.entities.level_entity import LevelEntity
from core.interfaces.level_repository import LevelRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository


class DjangoLevelRepository(
    DjangoBaseRepository[LevelEntity, Level, int], LevelRepository
):
    """Django implementation of the repository for levels"""

    def __init__(self):
        super().__init__(Level, LevelEntity)

    def get_by_name(self, name: str) -> Optional[LevelEntity]:
        """Retrieves a level by its name"""
        try:
            level = self.model.objects.get(name=name)
            return self._to_entity(level)
        except self.model.DoesNotExist:
            return None

    def get_by_acronyme(self, acronym: Optional[str]) -> Optional[LevelEntity]:
        """Retrieves a level by its acronym (can be None)"""
        try:
            level = self.model.objects.get(acronyme=acronym)
            return self._to_entity(level)
        except self.model.DoesNotExist:
            return None
