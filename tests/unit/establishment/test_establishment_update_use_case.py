import pytest

from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class TestEstablishmentUpdateUseCase:
    """Unit tests for the update method of EstablishmentUseCase"""

    class TestSuccess:
        """Tests for successful update"""

        @pytest.mark.asyncio
        async def test_should_update_establishment_successfully(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for successful establishment update"""
            # Given
            establishment_id = 1
            existing_establishment = establishment_factory(
                id=establishment_id, name="Old Name"
            )
            updated_data = establishment_factory(name="Updated Name")
            updated_establishment = establishment_factory(
                id=establishment_id, name="Updated Name"
            )

            mock_establishment_repository.get.return_value = existing_establishment
            mock_establishment_repository.get_by_name.return_value = (
                None  # No conflict with new name
            )
            mock_establishment_repository.update.return_value = updated_establishment

            # When
            result = await establishment_use_case.update(establishment_id, updated_data)

            # Then
            assert result == updated_establishment
            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_repository.update.assert_called_once_with(
                establishment_id, updated_data
            )

        @pytest.mark.asyncio
        async def test_should_update_establishment_with_same_name_successfully(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for successful establishment update when name is not changed"""
            # Given
            establishment_id = 1
            existing_establishment = establishment_factory(
                id=establishment_id, name="Same Name"
            )
            updated_data = establishment_factory(name="Same Name")
            updated_establishment = establishment_factory(
                id=establishment_id, name="Same Name"
            )

            mock_establishment_repository.get.return_value = existing_establishment
            # get_by_name should not be called if name is the same
            mock_establishment_repository.update.return_value = updated_establishment

            # When
            result = await establishment_use_case.update(establishment_id, updated_data)

            # Then
            assert result == updated_establishment
            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.get_by_name.assert_not_called()
            mock_establishment_repository.update.assert_called_once_with(
                establishment_id, updated_data
            )

    class TestFailures:
        """Tests for update failures"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_establishment_to_update_does_not_exist(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for update when establishment does not exist"""
            # Given
            establishment_id = 999
            updated_data = establishment_factory(name="Updated Name")
            mock_establishment_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await establishment_use_case.update(establishment_id, updated_data)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.get_by_name.assert_not_called()
            mock_establishment_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_new_name_already_exists(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for update when new name conflicts with existing establishment"""
            # Given
            establishment_id = 1
            existing_establishment = establishment_factory(
                id=establishment_id, name="Old Name"
            )
            updated_data = establishment_factory(name="Conflicting Name")
            conflicting_establishment = establishment_factory(
                id=2, name="Conflicting Name"
            )

            mock_establishment_repository.get.return_value = existing_establishment
            mock_establishment_repository.get_by_name.return_value = (
                conflicting_establishment
            )

            # When & Then
            with pytest.raises(ConflictException):
                await establishment_use_case.update(establishment_id, updated_data)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure_during_update(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for error handling during initial get in update"""
            # Given
            establishment_id = 1
            updated_data = establishment_factory(name="Updated Name")
            mock_establishment_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.update(establishment_id, updated_data)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.get_by_name.assert_not_called()
            mock_establishment_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure_during_update(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for error handling during name conflict check in update"""
            # Given
            establishment_id = 1
            existing_establishment = establishment_factory(
                id=establishment_id, name="Old Name"
            )
            updated_data = establishment_factory(name="Updated Name")
            mock_establishment_repository.get.return_value = existing_establishment
            mock_establishment_repository.get_by_name.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.update(establishment_id, updated_data)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_update_failure(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for error handling during actual update operation"""
            # Given
            establishment_id = 1
            existing_establishment = establishment_factory(
                id=establishment_id, name="Old Name"
            )
            updated_data = establishment_factory(name="Updated Name")
            mock_establishment_repository.get.return_value = existing_establishment
            mock_establishment_repository.get_by_name.return_value = None
            mock_establishment_repository.update.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.update(establishment_id, updated_data)

            mock_establishment_repository.get.assert_called_once_with(establishment_id)
            mock_establishment_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_repository.update.assert_called_once_with(
                establishment_id, updated_data
            )
