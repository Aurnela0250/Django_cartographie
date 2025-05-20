from unittest.mock import Mock
from uuid import UUID

import pytest

from core.domain.entities.user_entity import UserEntity
from core.use_cases.auth_use_case import LoginUseCase, SignUpUseCase
from presentation.exceptions import AuthenticationError, ConflictError


@pytest.mark.unit
class TestSignUpUseCase:
    def setup_method(self):
        self.user_repository = Mock()
        self.use_case = SignUpUseCase(self.user_repository)

    def test_execute_success(self):
        # Arrange
        email = "test@example.com"
        password = "password123"

        # Mock repository to return None (user doesn't exist)
        self.user_repository.get_user_by_email.return_value = None
        # Mock user creation
        created_user = UserEntity(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            email=email,
            password="",
            active=True,
            updated_by=None,
            created_at=None,
            updated_at=None,
        )
        self.user_repository.create_user.return_value = created_user

        # Act
        result = self.use_case.execute(email, password)

        # Assert
        assert result.email == email
        self.user_repository.get_user_by_email.assert_called_once_with(email)
        self.user_repository.create_user.assert_called_once()

    def test_execute_user_already_exists(self):
        # Arrange
        email = "existing@example.com"
        password = "password123"
        # Mock repository to return an existing user
        existing_user = UserEntity(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            email=email,
            password="",
            active=True,
            updated_by=None,
            created_at=None,
            updated_at=None,
        )
        self.user_repository.get_user_by_email.return_value = existing_user

        # Act & Assert
        with pytest.raises(ConflictError) as exc_info:
            self.use_case.execute(email, password)

        assert "Un compte existe déjà" in str(exc_info.value)
        self.user_repository.create_user.assert_not_called()


@pytest.mark.unit
class TestLoginUseCase:
    def setup_method(self):
        self.user_repository = Mock()
        self.use_case = LoginUseCase(self.user_repository)

    def test_execute_success(self):
        # Arrange
        email = "test@example.com"
        password = "password123"
        # Mock successful authentication
        authenticated_user = UserEntity(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            email=email,
            password="",
            active=True,
            updated_by=None,
            created_at=None,
            updated_at=None,
        )
        self.user_repository.authenticate_user.return_value = authenticated_user

        # Act
        result = self.use_case.execute(email, password)

        # Assert
        assert result.email == email
        self.user_repository.authenticate_user.assert_called_once_with(email, password)

    def test_execute_invalid_credentials(self):
        # Arrange
        email = "test@example.com"
        password = "wrong_password"

        # Mock failed authentication
        self.user_repository.authenticate_user.return_value = None

        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            self.use_case.execute(email, password)

        assert "Invalid credentials" in str(exc_info.value)

    def test_execute_inactive_user(self):
        # Arrange
        email = "inactive@example.com"
        password = "password123"
        # Mock authentication with inactive user
        inactive_user = UserEntity(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            email=email,
            password="",
            active=False,
            updated_by=None,
            created_at=None,
            updated_at=None,
        )
        self.user_repository.authenticate_user.return_value = inactive_user

        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            self.use_case.execute(email, password)

        assert "User account is not active" in str(exc_info.value)
