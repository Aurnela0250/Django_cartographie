import pytest

from presentation.exceptions import ConflictException, InternalServerErrorException


class TestAuthSignupUseCase:
    """Unit tests for the signup method of AuthUseCase"""

    class TestSuccess:
        """Tests for success cases"""

        @pytest.mark.asyncio
        async def test_should_signup_successfully(
            self, auth_use_case, mock_auth_repository, mock_bcrypt_service, user_factory
        ):
            """Test for successful user signup"""
            # Given
            email = "test@example.com"
            password = "password123"
            expected_user = user_factory(id=1, email=email, password="hashed_password")
            mock_auth_repository.get_user_by_email.return_value = (
                None  # No existing user
            )
            mock_bcrypt_service.hash_password.return_value = "hashed_password"
            mock_auth_repository.signup.return_value = expected_user

            # When
            result = await auth_use_case.signup(email, password)

            # Then
            assert result == expected_user
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_bcrypt_service.hash_password.assert_called_once_with(password)
            mock_auth_repository.signup.assert_called_once_with(
                email=email, hashed_password="hashed_password"
            )

    class TestFailures:
        """Tests for failure cases"""

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_email_exists(
            self, auth_use_case, mock_auth_repository, user_factory, caplog
        ):
            """Test for signup with existing email"""
            # Given
            email = "existing@example.com"
            password = "password123"
            mock_auth_repository.get_user_by_email.return_value = user_factory(
                id=1, email=email, password="hashed_password"
            )

            # When & Then
            with pytest.raises(ConflictException):
                await auth_use_case.signup(email, password)

            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_auth_repository.signup.assert_not_called()
            assert "Signup attempt with existing account" in caplog.text

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
                await auth_use_case.signup(email, password)

            assert "Unexpected error during signup" in caplog.text
            assert "DB error" in str(excinfo.value.__cause__)
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_auth_repository.signup.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_hash_password_failure(
            self, auth_use_case, mock_auth_repository, mock_bcrypt_service, caplog
        ):
            """Test for internal server error during password hashing"""
            # Given
            email = "test@example.com"
            password = "password123"
            mock_auth_repository.get_user_by_email.return_value = (
                None  # No existing user
            )
            mock_bcrypt_service.hash_password.side_effect = Exception("Hashing error")

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.signup(email, password)

            assert "Unexpected error during signup" in caplog.text
            assert "Hashing error" in str(excinfo.value.__cause__)
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_bcrypt_service.hash_password.assert_called_once_with(password)
            mock_auth_repository.signup.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_signup_failure(
            self, auth_use_case, mock_auth_repository, mock_bcrypt_service, caplog
        ):
            """Test for internal server error during user signup"""
            # Given
            email = "test@example.com"
            password = "password123"
            mock_auth_repository.get_user_by_email.return_value = (
                None  # No existing user
            )
            mock_bcrypt_service.hash_password.return_value = "hashed_password"
            mock_auth_repository.signup.side_effect = Exception("Signup DB error")

            # When & Then
            with pytest.raises(InternalServerErrorException) as excinfo:
                await auth_use_case.signup(email, password)

            assert "Unexpected error during signup" in caplog.text
            assert "Signup DB error" in str(excinfo.value.__cause__)
            mock_auth_repository.get_user_by_email.assert_called_once_with(email)
            mock_auth_repository.signup.assert_called_once_with(
                email=email, hashed_password="hashed_password"
            )
