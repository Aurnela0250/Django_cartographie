from abc import abstractmethod

from core.entities.user_entity import UserEntity
from core.interfaces.base_repository import BaseRepository


class IAuthRepository(BaseRepository[UserEntity]):
    @abstractmethod
    def signup(self, email: str, hashed_password: str) -> UserEntity:
        """Create a new user in the database."""
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserEntity | None:
        """Get user by email address."""
        raise NotImplementedError

    @abstractmethod
    def update_password(self, user_id: int, hashed_password: str) -> bool:
        """Update user password with hashed password."""
        raise NotImplementedError

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> bool:
        """Delete user from database by ID."""
        raise NotImplementedError
