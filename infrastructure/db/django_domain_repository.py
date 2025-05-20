from typing import Optional

from apps.domain.models import Domain
from core.domain.entities.domain_entity import DomainEntity
from core.interfaces.domain_repository import DomainRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository


class DjangoDomainRepository(
    DjangoBaseRepository[DomainEntity, Domain, int], DomainRepository
):
    def __init__(self):
        super().__init__(Domain, DomainEntity)

    def get_by_name(self, name: str) -> Optional[DomainEntity]:
        try:
            domain = self.model.objects.get(name=name)
            return self._to_entity(domain)
        except self.model.DoesNotExist:
            return None
