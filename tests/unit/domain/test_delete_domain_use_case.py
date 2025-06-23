import pytest
from unittest.mock import AsyncMock

from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseException,
)
from presentation.exceptions import (
    InternalServerErrorException,
    NotFoundException,
)


class TestDeleteDomainUseCase:
    """Unit tests for the delete method of DomainUseCase."""

    class TestFailures:
        """Tests for failure cases."""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_repo_raises_does_not_exist(
            self, domain_use_case, mock_domain_repository
        ):
            """
            Should raise NotFoundException when domain_repository.delete
            raises DatabaseDoesNotExistException.
            """
            # Given
            domain_id = 1
            mock_domain_repository.delete = AsyncMock(
                side_effect=DatabaseDoesNotExistException
            )

            # When & Then
            with pytest.raises(NotFoundException):
                await domain_use_case.delete(domain_id)

            mock_domain_repository.delete.assert_called_once_with(domain_id)

        @pytest.mark.asyncio
        async def test_should_raise_internal_server_error_on_db_exception(
            self, domain_use_case, mock_domain_repository
        ):
            """
            Should raise InternalServerErrorException when domain_repository.delete
            raises DatabaseException.
            """
            # Given
            domain_id = 1
            mock_domain_repository.delete = AsyncMock(side_effect=DatabaseException)

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.delete(domain_id)

            mock_domain_repository.delete.assert_called_once_with(domain_id)

    class TestSuccess:
        """Tests for success cases."""

        @pytest.mark.asyncio
        async def test_should_return_true_on_successful_deletion(
            self, domain_use_case, mock_domain_repository
        ):
            """Should return True when the deletion is successful."""
            # Given
            domain_id = 1
            mock_domain_repository.delete = AsyncMock(return_value=True)

            # When
            result = await domain_use_case.delete(domain_id)

            # Then
            assert result is True
            mock_domain_repository.delete.assert_called_once_with(domain_id)
