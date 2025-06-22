import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestEstablishmentGetUseCase:
    """Unit tests for the get method of EstablishmentUseCase"""

    class TestSuccess:
        """Tests for successful retrieval"""

        @pytest.mark.asyncio
        async def test_should_get_establishment_successfully(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for successful establishment retrieval"""
            # Given
            establishment_id = 1
            expected_establishment = establishment_factory(id=establishment_id)
            mock_establishment_repository.get.return_value = expected_establishment

            # When
            result = await establishment_use_case.get(establishment_id)

            # Then
            assert result == expected_establishment
            mock_establishment_repository.get.assert_called_once_with(establishment_id)

    class TestFailures:
        """Tests for retrieval failures"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_establishment_does_not_exist(
            self, establishment_use_case, mock_establishment_repository
        ):
            """Test for establishment retrieval when not found"""
            # Given
            establishment_id = 999
            mock_establishment_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await establishment_use_case.get(establishment_id)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self, establishment_use_case, mock_establishment_repository
        ):
            """Test for error handling during retrieval"""
            # Given
            establishment_id = 1
            mock_establishment_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.get(establishment_id)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
