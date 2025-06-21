from unittest.mock import AsyncMock

import pytest

from core.entities.city import CityEntity
from core.use_cases.city_use_case import CityUseCase
from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestCityGetUseCase:
    """Tests unitaires pour la méthode get de CityUseCase"""

    @pytest.fixture
    def mock_city_repository(self):
        """Mock du repository de ville"""
        mock_repo = AsyncMock()
        mock_repo.get = AsyncMock()
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
    async def test_get_success(self, city_use_case, mock_city_repository, sample_city):
        """Test de récupération de ville réussie"""
        # Arrange
        city_id = 1
        mock_city_repository.get.return_value = sample_city

        # Act
        result = await city_use_case.get(city_id)

        # Assert
        assert result == sample_city
        mock_city_repository.get.assert_called_once_with(city_id)

    @pytest.mark.asyncio
    async def test_get_city_not_found(self, city_use_case, mock_city_repository):
        """Test de récupération d'une ville inexistante"""
        # Arrange
        city_id = 999
        mock_city_repository.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            await city_use_case.get(city_id)

        mock_city_repository.get.assert_called_once_with(city_id)

    @pytest.mark.asyncio
    async def test_get_repository_error(self, city_use_case, mock_city_repository):
        """Test de gestion d'erreur lors de la récupération en base"""
        # Arrange
        city_id = 1
        mock_city_repository.get.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.get(city_id)

        mock_city_repository.get.assert_called_once_with(city_id)
