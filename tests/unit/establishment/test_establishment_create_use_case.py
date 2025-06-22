import pytest

from presentation.exceptions import ConflictException, InternalServerErrorException


class TestEstablishmentCreateUseCase:
    """Unit tests for the create method of EstablishmentUseCase"""

    class TestSuccess:
        """Tests for successful creation"""

        @pytest.mark.asyncio
        async def test_should_create_establishment_successfully(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for successful establishment creation"""
            # Given
            new_establishment = establishment_factory(name="New Establishment")
            created_establishment = establishment_factory(
                id=1, name="New Establishment"
            )
            mock_establishment_repository.get_by_name.return_value = None
            mock_establishment_repository.create.return_value = created_establishment

            # When
            result = await establishment_use_case.create(new_establishment)

            # Then
            assert result == created_establishment
            mock_establishment_repository.get_by_name.assert_called_once_with(
                new_establishment.name
            )
            mock_establishment_repository.create.assert_called_once_with(
                new_establishment
            )

    class TestFailures:
        """Tests for creation failures"""

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_establishment_already_exists(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for establishment creation with already existing name"""
            # Given
            new_establishment = establishment_factory(name="Existing Establishment")
            existing_establishment = establishment_factory(
                id=1, name="Existing Establishment"
            )
            mock_establishment_repository.get_by_name.return_value = (
                existing_establishment
            )

            # When & Then
            with pytest.raises(ConflictException):
                await establishment_use_case.create(new_establishment)

            mock_establishment_repository.get_by_name.assert_called_once_with(
                new_establishment.name
            )
            mock_establishment_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for error handling during existence check"""
            # Given
            new_establishment = establishment_factory(name="New Establishment")
            mock_establishment_repository.get_by_name.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.create(new_establishment)

            mock_establishment_repository.get_by_name.assert_called_once_with(
                new_establishment.name
            )
            mock_establishment_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_create_failure(
            self,
            establishment_use_case,
            mock_establishment_repository,
            establishment_factory,
        ):
            """Test for error handling during database creation"""
            # Given
            new_establishment = establishment_factory(name="New Establishment")
            mock_establishment_repository.get_by_name.return_value = None
            mock_establishment_repository.create.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_use_case.create(new_establishment)

            mock_establishment_repository.get_by_name.assert_called_once_with(
                new_establishment.name
            )
            mock_establishment_repository.create.assert_called_once_with(
                new_establishment
            )
