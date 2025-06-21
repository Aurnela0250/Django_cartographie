from unittest.mock import AsyncMock, MagicMock

import pytest

from core.entities.user import UserEntity
from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from presentation.exceptions import ConflictException, InternalServerErrorException


class TestAuthSignupUseCase:
    """Tests unitaires pour la méthode signup de AuthUseCase"""

    @pytest.fixture
    def mock_jwt_service(self):
        """Mock du service JWT"""
        mock_service = MagicMock(spec=JWTService)
        return mock_service

    @pytest.fixture
    def mock_bcrypt_service(self):
        """Mock du service Bcrypt"""
        mock_service = MagicMock(spec=BcryptService)
        mock_service.hash_password = AsyncMock()
        return mock_service

    @pytest.fixture
    def mock_auth_repository(self):
        """Mock du repository d'authentification"""
        mock_repo = AsyncMock()
        mock_repo.get_user_by_email = AsyncMock()
        mock_repo.signup = AsyncMock()
        return mock_repo

    @pytest.fixture
    def auth_use_case(
        self, mock_jwt_service, mock_bcrypt_service, mock_auth_repository
    ):
        """Fixture pour créer une instance d'AuthUseCase avec des mocks"""
        return AuthUseCase(
            jwt_service=mock_jwt_service,
            bcrypt_service=mock_bcrypt_service,
            auth_repository=mock_auth_repository,
        )

    @pytest.fixture
    def sample_user(self):
        """Fixture pour un utilisateur de test"""
        return UserEntity(
            id=1,
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_signup_success(
        self, auth_use_case, mock_auth_repository, mock_bcrypt_service, sample_user
    ):
        """Test de création de compte réussie"""
        # Arrange
        email = "test@example.com"
        password = "password123"
        hashed_password = "hashed_password"

        mock_auth_repository.get_user_by_email.return_value = None
        mock_bcrypt_service.hash_password.return_value = hashed_password
        mock_auth_repository.signup.return_value = sample_user

        # Act
        result = await auth_use_case.signup(email, password)

        # Assert
        assert result == sample_user
        mock_auth_repository.get_user_by_email.assert_called_once_with(email)
        mock_bcrypt_service.hash_password.assert_called_once_with(password)
        mock_auth_repository.signup.assert_called_once_with(
            email=email, hashed_password=hashed_password
        )

    @pytest.mark.asyncio
    async def test_signup_email_already_exists(
        self, auth_use_case, mock_auth_repository, mock_bcrypt_service, sample_user
    ):
        """Test de création de compte avec email déjà existant"""
        # Arrange
        email = "test@example.com"
        password = "password123"

        mock_auth_repository.get_user_by_email.return_value = sample_user

        # Act & Assert
        with pytest.raises(ConflictException):
            await auth_use_case.signup(email, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(email)
        mock_bcrypt_service.hash_password.assert_not_called()
        mock_auth_repository.signup.assert_not_called()

    @pytest.mark.asyncio
    async def test_signup_bcrypt_service_error(
        self, auth_use_case, mock_auth_repository, mock_bcrypt_service
    ):
        """Test de gestion d'erreur lors du hashage du mot de passe"""
        # Arrange
        email = "test@example.com"
        password = "password123"

        mock_auth_repository.get_user_by_email.return_value = None
        mock_bcrypt_service.hash_password.side_effect = Exception("Bcrypt error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.signup(email, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(email)
        mock_bcrypt_service.hash_password.assert_called_once_with(password)
        mock_auth_repository.signup.assert_not_called()

    @pytest.mark.asyncio
    async def test_signup_repository_error(
        self, auth_use_case, mock_auth_repository, mock_bcrypt_service
    ):
        """Test de gestion d'erreur lors de la création en base"""
        # Arrange
        email = "test@example.com"
        password = "password123"
        hashed_password = "hashed_password"

        mock_auth_repository.get_user_by_email.return_value = None
        mock_bcrypt_service.hash_password.return_value = hashed_password
        mock_auth_repository.signup.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.signup(email, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(email)
        mock_bcrypt_service.hash_password.assert_called_once_with(password)
        mock_auth_repository.signup.assert_called_once_with(
            email=email, hashed_password=hashed_password
        )
