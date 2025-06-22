import pytest

from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class TestCityUpdateUseCase:
    """Tests unitaires pour la méthode update de CityUseCase"""

    class TestSuccess:
        """Tests des cas de succès"""

        @pytest.mark.asyncio
        async def test_should_update_city_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de mise à jour de ville réussie"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            updated_data = city_factory(id=city_id, name="Lyon", region_id=2)
            updated_result = city_factory(id=city_id, name="Lyon", region_id=2)

            mock_city_repository.get.return_value = existing_city
            mock_city_repository.get_by_name.return_value = None
            mock_city_repository.update.return_value = updated_result

            # When
            result = await city_use_case.update(city_id, updated_data)

            # Then
            assert result == updated_result
            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.get_by_name.assert_called_once_with(updated_data.name)
            mock_city_repository.update.assert_called_once_with(city_id, updated_data)

        @pytest.mark.asyncio
        async def test_should_update_city_with_same_name_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de mise à jour de ville avec le même nom (réussie)"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            same_name_data = city_factory(id=city_id, name="Paris", region_id=2)
            updated_result = city_factory(id=city_id, name="Paris", region_id=2)

            mock_city_repository.get.return_value = existing_city
            mock_city_repository.update.return_value = updated_result

            # When
            result = await city_use_case.update(city_id, same_name_data)

            # Then
            assert result == updated_result
            mock_city_repository.get.assert_called_once_with(city_id)
            # get_by_name ne doit pas être appelé si le nom n'a pas changé
            mock_city_repository.get_by_name.assert_not_called()
            mock_city_repository.update.assert_called_once_with(city_id, same_name_data)

        @pytest.mark.asyncio
        async def test_should_update_when_name_exists_for_same_city(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de mise à jour où le nom existe mais c'est la même ville"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            updated_data = city_factory(id=city_id, name="Lyon", region_id=2)
            same_city_by_name = city_factory(id=city_id, name="Lyon", region_id=3)
            updated_result = city_factory(id=city_id, name="Lyon", region_id=2)

            mock_city_repository.get.return_value = existing_city
            mock_city_repository.get_by_name.return_value = same_city_by_name
            mock_city_repository.update.return_value = updated_result

            # When
            result = await city_use_case.update(city_id, updated_data)

            # Then
            assert result == updated_result
            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.get_by_name.assert_called_once_with(updated_data.name)
            mock_city_repository.update.assert_called_once_with(city_id, updated_data)

    class TestFailures:
        """Tests des cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_city_does_not_exist(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de mise à jour d'une ville inexistante"""
            # Given
            city_id = 999
            updated_data = city_factory(name="Lyon", region_id=2)
            mock_city_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await city_use_case.update(city_id, updated_data)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.get_by_name.assert_not_called()
            mock_city_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_name_already_exists(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de mise à jour avec un nom déjà existant"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            updated_data = city_factory(id=city_id, name="Lyon", region_id=2)
            other_city = city_factory(id=2, name="Lyon", region_id=3)

            mock_city_repository.get.return_value = existing_city
            mock_city_repository.get_by_name.return_value = other_city

            # When & Then
            with pytest.raises(ConflictException):
                await city_use_case.update(city_id, updated_data)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.get_by_name.assert_called_once_with(updated_data.name)
            mock_city_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la récupération de la ville existante"""
            # Given
            city_id = 1
            updated_data = city_factory(name="Lyon", region_id=2)
            mock_city_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.update(city_id, updated_data)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.get_by_name.assert_not_called()
            mock_city_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la vérification d'existence du nom"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            updated_data = city_factory(id=city_id, name="Lyon", region_id=2)

            mock_city_repository.get.return_value = existing_city
            mock_city_repository.get_by_name.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.update(city_id, updated_data)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.get_by_name.assert_called_once_with(updated_data.name)
            mock_city_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_update_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la mise à jour en base"""
            # Given
            city_id = 1
            existing_city = city_factory(id=city_id, name="Paris", region_id=1)
            updated_data = city_factory(id=city_id, name="Lyon", region_id=2)

            mock_city_repository.get.return_value = existing_city
            mock_city_repository.get_by_name.return_value = None
            mock_city_repository.update.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.update(city_id, updated_data)

            mock_city_repository.get.assert_called_once_with(city_id)
            mock_city_repository.get_by_name.assert_called_once_with(updated_data.name)
            mock_city_repository.update.assert_called_once_with(city_id, updated_data)
