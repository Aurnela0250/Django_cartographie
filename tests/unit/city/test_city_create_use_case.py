import pytest

from presentation.exceptions import ConflictException, InternalServerErrorException


class TestCityCreateUseCase:
    """Tests unitaires pour la méthode create de CityUseCase"""

    class TestSuccess:
        """Tests des cas de succès"""

        @pytest.mark.asyncio
        async def test_should_create_city_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de création de ville réussie"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            created_city = city_factory(id=1, name="Paris", region_id=1)
            mock_city_repository.get_by_name.return_value = None
            mock_city_repository.create.return_value = created_city

            # When
            result = await city_use_case.create(new_city)

            # Then
            assert result == created_city
            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_called_once_with(new_city)

    class TestFailures:
        """Tests des cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_city_already_exists(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de création de ville avec nom déjà existant"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            existing_city = city_factory(id=1, name="Paris", region_id=1)
            mock_city_repository.get_by_name.return_value = existing_city

            # When & Then
            with pytest.raises(ConflictException):
                await city_use_case.create(new_city)

            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la vérification d'existence"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            mock_city_repository.get_by_name.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.create(new_city)

            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_create_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la création en base"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            mock_city_repository.get_by_name.return_value = None
            mock_city_repository.create.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.create(new_city)

            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_called_once_with(new_city)
