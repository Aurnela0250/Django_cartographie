import pytest
from pydantic import ValidationError

from presentation.schemas.user_schemas import UserBase, UserCreate, UserOut


@pytest.mark.unit
class TestUserSchemas:
    def test_user_base_valid_email(self):
        # Act
        user = UserBase(email="test@example.com")
        
        # Assert
        assert user.email == "test@example.com"

    def test_user_base_invalid_email(self):
        # Act & Assert
        with pytest.raises(ValidationError):
            UserBase(email="invalid-email")

    def test_user_create_valid(self):
        # Act
        user = UserCreate(email="test@example.com", password="password123")
        
        # Assert
        assert user.email == "test@example.com"
        assert user.password == "password123"

    def test_user_create_missing_password(self):
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com")

    def test_user_out_valid(self):
        # Act
        user = UserOut(email="test@example.com")
        
        # Assert
        assert user.email == "test@example.com"