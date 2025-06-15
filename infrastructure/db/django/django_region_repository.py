from typing import Optional

from apps.region.models import Region
from core.domain.entities.region_entity import RegionEntity
from core.interfaces.region_repository import RegionRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository


class DjangoRegionRepository(
    DjangoBaseRepository[RegionEntity, Region, int], RegionRepository
):
    """Implémentation Django du repository pour les régions"""

    def __init__(self):
        super().__init__(Region, RegionEntity)

    def get_by_name(self, name: str) -> Optional[RegionEntity]:
        """Récupère une région par son nom"""
        try:
            region = self.model.objects.get(name=name)
            return self._to_entity(region)
        except self.model.DoesNotExist:
            return None

    def get_by_code(self, code: str) -> Optional[RegionEntity]:
        """Récupère une région par son code"""
        try:
            region = self.model.objects.get(code=code)
            return self._to_entity(region)
        except self.model.DoesNotExist:
            return None
