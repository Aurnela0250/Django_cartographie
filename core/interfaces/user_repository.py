from abc import abstractmethod
from typing import Optional

from core.entities.filters import UserFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.user_entity import UserEntity
from core.interfaces.base_repository import BaseRepository


class IUserRepository(BaseRepository[UserEntity]):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: UserFilters,
    ) -> PaginatedResult[UserEntity]:
        """
        Filtre les utilisateurs selon les critères fournis avec typage strict

        Args:
            pagination_params: Paramètres de pagination
            filters: Filtres typés avec validation Pydantic

        Returns:
            PaginatedResult[UserEntity]: Résultat paginé des utilisateurs filtrés
        """
        raise NotImplementedError
