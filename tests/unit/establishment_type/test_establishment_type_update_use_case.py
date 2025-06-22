import pytest

from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class TestEstablishmentTypeUpdateUseCase:
    """Tests unitaires pour la méthode update de EstablishmentTypeUseCase"""

    class TestSuccess:
        """Tests pour les cas de succès"""

        @pytest.mark.asyncio
        async def test_should_update_establishment_type_successfully(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la mise à jour réussie d'un type d'établissement"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            updated_data = establishment_type_factory(id=1, name="Collège")
            updated_result = establishment_type_factory(id=1, name="Collège")

            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.get_by_name.return_value = None
            mock_establishment_type_repository.update.return_value = updated_result

            # When
            result = await establishment_type_use_case.update(
                establishment_type_id, updated_data
            )

            # Then
            assert result == updated_result
            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_type_repository.update.assert_called_once_with(
                establishment_type_id, updated_data
            )

        @pytest.mark.asyncio
        async def test_should_update_establishment_type_with_same_name_successfully(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la mise à jour avec le même nom (réussie)"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            same_name_data = establishment_type_factory(id=1, name="Lycée")
            updated_result = establishment_type_factory(id=1, name="Lycée")

            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.update.return_value = updated_result

            # When
            result = await establishment_type_use_case.update(
                establishment_type_id, same_name_data
            )

            # Then
            assert result == updated_result
            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.get_by_name.assert_not_called()
            mock_establishment_type_repository.update.assert_called_once_with(
                establishment_type_id, same_name_data
            )

    class TestFailures:
        """Tests pour les cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_establishment_type_does_not_exist(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la mise à jour d'un type d'établissement inexistant"""
            # Given
            establishment_type_id = 999
            updated_data = establishment_type_factory(name="Collège")
            mock_establishment_type_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await establishment_type_use_case.update(
                    establishment_type_id, updated_data
                )

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.get_by_name.assert_not_called()
            mock_establishment_type_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_name_already_exists(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la mise à jour avec un nom déjà existant"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            updated_data = establishment_type_factory(id=1, name="Collège")
            other_establishment_type = establishment_type_factory(id=2, name="Collège")

            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.get_by_name.return_value = (
                other_establishment_type
            )

            # When & Then
            with pytest.raises(ConflictException):
                await establishment_type_use_case.update(
                    establishment_type_id, updated_data
                )

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_type_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la gestion d'erreur lors de la récupération"""
            # Given
            establishment_type_id = 1
            updated_data = establishment_type_factory(name="Collège")
            mock_establishment_type_repository.get.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.update(
                    establishment_type_id, updated_data
                )

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.get_by_name.assert_not_called()
            mock_establishment_type_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la gestion d'erreur lors de la vérification du nom"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            updated_data = establishment_type_factory(id=1, name="Collège")

            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.get_by_name.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.update(
                    establishment_type_id, updated_data
                )

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_type_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_update_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la gestion d'erreur lors de la mise à jour en base"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            updated_data = establishment_type_factory(id=1, name="Collège")

            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.get_by_name.return_value = None
            mock_establishment_type_repository.update.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.update(
                    establishment_type_id, updated_data
                )

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                updated_data.name
            )
            mock_establishment_type_repository.update.assert_called_once_with(
                establishment_type_id, updated_data
            )
