from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from presentation.exceptions import InternalServerErrorException


class TestAuthLogoutUseCase:
    """Tests unitaires pour la méthode logout de AuthUseCase"""

    @pytest.fixture
    def mock_jwt_service(self):
        """Mock du service JWT"""
        mock_service = MagicMock(spec=JWTService)
        mock_service.decode_access_token = AsyncMock()
        mock_service.decode_refresh_token = AsyncMock()
        mock_service.revoke_token = AsyncMock()
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

    @pytest.mark.asyncio
    async def test_logout_success(self, auth_use_case, mock_jwt_service):
        """Test de déconnexion réussie"""
        # Arrange
        access_token = "valid_access_token"
        refresh_token = "valid_refresh_token"

        fixed_time = 1721600000

        # Mock des payloads des tokens
        access_payload = MagicMock()
        access_payload.jti = "jti-access"
        access_payload.exp = fixed_time + 1000  # Token expire dans 1000 secondes

        refresh_payload = MagicMock()
        refresh_payload.jti = "jti-refresh"
        refresh_payload.exp = fixed_time + 2000  # Token expire dans 2000 secondes

        mock_jwt_service.decode_access_token.return_value = access_payload
        mock_jwt_service.decode_refresh_token.return_value = refresh_payload
        mock_jwt_service.revoke_token.return_value = None

        # Mock datetime.now pour avoir un temps fixe
        with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.timestamp.return_value = fixed_time
            mock_datetime.now.return_value = mock_now

            # Act
            result = await auth_use_case.logout(access_token, refresh_token)

            # Assert
            assert result is None
            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)
            mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                refresh_token
            )
            mock_jwt_service.revoke_token.assert_any_await("jti-access", 1000)
            mock_jwt_service.revoke_token.assert_any_await("jti-refresh", 2000)
            assert mock_jwt_service.revoke_token.await_count == 2

    @pytest.mark.asyncio
    async def test_logout_with_empty_tokens(self, auth_use_case, mock_jwt_service):
        """Test de déconnexion avec tokens vides"""
        # Arrange
        access_token = ""
        refresh_token = ""

        # Mock des payloads avec des tokens expirés (exp dans le passé)
        fixed_time = 1721600000

        access_payload = MagicMock()
        access_payload.jti = "jti-access"
        access_payload.exp = fixed_time - 1000  # Token déjà expiré

        refresh_payload = MagicMock()
        refresh_payload.jti = "jti-refresh"
        refresh_payload.exp = fixed_time - 1000  # Token déjà expiré

        mock_jwt_service.decode_access_token.return_value = access_payload
        mock_jwt_service.decode_refresh_token.return_value = refresh_payload

        with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.timestamp.return_value = fixed_time
            mock_datetime.now.return_value = mock_now

            # Act
            result = await auth_use_case.logout(access_token, refresh_token)

            # Assert
            assert result is None
            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)
            mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                refresh_token
            )
            # Aucun token ne devrait être révoqué car ils sont expirés
            mock_jwt_service.revoke_token.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_logout_jwt_service_error(self, auth_use_case, mock_jwt_service):
        """Test de gestion d'erreur lors du décodage des tokens"""
        # Arrange
        access_token = "valid_access_token"
        refresh_token = "valid_refresh_token"

        # Simuler une erreur lors du décodage du token d'accès
        mock_jwt_service.decode_access_token.side_effect = Exception(
            "Token decode error"
        )

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.logout(access_token, refresh_token)

        mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)

    @pytest.mark.asyncio
    async def test_logout_with_none_tokens(self, auth_use_case, mock_jwt_service):
        """Test de déconnexion avec tokens None"""
        # Arrange
        access_token = None
        refresh_token = None

        # Mock des payloads même pour des tokens None
        fixed_time = 1721600000

        access_payload = MagicMock()
        access_payload.jti = "jti-access"
        access_payload.exp = fixed_time + 1000

        refresh_payload = MagicMock()
        refresh_payload.jti = "jti-refresh"
        refresh_payload.exp = fixed_time + 1000

        mock_jwt_service.decode_access_token.return_value = access_payload
        mock_jwt_service.decode_refresh_token.return_value = refresh_payload

        with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.timestamp.return_value = fixed_time
            mock_datetime.now.return_value = mock_now

            # Act
            result = await auth_use_case.logout(access_token, refresh_token)

            # Assert
            assert result is None
            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)
            mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                refresh_token
            )
            # Les tokens devraient être révoqués car ils sont valides
            assert mock_jwt_service.revoke_token.await_count == 2

    @pytest.mark.asyncio
    async def test_logout_partial_tokens(self, auth_use_case, mock_jwt_service):
        """Test de déconnexion avec seulement un des deux tokens"""
        # Arrange - Test avec seulement access_token
        access_token = "valid_access_token"
        refresh_token = None

        fixed_time = 1721600000

        access_payload = MagicMock()
        access_payload.jti = "jti-access"
        access_payload.exp = fixed_time + 1000

        refresh_payload = MagicMock()
        refresh_payload.jti = "jti-refresh"
        refresh_payload.exp = fixed_time + 1000

        mock_jwt_service.decode_access_token.return_value = access_payload
        mock_jwt_service.decode_refresh_token.return_value = refresh_payload

        with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.timestamp.return_value = fixed_time
            mock_datetime.now.return_value = mock_now

            # Act
            result = await auth_use_case.logout(access_token, refresh_token)

            # Assert
            assert result is None
            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)
            mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                refresh_token
            )
            assert mock_jwt_service.revoke_token.await_count == 2

        # Reset mock pour le deuxième test
        mock_jwt_service.reset_mock()
        mock_jwt_service.decode_access_token.return_value = access_payload
        mock_jwt_service.decode_refresh_token.return_value = refresh_payload

        # Arrange - Test avec seulement refresh_token
        access_token = None
        refresh_token = "valid_refresh_token"

        with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.timestamp.return_value = fixed_time
            mock_datetime.now.return_value = mock_now

            # Act
            result = await auth_use_case.logout(access_token, refresh_token)

            # Assert
            assert result is None
            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)
            mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                refresh_token
            )
            assert mock_jwt_service.revoke_token.await_count == 2
