import pytest

from presentation.exceptions import ConflictException, InternalServerErrorException


class TestEstablishmentTypeCreateUseCase:
    """Tests unitaires pour la méthode create de EstablishmentTypeUseCase"""

    class TestSuccess:
        """Tests pour les cas de succès"""

        @pytest.mark.asyncio
        async def test_should_create_establishment_type_successfully(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la création réussie d'un type d'établissement"""
            # Given
            new_establishment_type = establishment_type_factory(name="Lycée")
            created_establishment_type = establishment_type_factory(id=1, name="Lycée")
            mock_establishment_type_repository.get_by_name.return_value = None
            mock_establishment_type_repository.create.return_value = (
                created_establishment_type
            )

            # When
            result = await establishment_type_use_case.create(new_establishment_type)

            # Then
            assert result == created_establishment_type
            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                new_establishment_type.name
            )
            mock_establishment_type_repository.create.assert_called_once_with(
                new_establishment_type
            )

    class TestFailures:
        """Tests pour les cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_establishment_type_already_exists(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la création d'un type d'établissement avec nom déjà existant"""
            # Given
            new_establishment_type = establishment_type_factory(name="Lycée")
            existing_establishment_type = establishment_type_factory(id=1, name="Lycée")
            mock_establishment_type_repository.get_by_name.return_value = (
                existing_establishment_type
            )

            # When & Then
            with pytest.raises(ConflictException):
                await establishment_type_use_case.create(new_establishment_type)

            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                new_establishment_type.name
            )
            mock_establishment_type_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la gestion d'erreur lors de la vérification d'existence"""
            # Given
            new_establishment_type = establishment_type_factory(name="Lycée")
            mock_establishment_type_repository.get_by_name.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.create(new_establishment_type)

            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                new_establishment_type.name
            )
            mock_establishment_type_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_create_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la gestion d'erreur lors de la création en base"""
            # Given
            new_establishment_type = establishment_type_factory(name="Lycée")
            mock_establishment_type_repository.get_by_name.return_value = None
            mock_establishment_type_repository.create.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.create(new_establishment_type)

            mock_establishment_type_repository.get_by_name.assert_called_once_with(
                new_establishment_type.name
            )
            mock_establishment_type_repository.create.assert_called_once_with(
                new_establishment_type
            )
