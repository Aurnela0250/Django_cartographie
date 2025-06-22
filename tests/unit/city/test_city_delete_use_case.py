import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestCityDeleteUseCase:
    """Tests unitaires pour la méthode delete de CityUseCase"""

    class TestSuccess:
        """Tests des cas de succès"""

        @pytest.mark.asyncio
        async def test_should_delete_city_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de suppression de ville réussie"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            mock_city_repository.get.return_value = existing_city
            mock_city_repository.delete.return_value = True

            # When
            result = await city_use_case.delete(city_id)

            # Then
            assert result is True
            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.delete.assert_called_once_with(city_id)

        @pytest.mark.asyncio
        async def test_should_return_false_when_delete_fails(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de suppression qui retourne False (échec de suppression)"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            mock_city_repository.get.return_value = existing_city
            mock_city_repository.delete.return_value = False

            # When
            result = await city_use_case.delete(city_id)

            # Then
            assert result is False
            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.delete.assert_called_once_with(city_id)

    class TestFailures:
        """Tests des cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_city_does_not_exist(
            self, city_use_case, mock_city_repository
        ):
            """Test de suppression d'une ville inexistante"""
            # Given
            city_id = 999
            mock_city_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await city_use_case.delete(city_id)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self, city_use_case, mock_city_repository
        ):
            """Test de gestion d'erreur lors de la vérification d'existence"""
            # Given
            city_id = 1
            mock_city_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.delete(city_id)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_delete_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la suppression en base"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            mock_city_repository.get.return_value = existing_city
            mock_city_repository.delete.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.delete(city_id)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.delete.assert_called_once_with(city_id)
