import logging

from core.domain.entities.user import UserEntity
from core.interfaces.user_repository import UserRepository
from presentation.exceptions import AuthenticationError, ConflictError


class SignUpUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, email: str, password: str) -> UserEntity:

        # Check if email or username already exists
        if self.user_repository.get_user_by_email(email):
            # Log without revealing the exact email in production logs
            self.logger.info("Signup attempt with existing account")
            raise ConflictError(detail="Un compte existe déjà")

        user = UserEntity(
            id=None,
            email=email,
            password=password,
            created_at=None,
            updated_at=None,
        )

        user_created = self.user_repository.create_user(user)

        return user_created


class LoginUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, login: str, password: str) -> UserEntity:
        user = self.user_repository.authenticate_user(login, password)
        if not user:
            raise AuthenticationError("Invalid credentials")
        if not user.active:
            raise AuthenticationError("User account is not active")
        return user
