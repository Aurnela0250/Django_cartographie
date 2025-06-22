from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

import pytest

from core.entities.token import TokenEntity
from core.entities.user import UserEntity
from presentation.constants import errors_code
from presentation.exceptions import InternalServerErrorException, UnauthorizedException


class TestAuthRefreshTokenUseCase:
    """Unit tests for the refresh_token method of AuthUseCase"""

    class TestSuccess:
        """Tests for success cases"""

        @pytest.mark.asyncio
        @patch("core.use_cases.auth_use_case.datetime")
        async def test_should_refresh_token_successfully(
            self,
            mock_datetime,
            auth_use_case,
            mock_jwt_service,
            mock_auth_repository,
            user_factory,
            token_factory,
        ):
            """Test for successful token refresh"""
            # Given
            refresh_token_str = "old_refresh_token"
            user_id = 1
            jti = "old_jti"

            # Mock datetime.now to control timestamp
            fixed_now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
            mock_datetime.now.return_value = fixed_now

            # Mock old refresh token payload
            mock_old_payload = AsyncMock()
            mock_old_payload.user_id = user_id
            mock_old_payload.jti = jti
            mock_old_payload.exp = int(
                (fixed_now + timedelta(seconds=3600)).timestamp()
            )  # Expires in 1 hour
            mock_jwt_service.decode_refresh_token.return_value = mock_old_payload

            # Mock new token payload
            mock_new_token_payload = token_factory(
                user_id=user_id,
                exp=1234567890,
                iat=1234567890,
                jti="new_jti",
                token_type="access",
                iss="issuer",
                aud="audience",
                access_token="new_access_token_value",
                refresh_token="new_refresh_token_value",
            )
            mock_jwt_service.generate_tokens.return_value = mock_new_token_payload

            # Mock user found
            user_found = user_factory(
                id=user_id, email="test@example.com", password="hashed_password"
            )
            mock_auth_repository.get_user_by_id.return_value = user_found

            # When
            result = await auth_use_case.refresh_token(refresh_token_str)

            # Then
            assert isinstance(result, TokenEntity)
            assert result.user_id == user_id
            assert result.access_token == "new_access_token_value"
            assert result.refresh_token == "new_refresh_token_value"
            assert result.user == user_found

            mock_jwt_service.decode_refresh_token.assert_called_once_with(
                refresh_token_str
            )
            mock_jwt_service.revoke_token.assert_called_once_with(
                jti, 3600
            )  # exp_time calculated as 3600
            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)
            mock_jwt_service.generate_tokens.assert_called_once_with(user_id)

    class TestFailures:
        """Tests for failure cases"""

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_on_decode_error(
            self, auth_use_case, mock_jwt_service, mock_auth_repository, caplog
        ):
            """Test for token refresh failure due to decode error"""
            # Given
            refresh_token_str = "invalid_token"
            mock_jwt_service.decode_refresh_token.side_effect = UnauthorizedException(
                code=errors_code.INVALID_TOKEN
            )

            # When & Then
            with pytest.raises(UnauthorizedException) as excinfo:
                await auth_use_case.refresh_token(refresh_token_str)

            assert excinfo.value.code == errors_code.INVALID_TOKEN
            mock_jwt_service.decode_refresh_token.assert_called_once_with(
                refresh_token_str
            )
            mock_jwt_service.revoke_token.assert_not_called()
            mock_auth_repository.get_user_by_id.assert_not_called()
            mock_jwt_service.generate_tokens.assert_not_called()
            assert "Token refresh failed" in caplog.text

        @pytest.mark.asyncio
        @patch("core.use_cases.auth_use_case.datetime")
        async def test_should_raise_unauthorized_when_user_not_found(
            self,
            mock_datetime,
            auth_use_case,
            mock_jwt_service,
            mock_auth_repository,
            caplog,
        ):
            """Test for token refresh failure when user is not found"""
            # Given
            refresh_token_str = "old_refresh_token"
            user_id = 1
            jti = "old_jti"

            fixed_now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
            mock_datetime.now.return_value = fixed_now

            mock_old_payload = AsyncMock()
            mock_old_payload.user_id = user_id
            mock_old_payload.jti = jti
            mock_old_payload.exp = int(
                (fixed_now + timedelta(seconds=3600)).timestamp()
            )
            mock_jwt_service.decode_refresh_token.return_value = mock_old_payload

            mock_auth_repository.get_user_by_id.return_value = None  # User not found

            # When & Then
            with pytest.raises(UnauthorizedException) as excinfo:
                await auth_use_case.refresh_token(refresh_token_str)

            assert excinfo.value.code == errors_code.INVALID_TOKEN
            mock_jwt_service.decode_refresh_token.assert_called_once_with(
                refresh_token_str
            )
            mock_jwt_service.revoke_token.assert_called_once_with(jti, 3600)
            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)
            mock_jwt_service.generate_tokens.assert_not_called()
            assert "Token refresh failed" in caplog.text

        @pytest.mark.asyncio
        @patch("core.use_cases.auth_use_case.datetime")
        async def test_should_raise_internal_error_on_revoke_failure(
            self,
            mock_datetime,
            auth_use_case,
            mock_jwt_service,
            mock_auth_repository,
            caplog,
        ):
            """Test for internal server error during token revocation"""
            # Given
            refresh_token_str = "old_refresh_token"
            user_id = 1
            jti = "old_jti"

            fixed_now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
            mock_datetime.now.return_value = fixed_now

            mock_old_payload = AsyncMock()
            mock_old_payload.user_id = user_id
            mock_old_payload.jti = jti
            mock_old_payload.exp = int(
                (fixed_now + timedelta(seconds=3600)).timestamp()
            )
            mock_jwt_service.decode_refresh_token.return_value = mock_old_payload
            mock_jwt_service.revoke_token.side_effect = Exception("Revoke error")

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.refresh_token(refresh_token_str)

            assert "Unexpected error during token refresh" in caplog.text
            assert "Revoke error" in str(excinfo.value.__cause__)
            mock_jwt_service.decode_refresh_token.assert_called_once_with(
                refresh_token_str
            )
            mock_jwt_service.revoke_token.assert_called_once_with(jti, 3600)
            mock_auth_repository.get_user_by_id.assert_not_called()  # Not called because revoke fails first
            mock_jwt_service.generate_tokens.assert_not_called()

        @pytest.mark.asyncio
        @patch("core.use_cases.auth_use_case.datetime")
        async def test_should_raise_internal_error_on_get_user_failure(
            self,
            mock_datetime,
            auth_use_case,
            mock_jwt_service,
            mock_auth_repository,
            caplog,
        ):
            """Test for internal server error during user retrieval"""
            # Given
            refresh_token_str = "old_refresh_token"
            user_id = 1
            jti = "old_jti"

            fixed_now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
            mock_datetime.now.return_value = fixed_now

            mock_old_payload = AsyncMock()
            mock_old_payload.user_id = user_id
            mock_old_payload.jti = jti
            mock_old_payload.exp = int(
                (fixed_now + timedelta(seconds=3600)).timestamp()
            )
            mock_jwt_service.decode_refresh_token.return_value = mock_old_payload
            mock_auth_repository.get_user_by_id.side_effect = Exception("DB error")

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.refresh_token(refresh_token_str)

            assert "Unexpected error during token refresh" in caplog.text
            assert "DB error" in str(excinfo.value.__cause__)
            mock_jwt_service.decode_refresh_token.assert_called_once_with(
                refresh_token_str
            )
            mock_jwt_service.revoke_token.assert_called_once_with(jti, 3600)
            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)
            mock_jwt_service.generate_tokens.assert_not_called()

        @pytest.mark.asyncio
        @patch("core.use_cases.auth_use_case.datetime")
        async def test_should_raise_internal_error_on_generate_tokens_failure(
            self,
            mock_datetime,
            auth_use_case,
            mock_jwt_service,
            mock_auth_repository,
            caplog,
        ):
            """Test for internal server error during token generation"""
            # Given
            refresh_token_str = "old_refresh_token"
            user_id = 1
            jti = "old_jti"

            fixed_now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
            mock_datetime.now.return_value = fixed_now

            mock_old_payload = AsyncMock()
            mock_old_payload.user_id = user_id
            mock_old_payload.jti = jti
            mock_old_payload.exp = int(
                (fixed_now + timedelta(seconds=3600)).timestamp()
            )
            mock_jwt_service.decode_refresh_token.return_value = mock_old_payload

            user_found = UserEntity(
                id=user_id, email="test@example.com", password="hashed_password"
            )
            mock_auth_repository.get_user_by_id.return_value = user_found
            mock_jwt_service.generate_tokens.side_effect = Exception(
                "JWT generation error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.refresh_token(refresh_token_str)

            assert "Unexpected error during token refresh" in caplog.text
            assert "JWT generation error" in str(excinfo.value.__cause__)
            mock_jwt_service.decode_refresh_token.assert_called_once_with(
                refresh_token_str
            )
            mock_jwt_service.revoke_token.assert_called_once_with(jti, 3600)
            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)
            mock_jwt_service.generate_tokens.assert_called_once_with(user_id)

        @pytest.mark.asyncio
        @patch("core.use_cases.auth_use_case.datetime")
        async def test_should_raise_internal_error_when_user_id_is_none(
            self,
            mock_datetime,
            auth_use_case,
            mock_jwt_service,
            mock_auth_repository,
            caplog,
        ):
            """Test for internal server error when user ID is None"""
            # Given
            refresh_token_str = "old_refresh_token"
            user_id = 1
            jti = "old_jti"

            fixed_now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
            mock_datetime.now.return_value = fixed_now

            mock_old_payload = AsyncMock()
            mock_old_payload.user_id = user_id
            mock_old_payload.jti = jti
            mock_old_payload.exp = int(
                (fixed_now + timedelta(seconds=3600)).timestamp()
            )
            mock_jwt_service.decode_refresh_token.return_value = mock_old_payload

            user_found_no_id = UserEntity(
                id=None, email="test@example.com", password="hashed_password"
            )
            mock_auth_repository.get_user_by_id.return_value = user_found_no_id

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await auth_use_case.refresh_token(refresh_token_str)

            mock_jwt_service.decode_refresh_token.assert_called_once_with(
                refresh_token_str
            )
            mock_jwt_service.revoke_token.assert_called_once_with(jti, 3600)
            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)
            mock_jwt_service.generate_tokens.assert_not_called()  # Should not be called because user.id is None
            assert "Unexpected error during token refresh" in caplog.text
