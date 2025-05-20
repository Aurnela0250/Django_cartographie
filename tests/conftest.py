import os
import uuid

import django

# Configurez Django avant d'importer des modules qui en dépendent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from django.contrib.auth import get_user_model

from core.domain.entities.user_entity import UserEntity
from infrastructure.db.django_user_repository import DjangoUserRepository
from infrastructure.external_services.jwt_service import JWTService

User = get_user_model()


@pytest.fixture
def user_repository():
    return DjangoUserRepository()


@pytest.fixture
def jwt_service():
    return JWTService()


@pytest.fixture
def test_user(db):
    """Create a test user in the database."""
    user = User.objects.create_user(
        email="testuser@example.com", password="testpassword"
    )
    return user


@pytest.fixture
def test_user_entity():
    """Return a test user entity without saving to the database."""
    return UserEntity(
        id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
        email="testuser@example.com",
        password="",
        active=True,
        updated_by=None,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def auth_tokens(test_user, jwt_service):
    """Generate authentication tokens for a test user."""
    access_token, refresh_token = jwt_service.generate_tokens(str(test_user.id))
    return {"access_token": access_token, "refresh_token": refresh_token}


@pytest.fixture
def auth_header(auth_tokens):
    """Return an Authorization header with a bearer token."""
    return {"Authorization": f"Bearer {auth_tokens['access_token']}"}
