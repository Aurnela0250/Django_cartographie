import pytest

from core.entities.filters import EstablishmentFilters
from presentation.exceptions import InternalServerErrorException


class TestEstablishmentFilterUseCase:
    """Tests for the filter method"""

    class TestSuccess:
        """Tests for successful filtering of establishments"""

        @pytest.mark.asyncio
        async def test_should_filter_establishments_successfully(
            self,
            establishment_use_case,
            mock_establishment_repository,
            pagination_params_factory,
            paginated_result_factory,
        ):
            """Test for successful filtering of establishments"""
            # Given
            pagination_params = pagination_params_factory()
            filters = EstablishmentFilters(name="Test")
            expected_paginated_result = paginated_result_factory(total_items=2)
            mock_establishment_repository.filter.return_value = (
                expected_paginated_result
            )

            # When
            result = await establishment_use_case.filter(pagination_params, filters)

            # Then
            assert result == expected_paginated_result
            mock_establishment_repository.filter.assert_called_once_with(
                pagination_params=pagination_params,
                filters=filters,
            )

    class TestFailures:
        """Tests for filter failures"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_filter_failure(
            self,
            establishment_use_case,
            mock_establishment_repository,
            pagination_params_factory,
        ):
            """Test for error handling during filter"""
            # Given
            pagination_params = pagination_params_factory()
            filters = EstablishmentFilters(name="Test")
            mock_establishment_repository.filter.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.filter(pagination_params, filters)

            mock_establishment_repository.filter.assert_called_once_with(
                pagination_params=pagination_params,
                filters=filters,
            )
