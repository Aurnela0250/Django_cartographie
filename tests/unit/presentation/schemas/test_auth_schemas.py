import pytest
from pydantic import ValidationError

from presentation.schemas.auth_schema import Login, Token, TokenData, TokenPayload


@pytest.mark.unit
class TestAuthSchemas:
    def test_login_valid(self):
        # Act
        login = Login(email="test@example.com", password="password123")

        # Assert
        assert login.email == "test@example.com"
        assert login.password == "password123"

    def test_login_missing_fields(self):
        # Act & Assert
        with pytest.raises(ValidationError):
            Login(email="test@example.com")

        with pytest.raises(ValidationError):
            Login(password="password123")

    def test_token_valid(self):
        # Act
        token = Token(
            access_token="access_token_value",
            refresh_token="refresh_token_value",
            token_type="bearer",
        )

        # Assert
        assert token.access_token == "access_token_value"
        assert token.refresh_token == "refresh_token_value"
        assert token.token_type == "bearer"

    def test_token_missing_fields(self):
        # Act & Assert
        # Le champ access_token est obligatoire
        with pytest.raises(ValidationError):
            Token(refresh_token="refresh_token_value", token_type="bearer")

        # Le champ token_type est obligatoire
        with pytest.raises(ValidationError):
            Token(
                access_token="access_token_value", refresh_token="refresh_token_value"
            )
            
        # Test avec seulement access_token et token_type (refresh_token est optionnel)
        token = Token(access_token="access_token_value", token_type="bearer")
        assert token.access_token == "access_token_value"
        assert token.token_type == "bearer"
        assert token.refresh_token is None

    def test_token_payload_valid(self):
        # Act
        payload = TokenPayload(
            user_id="user123", exp=1234567890, iat=1234567800, token_type="access"
        )

        # Assert
        assert payload.user_id == "user123"
        assert payload.exp == 1234567890
        assert payload.iat == 1234567800
        assert payload.token_type == "access"

    def test_token_data_valid(self):
        # Act
        data = TokenData(email="test@example.com")

        # Assert
        assert data.email == "test@example.com"

    def test_token_data_optional_email(self):
        # Act
        data = TokenData()

        # Assert
        assert data.email is None
