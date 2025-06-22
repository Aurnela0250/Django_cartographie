import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestEstablishmentTypeGetUseCase:
    """Tests unitaires pour la méthode get de EstablishmentTypeUseCase"""

    class TestSuccess:
        """Tests pour les cas de succès"""

        @pytest.mark.asyncio
        async def test_should_get_establishment_type_successfully(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
        ):
            """Test pour la récupération réussie d'un type d'établissement"""
            # Given
            establishment_type_id = 1
            expected_establishment_type = establishment_type_factory(id=1, name="Lycée")
            mock_establishment_type_repository.get.return_value = (
                expected_establishment_type
            )

            # When
            result = await establishment_type_use_case.get(establishment_type_id)

            # Then
            assert result == expected_establishment_type
            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )

    class TestFailures:
        """Tests pour les cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_establishment_type_does_not_exist(
            self, establishment_type_use_case, mock_establishment_type_repository
        ):
            """Test pour la récupération d'un type d'établissement inexistant"""
            # Given
            establishment_type_id = 999
            mock_establishment_type_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await establishment_type_use_case.get(establishment_type_id)

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_repository_failure(
            self, establishment_type_use_case, mock_establishment_type_repository
        ):
            """Test pour la gestion d'erreur lors de la récupération en base"""
            # Given
            establishment_type_id = 1
            mock_establishment_type_repository.get.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.get(establishment_type_id)

            mock_establishment_type_repository.get.assert_called_once_with(
                establishment_type_id
            )
