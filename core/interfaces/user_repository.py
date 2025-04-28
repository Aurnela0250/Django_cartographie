from abc import abstractmethod
from typing import Optional

from core.domain.entities.user_entity import UserEntity
from core.interfaces.unit_of_work import BaseRepository


class UserRepository(BaseRepository[UserEntity]):
    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        pass
