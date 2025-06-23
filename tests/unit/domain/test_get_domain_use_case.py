import pytest

from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseException,
    InternalServerErrorException,
    NotFoundException,
)
from tests.factories import DomainFactory


class TestDomainGetUseCase:
    """Unit tests for the get method of DomainUseCase."""

    @pytest.mark.asyncio
    async def test_should_get_domain_successfully(
        self, domain_use_case, mock_domain_repository, domain_factory
    ):
        """Test for successful domain retrieval."""
        # Given
        expected_domain = DomainFactory.build()
        mock_domain_repository.get.return_value = expected_domain

        # When
        result = await domain_use_case.get(expected_domain.id)

        # Then
        assert result == expected_domain
        mock_domain_repository.get.assert_called_once_with(expected_domain.id)

    @pytest.mark.asyncio
    async def test_should_raise_not_found_when_domain_does_not_exist(
        self, domain_use_case, mock_domain_repository
    ):
        """Test for retrieval of a non-existent domain."""
        # Given
        domain_id = 999
        mock_domain_repository.get.side_effect = DatabaseDoesNotExistException(
            "Domain not found"
        )

        # When & Then
        with pytest.raises(NotFoundException):
            await domain_use_case.get(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_should_raise_internal_error_on_db_failure(
        self, domain_use_case, mock_domain_repository
    ):
        """Test for error handling during domain retrieval on generic DB error."""
        # Given
        domain_id = 1
        mock_domain_repository.get.side_effect = DatabaseException("Database error")

        # When & Then
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.get(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_should_raise_internal_error_on_unexpected_failure(
        self, domain_use_case, mock_domain_repository
    ):
        """Test for error handling during domain retrieval on unexpected error."""
        # Given
        domain_id = 1
        mock_domain_repository.get.side_effect = Exception("Unexpected error")

        # When & Then
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.get(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)
