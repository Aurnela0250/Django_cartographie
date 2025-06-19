from abc import abstractmethod

from core.entities.rate_entity import RateEntity
from core.interfaces.base_repository import BaseRepository


class IRateRepository(BaseRepository[RateEntity]):

    @abstractmethod
    async def get_rate_by_user_for_establishment(
        self,
        user_id: int,
        establishment_id: int,
    ) -> bool:
        """
        Get rate by user for  an establishment.

        Args:
            user_id: The ID of the user
            establishment_id: The ID of the establishment

        Returns:
            bool: True if the user has already rated the establishment, False otherwise
        """
        raise NotImplementedError
