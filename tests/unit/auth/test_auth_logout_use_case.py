from unittest.mock import MagicMock, patch

import pytest

from presentation.exceptions import InternalServerErrorException, UnauthorizedException


class TestAuthLogoutUseCase:
    """Unit tests for the logout method of AuthUseCase"""

    class TestSuccess:
        """Tests for success cases"""

        @pytest.mark.asyncio
        async def test_should_logout_successfully(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for successful logout"""
            # Arrange
            access_token = "valid_access_token"
            refresh_token = "valid_refresh_token"

            fixed_time = 1721600000

            # Mock token payloads
            access_payload = MagicMock()
            access_payload.jti = "jti-access"
            access_payload.exp = fixed_time + 1000  # Token expires in 1000 seconds

            refresh_payload = MagicMock()
            refresh_payload.jti = "jti-refresh"
            refresh_payload.exp = fixed_time + 2000  # Token expires in 2000 seconds

            mock_jwt_service.decode_access_token.return_value = access_payload
            mock_jwt_service.decode_refresh_token.return_value = refresh_payload
            mock_jwt_service.revoke_token.return_value = None

            # Mock datetime.now to return a fixed time
            with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
                mock_now = MagicMock()
                mock_now.timestamp.return_value = fixed_time
                mock_datetime.now.return_value = mock_now

                # Act
                result = await auth_use_case.logout(access_token, refresh_token)

                # Assert
                assert result is None
                mock_jwt_service.decode_access_token.assert_awaited_once_with(
                    access_token
                )
                mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                    refresh_token
                )
                mock_jwt_service.revoke_token.assert_any_await("jti-access", 1000)
                mock_jwt_service.revoke_token.assert_any_await("jti-refresh", 2000)
                assert mock_jwt_service.revoke_token.await_count == 2

        @pytest.mark.asyncio
        async def test_should_handle_empty_tokens(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for logout with empty tokens"""
            # Arrange
            access_token = ""
            refresh_token = ""

            # Mock expired token payloads
            fixed_time = 1721600000

            access_payload = MagicMock()
            access_payload.jti = "jti-access"
            access_payload.exp = fixed_time - 1000  # Token already expired

            refresh_payload = MagicMock()
            refresh_payload.jti = "jti-refresh"
            refresh_payload.exp = fixed_time - 1000  # Token already expired

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
                mock_jwt_service.decode_access_token.assert_awaited_once_with(
                    access_token
                )
                mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                    refresh_token
                )
                mock_jwt_service.revoke_token.assert_not_awaited()

        @pytest.mark.asyncio
        async def test_should_handle_none_tokens(self, auth_use_case, mock_jwt_service):
            """Test for logout with None tokens"""
            # Arrange
            access_token = None
            refresh_token = None

            # Mock valid token payloads
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
                mock_jwt_service.decode_access_token.assert_awaited_once_with(
                    access_token
                )
                mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                    refresh_token
                )
                assert mock_jwt_service.revoke_token.await_count == 2

        @pytest.mark.asyncio
        async def test_should_handle_partial_tokens(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for logout with only one of the tokens"""
            # Arrange - Test with only access_token
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
                mock_jwt_service.decode_access_token.assert_awaited_once_with(
                    access_token
                )
                mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                    refresh_token
                )
                assert mock_jwt_service.revoke_token.await_count == 2

            # Reset mock for the second test
            mock_jwt_service.reset_mock()
            mock_jwt_service.decode_access_token.return_value = access_payload
            mock_jwt_service.decode_refresh_token.return_value = refresh_payload

            # Arrange - Test with only refresh_token
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
                mock_jwt_service.decode_access_token.assert_awaited_once_with(
                    access_token
                )
                mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                    refresh_token
                )
                assert mock_jwt_service.revoke_token.await_count == 2

    class TestFailures:
        """Tests for failure cases"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_generic_decode_failure(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for generic error handling during token decode"""
            # Arrange
            access_token = "valid_access_token"
            refresh_token = "valid_refresh_token"

            mock_jwt_service.decode_access_token.side_effect = Exception(
                "Unexpected error during token decode"
            )

            # Act & Assert
            with pytest.raises(InternalServerErrorException):
                await auth_use_case.logout(access_token, refresh_token)

            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_on_access_token_decode_failure(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for UnauthorizedException during access token decode"""
            # Arrange
            access_token = "invalid_access_token"
            refresh_token = "valid_refresh_token"

            mock_jwt_service.decode_access_token.side_effect = UnauthorizedException(
                code="TOKEN_EXPIRED", message="Token has expired"
            )

            # Act & Assert
            with pytest.raises(UnauthorizedException):
                await auth_use_case.logout(access_token, refresh_token)

            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)
            mock_jwt_service.decode_refresh_token.assert_not_awaited()

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_on_refresh_token_decode_failure(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for UnauthorizedException during refresh token decode"""
            # Arrange
            access_token = "valid_access_token"
            refresh_token = "invalid_refresh_token"

            fixed_time = 1721600000

            access_payload = MagicMock()
            access_payload.jti = "jti-access"
            access_payload.exp = fixed_time + 1000

            mock_jwt_service.decode_access_token.return_value = access_payload
            mock_jwt_service.decode_refresh_token.side_effect = UnauthorizedException(
                code="TOKEN_REVOKED", message="Token has been revoked"
            )

            with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
                mock_now = MagicMock()
                mock_now.timestamp.return_value = fixed_time
                mock_datetime.now.return_value = mock_now

                # Act & Assert
                with pytest.raises(UnauthorizedException):
                    await auth_use_case.logout(access_token, refresh_token)

                mock_jwt_service.decode_access_token.assert_awaited_once_with(
                    access_token
                )
                mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                    refresh_token
                )
                mock_jwt_service.revoke_token.assert_not_awaited()

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_on_both_tokens_decode_failure(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for UnauthorizedException on both tokens decode failure"""
            # Arrange
            access_token = "invalid_access_token"
            refresh_token = "invalid_refresh_token"

            mock_jwt_service.decode_access_token.side_effect = UnauthorizedException(
                code="INVALID_TOKEN", message="Invalid access token"
            )
            mock_jwt_service.decode_refresh_token.side_effect = UnauthorizedException(
                code="INVALID_TOKEN", message="Invalid refresh token"
            )

            # Act & Assert
            with pytest.raises(UnauthorizedException):
                await auth_use_case.logout(access_token, refresh_token)

            mock_jwt_service.decode_access_token.assert_awaited_once_with(access_token)
            mock_jwt_service.decode_refresh_token.assert_not_awaited()

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_on_access_token_valid_refresh_token_invalid(
            self, auth_use_case, mock_jwt_service
        ):
            """Test for UnauthorizedException when access token is valid but refresh token is invalid"""
            # Arrange
            access_token = "valid_access_token"
            refresh_token = "expired_refresh_token"

            fixed_time = 1721600000

            access_payload = MagicMock()
            access_payload.jti = "jti-access"
            access_payload.exp = fixed_time + 1000

            mock_jwt_service.decode_access_token.return_value = access_payload
            mock_jwt_service.decode_refresh_token.side_effect = UnauthorizedException(
                code="TOKEN_EXPIRED", message="Refresh token has expired"
            )

            with patch("core.use_cases.auth_use_case.datetime") as mock_datetime:
                mock_now = MagicMock()
                mock_now.timestamp.return_value = fixed_time
                mock_datetime.now.return_value = mock_now

                # Act & Assert
                with pytest.raises(UnauthorizedException):
                    await auth_use_case.logout(access_token, refresh_token)

                mock_jwt_service.decode_access_token.assert_awaited_once_with(
                    access_token
                )
                mock_jwt_service.decode_refresh_token.assert_awaited_once_with(
                    refresh_token
                )
                mock_jwt_service.revoke_token.assert_not_awaited()
