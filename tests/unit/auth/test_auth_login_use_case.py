from unittest.mock import AsyncMock, MagicMock

import pytest

from core.entities.token import TokenEntity
from core.entities.user import UserEntity
from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from presentation.exceptions import InternalServerErrorException, UnauthorizedException


class TestAuthLoginUseCase:
    """Tests unitaires pour la méthode login de AuthUseCase"""

    @pytest.fixture
    def mock_jwt_service(self):
        """Mock du service JWT"""
        mock_service = MagicMock(spec=JWTService)
        mock_service.generate_tokens = AsyncMock()
        return mock_service

    @pytest.fixture
    def mock_bcrypt_service(self):
        """Mock du service Bcrypt"""
        mock_service = MagicMock(spec=BcryptService)
        mock_service.verify_password = AsyncMock()
        return mock_service

    @pytest.fixture
    def mock_auth_repository(self):
        """Mock du repository d'authentification"""
        mock_repo = AsyncMock()
        mock_repo.get_user_by_email = AsyncMock()
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

    @pytest.fixture
    def sample_token(self, sample_user):
        """Fixture pour un token de test"""
        return TokenEntity(
            user_id=1,
            exp=1640995200,  # Timestamp
            iat=1640908800,  # Timestamp
            jti="test-jti",
            token_type="bearer",
            iss="test-issuer",
            aud="test-audience",
            access_token="access_token_value",
            refresh_token="refresh_token_value",
            user=sample_user,
        )

    @pytest.mark.asyncio
    async def test_login_success(
        self,
        auth_use_case,
        mock_auth_repository,
        mock_bcrypt_service,
        mock_jwt_service,
        sample_user,
        sample_token,
    ):
        """Test de connexion réussie"""
        # Arrange
        login = "test@example.com"
        password = "password123"

        mock_auth_repository.get_user_by_email.return_value = sample_user
        mock_bcrypt_service.verify_password.return_value = True
        mock_jwt_service.generate_tokens.return_value = sample_token

        # Act
        result = await auth_use_case.login(login, password)

        # Assert
        assert isinstance(result, TokenEntity)
        assert result.user_id == sample_user.id
        assert result.access_token == "access_token_value"
        assert result.refresh_token == "refresh_token_value"
        mock_auth_repository.get_user_by_email.assert_called_once_with(login)
        mock_bcrypt_service.verify_password.assert_called_once_with(
            password, sample_user.password
        )
        mock_jwt_service.generate_tokens.assert_called_once_with(int(sample_user.id))

    @pytest.mark.asyncio
    async def test_login_user_not_found(
        self, auth_use_case, mock_auth_repository, mock_bcrypt_service, mock_jwt_service
    ):
        """Test de connexion avec utilisateur inexistant"""
        # Arrange
        login = "nonexistent@example.com"
        password = "password123"

        mock_auth_repository.get_user_by_email.return_value = None

        # Act & Assert
        with pytest.raises(UnauthorizedException):
            await auth_use_case.login(login, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(login)
        mock_bcrypt_service.verify_password.assert_not_called()
        mock_jwt_service.generate_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_user_without_id(
        self, auth_use_case, mock_auth_repository, mock_bcrypt_service, mock_jwt_service
    ):
        """Test de connexion avec utilisateur sans ID"""
        # Arrange
        login = "test@example.com"
        password = "password123"
        user_without_id = UserEntity(
            id=None,
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_auth_repository.get_user_by_email.return_value = user_without_id

        # Act & Assert
        from presentation.exceptions import InternalServerErrorException

        with pytest.raises(InternalServerErrorException):
            await auth_use_case.login(login, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(login)
        mock_bcrypt_service.verify_password.assert_not_called()
        mock_jwt_service.generate_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_invalid_password(
        self,
        auth_use_case,
        mock_auth_repository,
        mock_bcrypt_service,
        mock_jwt_service,
        sample_user,
    ):
        """Test de connexion avec mot de passe invalide"""
        # Arrange
        login = "test@example.com"
        password = "wrong_password"

        mock_auth_repository.get_user_by_email.return_value = sample_user
        mock_bcrypt_service.verify_password.return_value = False

        # Act & Assert
        with pytest.raises(UnauthorizedException):
            await auth_use_case.login(login, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(login)
        mock_bcrypt_service.verify_password.assert_called_once_with(
            password, sample_user.password
        )
        mock_jwt_service.generate_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_bcrypt_service_error(
        self,
        auth_use_case,
        mock_auth_repository,
        mock_bcrypt_service,
        mock_jwt_service,
        sample_user,
    ):
        """Test de gestion d'erreur lors de la vérification du mot de passe"""
        # Arrange
        login = "test@example.com"
        password = "password123"

        mock_auth_repository.get_user_by_email.return_value = sample_user
        mock_bcrypt_service.verify_password.side_effect = Exception("Bcrypt error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.login(login, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(login)
        mock_bcrypt_service.verify_password.assert_called_once_with(
            password, sample_user.password
        )
        mock_jwt_service.generate_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_jwt_service_error(
        self,
        auth_use_case,
        mock_auth_repository,
        mock_bcrypt_service,
        mock_jwt_service,
        sample_user,
    ):
        """Test de gestion d'erreur lors de la génération des tokens"""
        # Arrange
        login = "test@example.com"
        password = "password123"

        mock_auth_repository.get_user_by_email.return_value = sample_user
        mock_bcrypt_service.verify_password.return_value = True
        mock_jwt_service.generate_tokens.side_effect = Exception("JWT error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.login(login, password)

        mock_auth_repository.get_user_by_email.assert_called_once_with(login)
        mock_bcrypt_service.verify_password.assert_called_once_with(
            password, sample_user.password
        )
        mock_jwt_service.generate_tokens.assert_called_once_with(int(sample_user.id))
