from core.domain.entities.user import ClientEntity, UserEntity
from core.interfaces.user_repository import UserRepository
from presentation.exceptions import AuthenticationError, ValidationError


class SignUpClientUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(
        self, email: str, username: str, password: str, client_type: str
    ) -> ClientEntity:

        # Check if email or username already exists
        if self.user_repository.get_user_by_email(email):
            raise ValidationError("Email already exists")
        if self.user_repository.get_user_by_username(username):
            raise ValidationError("Username already exists")

        client = ClientEntity(
            id=None,
            email=email,
            username=username,
            password=password,
            client_type=client_type,
            created_by=None,
            created_at=None,
            updated_at=None,
        )

        client_created = self.user_repository.create_client(client)

        return client_created


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
