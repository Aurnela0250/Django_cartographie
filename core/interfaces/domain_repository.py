from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.domain_entity import DomainEntity
from core.interfaces.base_repository import BaseRepository


class DomainRepository(BaseRepository[DomainEntity], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[DomainEntity]:
        pass
