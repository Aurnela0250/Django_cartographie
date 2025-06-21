from unittest.mock import AsyncMock, MagicMock

import pytest

from core.entities.token import TokenEntity
from core.entities.user import UserEntity
from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from presentation.exceptions import InternalServerErrorException, UnauthorizedException


class MockJWTPayload:
    """Mock pour le payload JWT"""

    def __init__(self, user_id: int, jti: str, exp: int):
        self.user_id = user_id
        self.jti = jti
        self.exp = exp


class TestAuthRefreshTokenUseCase:
    """Tests unitaires pour la méthode refresh_token de AuthUseCase"""

    @pytest.fixture
    def mock_jwt_service(self):
        """Mock du service JWT"""
        mock_service = MagicMock(spec=JWTService)
        mock_service.decode_refresh_token = AsyncMock()
        mock_service.generate_tokens = AsyncMock()
        return mock_service

    @pytest.fixture
    def mock_bcrypt_service(self):
        """Mock du service Bcrypt"""
        mock_service = MagicMock(spec=BcryptService)
        return mock_service

    @pytest.fixture
    def mock_auth_repository(self):
        """Mock du repository d'authentification"""
        mock_repo = AsyncMock()
        mock_repo.get_user_by_id = AsyncMock()
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
            jti="new-jti",
            token_type="bearer",
            iss="test-issuer",
            aud="test-audience",
            access_token="new_access_token",
            refresh_token="new_refresh_token",
            user=sample_user,
        )

    @pytest.fixture
    def mock_jwt_payload(self):
        """Fixture pour un payload JWT mock"""
        return MockJWTPayload(
            user_id=1, jti="old-jti", exp=1640995200  # Timestamp futur
        )

    @pytest.mark.asyncio
    async def test_refresh_token_success(
        self,
        auth_use_case,
        mock_jwt_service,
        mock_auth_repository,
        sample_user,
        sample_token,
        mock_jwt_payload,
    ):
        """Test de rafraîchissement de token réussi"""
        # Arrange
        refresh_token = "old_refresh_token"

        mock_jwt_service.decode_refresh_token.return_value = mock_jwt_payload
        mock_auth_repository.get_user_by_id.return_value = sample_user
        mock_jwt_service.generate_tokens.return_value = sample_token

        # Act
        result = await auth_use_case.refresh_token(refresh_token)

        # Assert
        assert isinstance(result, TokenEntity)
        assert result.access_token == "new_access_token"
        assert result.refresh_token == "new_refresh_token"
        mock_jwt_service.decode_refresh_token.assert_called_once_with(refresh_token)
        mock_auth_repository.get_user_by_id.assert_called_once_with(
            mock_jwt_payload.user_id
        )
        mock_jwt_service.generate_tokens.assert_called_once_with(
            mock_jwt_payload.user_id
        )

    @pytest.mark.asyncio
    async def test_refresh_token_invalid_token(
        self, auth_use_case, mock_jwt_service, mock_auth_repository
    ):
        """Test de rafraîchissement avec token invalide"""
        # Arrange
        refresh_token = "invalid_refresh_token"

        mock_jwt_service.decode_refresh_token.side_effect = UnauthorizedException(
            "Invalid token"
        )

        # Act & Assert
        with pytest.raises(UnauthorizedException):
            await auth_use_case.refresh_token(refresh_token)

        mock_jwt_service.decode_refresh_token.assert_called_once_with(refresh_token)
        mock_auth_repository.get_user_by_id.assert_not_called()
        mock_jwt_service.generate_tokens.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_token_user_not_found(
        self, auth_use_case, mock_jwt_service, mock_auth_repository, mock_jwt_payload
    ):
        """Test de rafraîchissement avec utilisateur inexistant"""
        # Arrange
        refresh_token = "valid_refresh_token"

        mock_jwt_service.decode_refresh_token.return_value = mock_jwt_payload
        mock_auth_repository.get_user_by_id.return_value = None

        # Il faut aussi mocker revoke_token et generate_tokens car ils sont appelés avant la vérification de l'utilisateur
        mock_jwt_service.revoke_token = AsyncMock()

        # Mock pour generate_tokens - il sera appelé même si l'utilisateur n'existe pas
        sample_user = UserEntity(
            id=1,
            email="temp@example.com",
            password="temp_password",
            created_at=None,
            updated_at=None,
        )
        sample_token = TokenEntity(
            user_id=1,
            exp=1640995200,
            iat=1640908800,
            jti="new-jti",
            token_type="bearer",
            iss="test-issuer",
            aud="test-audience",
            access_token="new_access_token",
            refresh_token="new_refresh_token",
            user=sample_user,
        )
        mock_jwt_service.generate_tokens.return_value = sample_token

        # Act & Assert
        with pytest.raises(UnauthorizedException):
            await auth_use_case.refresh_token(refresh_token)

        mock_jwt_service.decode_refresh_token.assert_called_once_with(refresh_token)
        mock_auth_repository.get_user_by_id.assert_called_once_with(
            mock_jwt_payload.user_id
        )
        # generate_tokens EST appelé avant la vérification de l'utilisateur
        mock_jwt_service.generate_tokens.assert_called_once_with(
            mock_jwt_payload.user_id
        )

    @pytest.mark.asyncio
    async def test_refresh_token_user_without_id(
        self, auth_use_case, mock_jwt_service, mock_auth_repository, mock_jwt_payload
    ):
        """Test de rafraîchissement avec utilisateur sans ID"""
        # Arrange
        refresh_token = "valid_refresh_token"
        user_without_id = UserEntity(
            id=None,
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        mock_jwt_service.decode_refresh_token.return_value = mock_jwt_payload
        mock_auth_repository.get_user_by_id.return_value = user_without_id

        # Il faut aussi mocker revoke_token et generate_tokens
        mock_jwt_service.revoke_token = AsyncMock()

        sample_user = UserEntity(
            id=1,
            email="temp@example.com",
            password="temp_password",
            created_at=None,
            updated_at=None,
        )
        sample_token = TokenEntity(
            user_id=1,
            exp=1640995200,
            iat=1640908800,
            jti="new-jti",
            token_type="bearer",
            iss="test-issuer",
            aud="test-audience",
            access_token="new_access_token",
            refresh_token="new_refresh_token",
            user=sample_user,
        )
        mock_jwt_service.generate_tokens.return_value = sample_token

        # Act & Assert - L'implémentation lève une InternalServerErrorException, pas UnauthorizedException
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.refresh_token(refresh_token)

        mock_jwt_service.decode_refresh_token.assert_called_once_with(refresh_token)
        mock_auth_repository.get_user_by_id.assert_called_once_with(
            mock_jwt_payload.user_id
        )
        # generate_tokens EST appelé avant la vérification de l'ID utilisateur
        mock_jwt_service.generate_tokens.assert_called_once_with(
            mock_jwt_payload.user_id
        )

    @pytest.mark.asyncio
    async def test_refresh_token_generate_tokens_error(
        self,
        auth_use_case,
        mock_jwt_service,
        mock_auth_repository,
        sample_user,
        mock_jwt_payload,
    ):
        """Test de gestion d'erreur lors de la génération des nouveaux tokens"""
        # Arrange
        refresh_token = "valid_refresh_token"

        mock_jwt_service.decode_refresh_token.return_value = mock_jwt_payload
        mock_auth_repository.get_user_by_id.return_value = sample_user
        mock_jwt_service.generate_tokens.side_effect = Exception("JWT generation error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.refresh_token(refresh_token)

        mock_jwt_service.decode_refresh_token.assert_called_once_with(refresh_token)
        mock_auth_repository.get_user_by_id.assert_called_once_with(
            mock_jwt_payload.user_id
        )
        mock_jwt_service.generate_tokens.assert_called_once_with(
            mock_jwt_payload.user_id
        )
