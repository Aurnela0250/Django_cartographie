from unittest.mock import AsyncMock

import pytest

from core.entities.city import CityEntity
from core.use_cases.city_use_case import CityUseCase
from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestCityDeleteUseCase:
    """Tests unitaires pour la méthode delete de CityUseCase"""

    @pytest.fixture
    def mock_city_repository(self):
        """Mock du repository de ville"""
        mock_repo = AsyncMock()
        mock_repo.get = AsyncMock()
        mock_repo.delete = AsyncMock()
        return mock_repo

    @pytest.fixture
    def city_use_case(self, mock_city_repository):
        """Fixture pour créer une instance de CityUseCase avec des mocks"""
        return CityUseCase(
            city_repository=mock_city_repository,
        )

    @pytest.fixture
    def sample_city(self):
        """Fixture pour une ville de test"""
        return CityEntity(
            id=1,
            name="Paris",
            region_id=1,
            created_at=None,
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_delete_success(
        self, city_use_case, mock_city_repository, sample_city
    ):
        """Test de suppression de ville réussie"""
        # Arrange
        city_id = 1
        mock_city_repository.get.return_value = sample_city
        mock_city_repository.delete.return_value = True

        # Act
        result = await city_use_case.delete(city_id)

        # Assert
        assert result is True
        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.delete.assert_called_once_with(city_id)

    @pytest.mark.asyncio
    async def test_delete_city_not_found(self, city_use_case, mock_city_repository):
        """Test de suppression d'une ville inexistante"""
        # Arrange
        city_id = 999
        mock_city_repository.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            await city_use_case.delete(city_id)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_repository_get_error(
        self, city_use_case, mock_city_repository
    ):
        """Test de gestion d'erreur lors de la vérification d'existence"""
        # Arrange
        city_id = 1
        mock_city_repository.get.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.delete(city_id)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_repository_delete_error(
        self, city_use_case, mock_city_repository, sample_city
    ):
        """Test de gestion d'erreur lors de la suppression en base"""
        # Arrange
        city_id = 1
        mock_city_repository.get.return_value = sample_city
        mock_city_repository.delete.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.delete(city_id)

        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.delete.assert_called_once_with(city_id)

    @pytest.mark.asyncio
    async def test_delete_returns_false(
        self, city_use_case, mock_city_repository, sample_city
    ):
        """Test de suppression qui retourne False (échec de suppression)"""
        # Arrange
        city_id = 1
        mock_city_repository.get.return_value = sample_city
        mock_city_repository.delete.return_value = False

        # Act
        result = await city_use_case.delete(city_id)

        # Assert
        assert result is False
        mock_city_repository.get.assert_called_once_with(city_id)
        mock_city_repository.delete.assert_called_once_with(city_id)
