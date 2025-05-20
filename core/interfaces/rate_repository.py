from abc import abstractmethod
from typing import Optional

from core.domain.entities.rate_entity import RateEntity
from core.interfaces.base_repository import BaseRepository


class IRateRepository(BaseRepository[RateEntity]):
    @abstractmethod
    def create_rate(self, rate: RateEntity) -> RateEntity:
        pass

    @abstractmethod
    def get_rate_by_id(self, rate_id: int) -> Optional[RateEntity]:
        pass

    @abstractmethod
    def check_if_user_already_rate(self, user_id: int, establishment_id: int) -> bool:
        """
        Check if a user has already rated an establishment

        Args:
            user_id: The ID of the user
            establishment_id: The ID of the establishment

        Returns:
            bool: True if the user has already rated the establishment, False otherwise
        """
        pass
