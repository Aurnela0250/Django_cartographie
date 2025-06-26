import pytest

from core.entities.domain import DomainEntity
from core.entities.pagination import PaginatedResult
from presentation.exceptions import DatabaseException, InternalServerErrorException


class TestDomainFilterUseCase:
    """Unit tests for the filter method of DomainUseCase."""

    class TestSuccess:
        """Tests for success cases."""

        @pytest.mark.asyncio
        async def test_should_filter_domains_successfully(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
            pagination_params,
            domain_filters,
        ):
            """Test for successful domain filtering."""
            # Given
            sample_domain = domain_factory(id=1, name="Science")
            expected_result = PaginatedResult[DomainEntity](
                items=[sample_domain],
                total_items=1,
                page=1,
                per_page=10,
                total_pages=1,
            )
            mock_domain_repository.filter.return_value = expected_result

            # When
            result = await domain_use_case.filter(
                pagination_params=pagination_params, filters=domain_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 1
            assert result.items[0].name == "Science"
            mock_domain_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=domain_filters
            )

        @pytest.mark.asyncio
        async def test_should_return_empty_result_when_no_domains_match(
            self,
            domain_use_case,
            mock_domain_repository,
            pagination_params,
            domain_filters,
        ):
            """Test for domain filtering with no matching results."""
            # Given
            expected_result = PaginatedResult[DomainEntity](
                items=[],
                total_items=0,
                page=1,
                per_page=10,
                total_pages=0,
            )
            mock_domain_repository.filter.return_value = expected_result

            # When
            result = await domain_use_case.filter(
                pagination_params=pagination_params, filters=domain_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 0
            assert result.total_items == 0
            mock_domain_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=domain_filters
            )

        @pytest.mark.asyncio
        async def test_should_return_multiple_domains(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
            pagination_params,
            domain_filters,
        ):
            """Test for domain filtering returning multiple domains."""
            # Given
            domains = [
                domain_factory(id=1, name="Science"),
                domain_factory(id=2, name="Mathematics"),
            ]
            expected_result = PaginatedResult[DomainEntity](
                items=domains, total_items=2, page=1, per_page=10, total_pages=1
            )
            mock_domain_repository.filter.return_value = expected_result

            # When
            result = await domain_use_case.filter(
                pagination_params=pagination_params, filters=domain_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 2
            assert result.total_items == 2
            mock_domain_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=domain_filters
            )

        @pytest.mark.asyncio
        async def test_should_filter_domains_by_name(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
            pagination_params,
            domain_filters,
        ):
            """Test for successful domain filtering by name."""
            # Given
            domain_filters.name = "Science"
            sample_domain = domain_factory(id=1, name="Science")
            expected_result = PaginatedResult[DomainEntity](
                items=[sample_domain],
                total_items=1,
                page=1,
                per_page=10,
                total_pages=1,
            )
            mock_domain_repository.filter.return_value = expected_result

            # When
            result = await domain_use_case.filter(
                pagination_params=pagination_params, filters=domain_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 1
            assert result.items[0].name == "Science"
            mock_domain_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=domain_filters
            )

    class TestFailures:
        """Tests for failure cases."""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_filter_failure(
            self,
            domain_use_case,
            mock_domain_repository,
            pagination_params,
            domain_filters,
        ):
            """Test for error handling during domain filtering."""
            # Given
            repository_error = Exception("Database connection error")
            mock_domain_repository.filter.side_effect = repository_error

            # When & Then
            with pytest.raises(InternalServerErrorException) as exc_info:
                await domain_use_case.filter(
                    pagination_params=pagination_params, filters=domain_filters
                )

            # Verify that the exception is raised
            assert str(exc_info.value) == "Server error. Please try again later."
            mock_domain_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=domain_filters
            )

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_db_failure(
            self,
            domain_use_case,
            mock_domain_repository,
            pagination_params,
            domain_filters,
        ):
            """Test for error handling during domain retrieval on generic DB error."""
            # Given
            mock_domain_repository.filter.side_effect = DatabaseException(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.filter(
                    pagination_params=pagination_params,
                    filters=domain_filters,
                )
