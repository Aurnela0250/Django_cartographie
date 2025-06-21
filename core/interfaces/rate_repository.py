from abc import abstractmethod
from typing import Optional

from core.entities.rate import RateEntity
from core.interfaces.base_repository import BaseRepository


class IRateRepository(BaseRepository[RateEntity]):

    @abstractmethod
    async def get_rate_by_user_for_establishment(
        self,
        user_id: int,
        establishment_id: int,
    ) -> Optional[RateEntity]:
        """
        Get rate by user for  an establishment.

        Args:
            user_id: The ID of the user
            establishment_id: The ID of the establishment

        Returns:
            Optional[RateEntity]: The rate entity if found, None otherwise
        """
        raise NotImplementedError
