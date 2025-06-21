from unittest.mock import AsyncMock, MagicMock

import pytest

from core.entities.user import UserEntity
from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from presentation.exceptions import InternalServerErrorException, UnauthorizedException


class TestAuthGetCurrentUserUseCase:
    """Tests unitaires pour la méthode get_current_user de AuthUseCase"""

    @pytest.fixture
    def mock_jwt_service(self):
        """Mock du service JWT"""
        mock_service = MagicMock(spec=JWTService)
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

    @pytest.mark.asyncio
    async def test_get_current_user_success(
        self, auth_use_case, mock_auth_repository, sample_user
    ):
        """Test de récupération de l'utilisateur courant réussi"""
        # Arrange
        user_id = 1
        mock_auth_repository.get_user_by_id.return_value = sample_user

        # Act
        result = await auth_use_case.get_current_user(user_id)

        # Assert
        assert result == sample_user
        assert result.id == user_id
        assert result.email == "test@example.com"
        mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_current_user_not_found(
        self, auth_use_case, mock_auth_repository
    ):
        """Test de récupération avec utilisateur inexistant"""
        # Arrange
        user_id = 999
        mock_auth_repository.get_user_by_id.return_value = None

        # Act & Assert
        with pytest.raises(UnauthorizedException):
            await auth_use_case.get_current_user(user_id)

        mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_current_user_repository_error(
        self, auth_use_case, mock_auth_repository
    ):
        """Test de gestion d'erreur lors de la récupération en base"""
        # Arrange
        user_id = 1
        mock_auth_repository.get_user_by_id.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await auth_use_case.get_current_user(user_id)

        mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_get_current_user_with_different_ids(
        self, auth_use_case, mock_auth_repository
    ):
        """Test de récupération avec différents IDs d'utilisateur"""
        # Arrange
        user_ids = [1, 2, 3, 100]
        users = [
            UserEntity(
                id=uid,
                email=f"user{uid}@example.com",
                password="hashed",
                created_at=None,
                updated_at=None,
            )
            for uid in user_ids
        ]

        # Configuration des mocks pour retourner l'utilisateur correspondant
        def get_user_side_effect(uid):
            for user in users:
                if user.id == uid:
                    return user
            return None

        mock_auth_repository.get_user_by_id.side_effect = get_user_side_effect

        # Act & Assert
        for i, user_id in enumerate(user_ids):
            result = await auth_use_case.get_current_user(user_id)
            assert result == users[i]
            assert result.id == user_id
            assert result.email == f"user{user_id}@example.com"

        # Vérifier que le repository a été appelé pour chaque user_id
        assert mock_auth_repository.get_user_by_id.call_count == len(user_ids)
