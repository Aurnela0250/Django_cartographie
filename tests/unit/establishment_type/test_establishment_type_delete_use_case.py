import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestEstablishmentTypeDeleteUseCase:
    """Tests unitaires pour la méthode delete de EstablishmentTypeUseCase"""

    class TestSuccess:
        """Tests pour les cas de succès"""

        @pytest.mark.asyncio
        async def test_should_delete_establishment_type_successfully(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la suppression réussie d'un type d'établissement"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.delete.return_value = True

            # When
            result = await establishment_type_use_case.delete(establishment_type_id)

            # Then
            assert result is True
            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.delete.assert_called_once_with(
                establishment_type_id
            )

        @pytest.mark.asyncio
        async def test_should_return_false_when_deletion_fails(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour l'échec de suppression qui retourne False"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.delete.return_value = False

            # When
            result = await establishment_type_use_case.delete(establishment_type_id)

            # Then
            assert result is False
            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.delete.assert_called_once_with(
                establishment_type_id
            )

    class TestFailures:
        """Tests pour les cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_establishment_type_does_not_exist(
            self, establishment_type_use_case, mock_establishment_type_repository
        ):
            """Test pour la suppression d'un type d'établissement inexistant"""
            # Given
            establishment_type_id = 999
            mock_establishment_type_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await establishment_type_use_case.delete(establishment_type_id)

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self, establishment_type_use_case, mock_establishment_type_repository
        ):
            """Test pour la gestion d'erreur lors de la vérification d'existence"""
            # Given
            establishment_type_id = 1
            mock_establishment_type_repository.get.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.delete(establishment_type_id)

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_delete_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la gestion d'erreur lors de la suppression en base"""
            # Given
            establishment_type_id = 1
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            mock_establishment_type_repository.get.return_value = (
                existing_establishment_type
            )
            mock_establishment_type_repository.delete.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.delete(establishment_type_id)

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
            mock_establishment_type_repository.delete.assert_called_once_with(
                establishment_type_id
            )
