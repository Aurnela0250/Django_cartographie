from abc import ABC, abstractmethod
from typing import List, Optional

from core.domain.entities.mention_entity import MentionEntity
from core.interfaces.base_repository import BaseRepository


class IMentionRepository(BaseRepository[MentionEntity], ABC):
    @abstractmethod
    def check_domain_exists(self, domain_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, mention_id: int) -> Optional[MentionEntity]:
        pass

    @abstractmethod
    def get_all(self) -> List[MentionEntity]:
        pass

    @abstractmethod
    def update(
        self, mention_id: int, mention_data: MentionEntity
    ) -> Optional[MentionEntity]:
        pass

    @abstractmethod
    def delete(self, mention_id: int) -> bool:
        pass
