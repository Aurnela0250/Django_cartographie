from django.test import TestCase
import pytest

from apps.users.models import User
from core.domain.entities.user_entity import UserEntity
from infrastructure.db.django_user_repository import DjangoUserRepository


@pytest.mark.integration
class TestDjangoUserRepository(TestCase):
    def setUp(self):
        self.repository = DjangoUserRepository()
        # Create a test user
        self.test_user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

    def test_get_user_by_email_existing(self):
        # Act
        user = self.repository.get_user_by_email("test@example.com")

        # Assert
        assert user is not None
        assert user.email == "test@example.com"
        assert isinstance(user, UserEntity)

    def test_get_user_by_email_nonexistent(self):
        # Act
        user = self.repository.get_user_by_email("nonexistent@example.com")

        # Assert
        assert user is None

    def test_get_user_by_id_existing(self):
        # Act
        user = self.repository.get_user_by_id(self.test_user.id)

        # Assert
        assert user is not None
        assert user.email == "test@example.com"
        assert isinstance(user, UserEntity)

    def test_get_user_by_id_nonexistent(self):
        # Import UUID here to avoid potential circular imports
        import uuid

        # Act
        user = self.repository.get_user_by_id(uuid.uuid4())

        # Assert
        assert user is None

    def test_create_user(self):
        # Arrange
        new_user = UserEntity(
            id=None,
            email="new@example.com",
            password="newpassword",
            active=True,
            updated_by=None,
            created_at=None,
            updated_at=None,
        )

        # Act
        created_user = self.repository.create_user(new_user)

        # Assert
        assert created_user is not None
        assert created_user.email == "new@example.com"
        assert isinstance(created_user, UserEntity)

        # Verify the user was actually saved to the database
        db_user = User.objects.filter(email="new@example.com").first()
        assert db_user is not None

    def test_authenticate_user_valid(self):
        # Act
        user = self.repository.authenticate_user("test@example.com", "testpassword")

        # Assert
        assert user is not None
        assert user.email == "test@example.com"

    def test_authenticate_user_invalid_password(self):
        # Act
        user = self.repository.authenticate_user("test@example.com", "wrongpassword")

        # Assert
        assert user is None

    def test_authenticate_user_nonexistent(self):
        # Act
        user = self.repository.authenticate_user(
            "nonexistent@example.com", "testpassword"
        )

        # Assert
        assert user is None
