import pytest

from presentation.exceptions import InternalServerErrorException


class TestEstablishmentGetAllUseCase:
    """Tests for the get_all method"""

    class TestSuccess:
        """Tests for successful retrieval of all establishments"""

        @pytest.mark.asyncio
        async def test_should_get_all_establishments_successfully(
            self,
            establishment_use_case,
            mock_establishment_repository,
            pagination_params_factory,
            paginated_result_factory,
        ):
            """Test for successful retrieval of all establishments"""
            # Given
            pagination_params = pagination_params_factory()
            expected_paginated_result = paginated_result_factory(total_items=5)
            mock_establishment_repository.get_all.return_value = (
                expected_paginated_result
            )

            # When
            result = await establishment_use_case.get_all(pagination_params)

            # Then
            assert result == expected_paginated_result
            mock_establishment_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )

    class TestFailures:
        """Tests for get_all failures"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_all_failure(
            self,
            establishment_use_case,
            mock_establishment_repository,
            pagination_params_factory,
        ):
            """Test for error handling during get_all"""
            # Given
            pagination_params = pagination_params_factory()
            mock_establishment_repository.get_all.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.get_all(pagination_params)

            mock_establishment_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )
