import pytest

from core.entities.token import TokenEntity
from core.entities.user import UserEntity
from presentation.constants import errors_code
from presentation.exceptions import InternalServerErrorException, UnauthorizedException


class TestAuthLoginUseCase:
    """Unit tests for the login method of AuthUseCase"""

    class TestSuccess:
        """Tests for success cases"""

        @pytest.mark.asyncio
        async def test_should_login_successfully(
            self,
            auth_use_case,
            mock_auth_repository,
            mock_bcrypt_service,
            mock_jwt_service,
            user_factory,
            token_factory,
        ):
            """Test for successful user login"""
            # Given
            email = "test@example.com"
            password = "password123"
            hashed_password = "hashed_password"
            user_id = 1

            user_entity = user_factory(
                id=user_id, email=email, password=hashed_password
            )
            mock_auth_repository.get_user_by_email.return_value = user_entity
            mock_bcrypt_service.verify_password.return_value = True

            mock_token_payload = token_factory(
                user_id=user_id,
                exp=1234567890,
                iat=1234567890,
                jti="some_jti",
                token_type="access",
                iss="issuer",
                aud="audience",
                access_token="access_token_value",
                refresh_token="refresh_token_value",
            )

            mock_jwt_service.generate_tokens.return_value = mock_token_payload

            # When
            result = await auth_use_case.login(email, password)

            # Then
            assert isinstance(result, TokenEntity)
            assert result.user_id == user_id
            assert result.access_token == "access_token_value"
            assert result.refresh_token == "refresh_token_value"
            assert result.user == user_entity

            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_bcrypt_service.verify_password.assert_called_once_with(
                password, hashed_password
            )
            mock_jwt_service.generate_tokens.assert_called_once_with(user_id)

    class TestFailures:
        """Tests for failure cases"""

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_when_user_not_found(
            self, auth_use_case, mock_auth_repository, caplog
        ):
            """Test for login with non-existent user"""
            # Given
            email = "nonexistent@example.com"
            password = "password123"
            mock_auth_repository.get_user_by_email.return_value = None

            # When & Then
            with pytest.raises(UnauthorizedException) as excinfo:
                await auth_use_case.login(email, password)

            assert excinfo.value.code == errors_code.INVALID_CREDENTIALS
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            assert "Login failed for user" in caplog.text

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_when_password_invalid(
            self, auth_use_case, mock_auth_repository, mock_bcrypt_service, caplog
        ):
            """Test for login with invalid password"""
            # Given
            email = "test@example.com"
            password = "wrong_password"
            hashed_password = "hashed_password"
            user_entity = UserEntity(id=1, email=email, password=hashed_password)
            mock_auth_repository.get_user_by_email.return_value = user_entity
            mock_bcrypt_service.verify_password.return_value = False

            # When & Then
            with pytest.raises(UnauthorizedException) as excinfo:
                await auth_use_case.login(email, password)

            assert excinfo.value.code == errors_code.INVALID_CREDENTIALS
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_bcrypt_service.verify_password.assert_called_once_with(
                password, hashed_password
            )
            assert "Login failed for user" in caplog.text

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_user_by_email_failure(
            self, auth_use_case, mock_auth_repository, caplog
        ):
            """Test for internal server error during user retrieval by email"""
            # Given
            email = "test@example.com"
            password = "password123"
            mock_auth_repository.get_user_by_email.side_effect = Exception("DB error")

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.login(email, password)

            assert "Unexpected error during login" in caplog.text
            assert "DB error" in str(excinfo.value.__cause__)
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_verify_password_failure(
            self, auth_use_case, mock_auth_repository, mock_bcrypt_service, caplog
        ):
            """Test for internal server error during password verification"""
            # Given
            email = "test@example.com"
            password = "password123"
            hashed_password = "hashed_password"
            user_entity = UserEntity(id=1, email=email, password=hashed_password)
            mock_auth_repository.get_user_by_email.return_value = user_entity
            mock_bcrypt_service.verify_password.side_effect = Exception("Bcrypt error")

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.login(email, password)

            assert "Unexpected error during login" in caplog.text
            assert "Bcrypt error" in str(excinfo.value.__cause__)
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_bcrypt_service.verify_password.assert_called_once_with(
                password, hashed_password
            )

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_generate_tokens_failure(
            self,
            auth_use_case,
            mock_auth_repository,
            mock_bcrypt_service,
            mock_jwt_service,
            caplog,
        ):
            """Test for internal server error during token generation"""
            # Given
            email = "test@example.com"
            password = "password123"
            hashed_password = "hashed_password"
            user_id = 1
            user_entity = UserEntity(id=user_id, email=email, password=hashed_password)
            mock_auth_repository.get_user_by_email.return_value = user_entity
            mock_bcrypt_service.verify_password.return_value = True
            mock_jwt_service.generate_tokens.side_effect = Exception("JWT error")

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.login(email, password)

            assert "Unexpected error during login" in caplog.text
            assert "JWT error" in str(excinfo.value.__cause__)
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_bcrypt_service.verify_password.assert_called_once_with(
                password, hashed_password
            )
            mock_jwt_service.generate_tokens.assert_called_once_with(user_id)

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_when_user_id_is_none(
            self, auth_use_case, mock_auth_repository, mock_bcrypt_service, caplog
        ):
            """Test for internal server error when user ID is None"""
            # Given
            email = "test@example.com"
            password = "password123"
            hashed_password = "hashed_password"
            user_entity_no_id = UserEntity(
                id=None, email=email, password=hashed_password
            )
            mock_auth_repository.get_user_by_email.return_value = user_entity_no_id
            mock_bcrypt_service.verify_password.return_value = True

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await auth_use_case.login(email, password)

            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_bcrypt_service.verify_password.assert_called_once_with(
                password, hashed_password
            )
            assert "Unexpected error during login" in caplog.text
