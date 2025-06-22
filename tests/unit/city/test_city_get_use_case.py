import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestCityGetUseCase:
    """Tests unitaires pour la méthode get de CityUseCase"""

    class TestSuccess:
        """Tests des cas de succès"""

        @pytest.mark.asyncio
        async def test_should_get_city_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de récupération de ville réussie"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            mock_city_repository.get.return_value = existing_city

            # When
            result = await city_use_case.get(city_id)

            # Then
            assert result == existing_city
            mock_city_repository.get.assert_called_once_with(city_id)

    class TestFailures:
        """Tests des cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_city_does_not_exist(
            self, city_use_case, mock_city_repository
        ):
            """Test de récupération d'une ville inexistante"""
            # Given
            city_id = 999
            mock_city_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await city_use_case.get(city_id)

            mock_city_repository.get.assert_called_once_with(city_id)

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_repository_failure(
            self, city_use_case, mock_city_repository
        ):
            """Test de gestion d'erreur lors de la récupération en base"""
            # Given
            city_id = 1
            mock_city_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.get(city_id)

            mock_city_repository.get.assert_called_once_with(city_id)
