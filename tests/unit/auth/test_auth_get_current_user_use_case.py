import pytest

from presentation.exceptions import InternalServerErrorException, UnauthorizedException


class TestAuthGetCurrentUserUseCase:
    """Unit tests for the get_current_user method of AuthUseCase"""

    class TestSuccess:
        """Tests for success cases"""

        @pytest.mark.asyncio
        async def test_should_get_current_user_successfully(
            self,
            auth_use_case,
            mock_auth_repository,
            user_factory,
        ):
            """Test for successful retrieval of current user"""
            # Given
            user_id = 1
            sample_user = user_factory(
                id=user_id, email="test@example.com", password="hashed_password"
            )
            mock_auth_repository.get_user_by_id.return_value = sample_user

            # When
            result = await auth_use_case.get_current_user(user_id)

            # Then
            assert result == sample_user
            assert result.id == user_id
            assert result.email == "test@example.com"
            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)

    class TestFailures:
        """Tests for failure cases"""

        @pytest.mark.asyncio
        async def test_should_raise_unauthorized_when_user_not_found(
            self, auth_use_case, mock_auth_repository
        ):
            """Test for retrieval with non-existent user"""
            # Given
            user_id = 999
            mock_auth_repository.get_user_by_id.return_value = None

            # When & Then
            with pytest.raises(UnauthorizedException):
                await auth_use_case.get_current_user(user_id)

            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_repository_failure(
            self, auth_use_case, mock_auth_repository
        ):
            """Test for error handling during user retrieval"""
            # Given
            user_id = 1
            mock_auth_repository.get_user_by_id.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await auth_use_case.get_current_user(user_id)

            mock_auth_repository.get_user_by_id.assert_called_once_with(user_id)

        @pytest.mark.asyncio
        async def test_should_handle_multiple_user_ids(
            self, auth_use_case, mock_auth_repository, user_factory
        ):
            """Test for retrieval with different user IDs"""
            # Given
            user_ids = [1, 2, 3, 100]
            users = [
                user_factory(id=uid, email=f"user{uid}@example.com", password="hashed")
                for uid in user_ids
            ]

            def get_user_side_effect(uid):
                for user in users:
                    if user.id == uid:
                        return user
                return None

            mock_auth_repository.get_user_by_id.side_effect = get_user_side_effect

            # When & Then
            for i, user_id in enumerate(user_ids):
                result = await auth_use_case.get_current_user(user_id)
                assert result == users[i]
                assert result.id == user_id
                assert result.email == f"user{user_id}@example.com"

            assert mock_auth_repository.get_user_by_id.call_count == len(user_ids)
