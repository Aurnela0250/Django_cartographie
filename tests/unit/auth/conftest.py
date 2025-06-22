"""
Fixtures partagées pour les tests unitaires du module d'authentification.

Ce module centralise toutes les fixtures nécessaires pour tester AuthUseCase,
incluant les mocks des services et du repository.
"""

import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.entities.token import TokenEntity
from core.entities.user import UserEntity
from core.interfaces.auth_repository import IAuthRepository
from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService


@pytest.fixture
def mock_jwt_service():
    """
    Mock du service JWT pour les tests d'authentification.

    Returns:
        MagachMock: Service JWT mockée avec toutes les méthodes nécessaires
    """
    mock_service = MagicMock(spec=JWTService)
    mock_service.generate_tokens = AsyncMock()
    mock_service.decode_access_token = AsyncMock()
    mock_service.decode_refresh_token = AsyncMock()
    mock_service.revoke_token = AsyncMock()
    return mock_service


@pytest.fixture
def mock_bcrypt_service():
    """
    Mock du service Bcrypt pour les tests d'authentification.

    Returns:
        MagicMock: Service Bcrypt mockée avec toutes les méthodes nécessaires
    """
    mock_service = MagicMock(spec=BcryptService)
    mock_service.hash_password = AsyncMock()
    mock_service.verify_password = AsyncMock()
    return mock_service


@pytest.fixture
def mock_auth_repository():
    """
    Mock du repository d'authentification pour les tests.

    Returns:
        AsyncMock: Repository d'authentification mockée avec spec IAuthRepository
    """
    return AsyncMock(spec=IAuthRepository)


@pytest.fixture
def auth_use_case(mock_jwt_service, mock_bcrypt_service, mock_auth_repository):
    """
    Fixture pour créer une instance d'AuthUseCase avec des dépendances mockées.

    Args:
        mock_jwt_service: Service JWT mocké
        mock_bcrypt_service: Service Bcrypt mocké
        mock_auth_repository: Repository d'authentification mocké

    Returns:
        AuthUseCase: Instance du cas d'usage avec des dépendances mockées
    """
    return AuthUseCase(
        jwt_service=mock_jwt_service,
        bcrypt_service=mock_bcrypt_service,
        auth_repository=mock_auth_repository,
    )


@pytest.fixture
def sample_user():
    """
    Fixture pour créer un utilisateur de test standard.

    Returns:
        UserEntity: Utilisateur de test avec des données cohérentes
    """
    return UserEntity(
        id=1,
        email="test@example.com",
        password="hashed_password",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def sample_token_payload():
    """
    Fixture pour créer un payload de token de test standard.

    Returns:
        MagicMock: Payload de token mocké avec des attributs standards
    """
    mock_payload = MagicMock()
    mock_payload.user_id = 1
    mock_payload.exp = 1234567890
    mock_payload.iat = 1234567890
    mock_payload.jti = "sample_jti"
    mock_payload.token_type = "access"
    mock_payload.iss = "issuer"
    mock_payload.aud = "audience"
    mock_payload.access_token = "sample_access_token"
    mock_payload.refresh_token = "sample_refresh_token"
    return mock_payload


@pytest.fixture
def sample_token_entity(sample_user):
    """
    Fixture pour créer une entité Token de test standard.

    Args:
        sample_user: Utilisateur de test

    Returns:
        TokenEntity: Entité token de test avec des données cohérentes
    """
    return TokenEntity(
        user_id=1,
        exp=1234567890,
        iat=1234567890,
        jti="sample_jti",
        token_type="access",
        iss="issuer",
        aud="audience",
        access_token="sample_access_token",
        refresh_token="sample_refresh_token",
        user=sample_user,
    )


@pytest.fixture
def user_factory():
    """
    Fixture pour créer un utilisateur de test.

    Returns:
        function: Fonction de fabrique pour créer des utilisateurs de test
    """

    def _factory(**overrides):
        defaults = {
            "id": 1,
            "email": "test@example.com",
            "password": "hashed_password",
            "created_at": None,
            "updated_at": None,
        }
        return UserEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def token_factory(user_factory):
    """
    Fixture pour créer un token de test.

    Returns:
        function: Fonction de fabrique pour créer des tokens de test
    """

    def _factory(**overrides):
        defaults = {
            "user_id": 1,
            "exp": 1234567890,
            "iat": 1234567890,
            "jti": "sample_jti",
            "token_type": "access",
            "iss": "issuer",
            "aud": "audience",
            "access_token": "sample_access_token",
            "refresh_token": "sample_refresh_token",
            "user": user_factory(),  # Use factory to create a valid UserEntity
        }
        return TokenEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture(autouse=True)
def setup_logging(caplog):
    """
    Configure automatiquement le logging pour tous les tests d'authentification.

    Args:
        caplog: Fixture pytest pour capturer les logs
    """
    caplog.set_level(logging.INFO)
