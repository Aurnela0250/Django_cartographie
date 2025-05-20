from typing import Optional

from apps.establishment_type.models import EstablishmentType
from core.domain.entities.establishment_type_entity import EstablishmentTypeEntity
from core.interfaces.establishment_type_repository import IEstablishmentTypeRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository


class DjangoEstablishmentTypeRepository(
    DjangoBaseRepository[EstablishmentTypeEntity, EstablishmentType, int],
    IEstablishmentTypeRepository,
):
    """Django implementation of the repository for establishment types"""

    def __init__(self):
        super().__init__(EstablishmentType, EstablishmentTypeEntity)

    def get_by_name(self, name: str) -> Optional[EstablishmentTypeEntity]:
        """Retrieves an establishment type by its name"""
        try:
            establishment_type = self.model.objects.get(name=name)
            return self._to_entity(establishment_type)
        except self.model.DoesNotExist:
            return None
