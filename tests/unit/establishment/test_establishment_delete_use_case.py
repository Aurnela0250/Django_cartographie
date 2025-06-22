import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestEstablishmentDeleteUseCase:
    """Unit tests for the delete method of EstablishmentUseCase"""

    class TestSuccess:
        """Tests for successful deletion"""

        @pytest.mark.asyncio
        async def test_should_delete_establishment_successfully(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for successful establishment deletion"""
            # Given
            establishment_id = 1
            existing_establishment = establishment_factory(id=establishment_id)
            mock_establishment_repository.get.return_value = existing_establishment
            mock_establishment_repository.delete.return_value = True

            # When
            result = await establishment_use_case.delete(establishment_id)

            # Then
            assert result is True
            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.delete.assert_called_once_with(
                establishment_id
            )

    class TestFailures:
        """Tests for deletion failures"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_establishment_to_delete_does_not_exist(
            self, establishment_use_case, mock_establishment_repository
        ):
            """Test for deletion when establishment does not exist"""
            # Given
            establishment_id = 999
            mock_establishment_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await establishment_use_case.delete(establishment_id)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure_during_delete(
            self, establishment_use_case, mock_establishment_repository
        ):
            """Test for error handling during initial get in delete"""
            # Given
            establishment_id = 1
            mock_establishment_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.delete(establishment_id)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_delete_failure(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for error handling during actual delete operation"""
            # Given
            establishment_id = 1
            existing_establishment = establishment_factory(id=establishment_id)
            mock_establishment_repository.get.return_value = existing_establishment
            mock_establishment_repository.delete.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.delete(establishment_id)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.delete.assert_called_once_with(
                establishment_id
            )
