from unittest.mock import AsyncMock

import pytest

from core.entities.city import CityEntity
from core.use_cases.city_use_case import CityUseCase
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class TestCityUpdateUseCase:
    """Tests unitaires pour la méthode update de CityUseCase"""

    @pytest.fixture
    def mock_city_repository(self):
        """Mock du repository de ville"""
        mock_repo = AsyncMock()
        mock_repo.get = AsyncMock()
        mock_repo.get_by_name = AsyncMock()
        mock_repo.update = AsyncMock()
        return mock_repo

    @pytest.fixture
    def city_use_case(self, mock_city_repository):
        """Fixture pour créer une instance de CityUseCase avec des mocks"""
        return CityUseCase(
            city_repository=mock_city_repository,
        )

    @pytest.fixture
    def existing_city(self):
        """Fixture pour une ville existante"""
        return CityEntity(
            id=1,
            name="Paris",
            region_id=1,
            created_at=None,
            updated_at=None,
        )

    @pytest.fixture
    def updated_city_data(self):
        """Fixture pour des données de ville mises à jour"""
        return CityEntity(
            id=1,
            name="Lyon",
            region_id=2,
            created_at=None,
            updated_at=None,
        )

    @pytest.fixture
    def updated_city_result(self):
        """Fixture pour le résultat de la mise à jour"""
        return CityEntity(
            id=1,
            name="Lyon",
            region_id=2,
            created_at=None,
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        city_use_case,
        mock_city_repository,
        existing_city,
        updated_city_data,
        updated_city_result,
    ):
        """Test de mise à jour de ville réussie"""
        # Arrange
        city_id = 1
        mock_city_repository.get.return_value = existing_city
        mock_city_repository.get_by_name.return_value = None
        mock_city_repository.update.return_value = updated_city_result

        # Act
        result = await city_use_case.update(city_id, updated_city_data)

        # Assert
        assert result == updated_city_result
        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.get_by_name.assert_called_once_with(updated_city_data.name)
        mock_city_repository.update.assert_called_once_with(city_id, updated_city_data)

    @pytest.mark.asyncio
    async def test_update_same_name_success(
        self, city_use_case, mock_city_repository, existing_city, updated_city_result
    ):
        """Test de mise à jour de ville avec le même nom (réussie)"""
        # Arrange
        city_id = 1
        # Données avec le même nom que la ville existante
        same_name_data = CityEntity(
            id=1,
            name="Paris",  # Même nom
            region_id=2,  # Région différente
            created_at=None,
            updated_at=None,
        )

        mock_city_repository.get.return_value = existing_city
        mock_city_repository.update.return_value = updated_city_result

        # Act
        result = await city_use_case.update(city_id, same_name_data)

        # Assert
        assert result == updated_city_result
        mock_city_repository.get.assert_called_once_with(city_id)
        # get_by_name ne doit pas être appelé si le nom n'a pas changé
        mock_city_repository.get_by_name.assert_not_called()
        mock_city_repository.update.assert_called_once_with(city_id, same_name_data)

    @pytest.mark.asyncio
    async def test_update_city_not_found(
        self, city_use_case, mock_city_repository, updated_city_data
    ):
        """Test de mise à jour d'une ville inexistante"""
        # Arrange
        city_id = 999
        mock_city_repository.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            await city_use_case.update(city_id, updated_city_data)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.get_by_name.assert_not_called()
        mock_city_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_name_already_exists(
        self, city_use_case, mock_city_repository, existing_city, updated_city_data
    ):
        """Test de mise à jour avec un nom déjà existant"""
        # Arrange
        city_id = 1
        # Une autre ville avec le nouveau nom
        other_city = CityEntity(
            id=2,
            name="Lyon",
            region_id=3,
            created_at=None,
            updated_at=None,
        )

        mock_city_repository.get.return_value = existing_city
        mock_city_repository.get_by_name.return_value = other_city

        # Act & Assert
        with pytest.raises(ConflictException):
            await city_use_case.update(city_id, updated_city_data)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.get_by_name.assert_called_once_with(updated_city_data.name)
        mock_city_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_name_exists_same_city(
        self,
        city_use_case,
        mock_city_repository,
        existing_city,
        updated_city_data,
        updated_city_result,
    ):
        """Test de mise à jour où le nom existe mais c'est la même ville (mise à jour autorisée)"""
        # Arrange
        city_id = 1
        # La même ville trouvée par nom (cas où on met à jour avec le même nom)
        same_city_by_name = CityEntity(
            id=1,  # Même ID
            name="Lyon",
            region_id=3,
            created_at=None,
            updated_at=None,
        )

        mock_city_repository.get.return_value = existing_city
        mock_city_repository.get_by_name.return_value = same_city_by_name
        mock_city_repository.update.return_value = updated_city_result

        # Act
        result = await city_use_case.update(city_id, updated_city_data)

        # Assert
        assert result == updated_city_result
        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.get_by_name.assert_called_once_with(updated_city_data.name)
        mock_city_repository.update.assert_called_once_with(city_id, updated_city_data)

    @pytest.mark.asyncio
    async def test_update_repository_get_error(
        self, city_use_case, mock_city_repository, updated_city_data
    ):
        """Test de gestion d'erreur lors de la récupération de la ville existante"""
        # Arrange
        city_id = 1
        mock_city_repository.get.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.update(city_id, updated_city_data)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.get_by_name.assert_not_called()
        mock_city_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_repository_get_by_name_error(
        self, city_use_case, mock_city_repository, existing_city, updated_city_data
    ):
        """Test de gestion d'erreur lors de la vérification d'existence du nom"""
        # Arrange
        city_id = 1
        mock_city_repository.get.return_value = existing_city
        mock_city_repository.get_by_name.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.update(city_id, updated_city_data)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.get_by_name.assert_called_once_with(updated_city_data.name)
        mock_city_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_repository_update_error(
        self, city_use_case, mock_city_repository, existing_city, updated_city_data
    ):
        """Test de gestion d'erreur lors de la mise à jour en base"""
        # Arrange
        city_id = 1
        mock_city_repository.get.return_value = existing_city
        mock_city_repository.get_by_name.return_value = None
        mock_city_repository.update.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.update(city_id, updated_city_data)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.get_by_name.assert_called_once_with(updated_city_data.name)
        mock_city_repository.update.assert_called_once_with(city_id, updated_city_data)
