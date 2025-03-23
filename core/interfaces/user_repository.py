from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from core.domain.entities.user import ClientEntity, UserEntity


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def create_client(self, client: ClientEntity) -> ClientEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        pass
