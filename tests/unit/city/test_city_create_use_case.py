from unittest.mock import AsyncMock

import pytest

from core.entities.city import CityEntity
from core.use_cases.city_use_case import CityUseCase
from presentation.exceptions import ConflictException, InternalServerErrorException


class TestCityCreateUseCase:
    """Tests unitaires pour la méthode create de CityUseCase"""

    @pytest.fixture
    def mock_city_repository(self):
        """Mock du repository de ville"""
        mock_repo = AsyncMock()
        mock_repo.get_by_name = AsyncMock()
        mock_repo.create = AsyncMock()
        return mock_repo

    @pytest.fixture
    def city_use_case(self, mock_city_repository):
        """Fixture pour créer une instance de CityUseCase avec des mocks"""
        return CityUseCase(
            city_repository=mock_city_repository,
        )

    @pytest.fixture
    def sample_city_data(self):
        """Fixture pour des données de ville de test"""
        return CityEntity(
            id=None,
            name="Paris",
            region_id=1,
            created_at=None,
            updated_at=None,
        )

    @pytest.fixture
    def sample_created_city(self):
        """Fixture pour une ville créée"""
        return CityEntity(
            id=1,
            name="Paris",
            region_id=1,
            created_at=None,
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_create_success(
        self, city_use_case, mock_city_repository, sample_city_data, sample_created_city
    ):
        """Test de création de ville réussie"""
        # Arrange
        mock_city_repository.get_by_name.return_value = None
        mock_city_repository.create.return_value = sample_created_city

        # Act
        result = await city_use_case.create(sample_city_data)

        # Assert
        assert result == sample_created_city
        mock_city_repository.get_by_name.assert_called_once_with(sample_city_data.name)
        mock_city_repository.create.assert_called_once_with(sample_city_data)

    @pytest.mark.asyncio
    async def test_create_city_already_exists(
        self, city_use_case, mock_city_repository, sample_city_data, sample_created_city
    ):
        """Test de création de ville avec nom déjà existant"""
        # Arrange
        mock_city_repository.get_by_name.return_value = sample_created_city

        # Act & Assert
        with pytest.raises(ConflictException):
            await city_use_case.create(sample_city_data)

        mock_city_repository.get_by_name.assert_called_once_with(sample_city_data.name)
        mock_city_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_repository_get_by_name_error(
        self, city_use_case, mock_city_repository, sample_city_data
    ):
        """Test de gestion d'erreur lors de la vérification d'existence"""
        # Arrange
        mock_city_repository.get_by_name.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.create(sample_city_data)

        mock_city_repository.get_by_name.assert_called_once_with(sample_city_data.name)
        mock_city_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_repository_create_error(
        self, city_use_case, mock_city_repository, sample_city_data
    ):
        """Test de gestion d'erreur lors de la création en base"""
        # Arrange
        mock_city_repository.get_by_name.return_value = None
        mock_city_repository.create.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.create(sample_city_data)

        mock_city_repository.get_by_name.assert_called_once_with(sample_city_data.name)
        mock_city_repository.create.assert_called_once_with(sample_city_data)
