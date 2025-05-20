from typing import List, Optional

from apps.sector.models import Sector
from core.domain.entities.sector_entity import SectorEntity
from core.interfaces.sector_repository import SectorRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository
from infrastructure.db.django_model_to_entity import sector_to_entity


class DjangoSectorRepository(
    DjangoBaseRepository[SectorEntity, Sector, int], SectorRepository
):
    """Implémentation Django du repository pour les secteurs"""

    def __init__(self):
        super().__init__(Sector, SectorEntity)

    def get_by_name(self, name: str) -> Optional[SectorEntity]:
        try:
            sector = self.model.objects.get(name=name)
            return sector_to_entity(sector)
        except self.model.DoesNotExist:
            return None

    def get_by_region(self, region_id: int) -> List[SectorEntity]:
        sectors = self.model.objects.filter(region_id=region_id)
        return [sector_to_entity(sector) for sector in sectors]
