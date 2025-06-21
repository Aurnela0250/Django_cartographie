"""Tests unitaires pour la méthode filter de CityUseCase"""

from unittest.mock import AsyncMock, Mock

import pytest

from core.entities.city import CityEntity
from core.entities.filters import CityFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.city_repository import ICityRepository
from core.use_cases.city_use_case import CityUseCase
from presentation.exceptions import InternalServerErrorException


class TestCityFilterUseCase:
    """Classe de tests pour la méthode filter de CityUseCase"""

    @pytest.fixture
    def mock_city_repository(self) -> AsyncMock:
        """Mock du repository City"""
        return AsyncMock(spec=ICityRepository)

    @pytest.fixture
    def mock_logger(self) -> Mock:
        """Mock du logger"""
        return Mock()

    @pytest.fixture
    def city_use_case(
        self, mock_city_repository: AsyncMock, mock_logger: Mock
    ) -> CityUseCase:
        """Instance de CityUseCase avec les mocks injectés"""
        city_use_case = CityUseCase(city_repository=mock_city_repository)
        city_use_case.logger = mock_logger
        return city_use_case

    @pytest.fixture
    def sample_city(self) -> CityEntity:
        """Ville d'exemple pour les tests"""
        return CityEntity(id=1, name="Paris", region_id=1)

    @pytest.fixture
    def pagination_params(self) -> PaginationParams:
        """Paramètres de pagination d'exemple"""
        return PaginationParams(page=1, per_page=10)

    @pytest.fixture
    def city_filters(self) -> CityFilters:
        """Filtres d'exemple pour les villes"""
        return CityFilters(name="Paris")

    async def test_filter_success(
        self,
        city_use_case: CityUseCase,
        mock_city_repository: AsyncMock,
        sample_city: CityEntity,
        pagination_params: PaginationParams,
        city_filters: CityFilters,
    ):
        """Test du filtrage avec succès"""
        # Arrange
        expected_result = PaginatedResult[CityEntity](
            items=[sample_city], total_items=1, page=1, per_page=10, total_pages=1
        )
        mock_city_repository.filter.return_value = expected_result

        # Act
        result = await city_use_case.filter(
            pagination_params=pagination_params, filters=city_filters
        )

        # Assert
        assert result == expected_result
        assert len(result.items) == 1
        assert result.items[0].name == "Paris"
        mock_city_repository.filter.assert_called_once_with(
            pagination_params=pagination_params, filters=city_filters
        )

    async def test_filter_empty_result(
        self,
        city_use_case: CityUseCase,
        mock_city_repository: AsyncMock,
        pagination_params: PaginationParams,
        city_filters: CityFilters,
    ):
        """Test du filtrage avec résultat vide"""
        # Arrange
        expected_result = PaginatedResult[CityEntity](
            items=[], total_items=0, page=1, per_page=10, total_pages=0
        )
        mock_city_repository.filter.return_value = expected_result

        # Act
        result = await city_use_case.filter(
            pagination_params=pagination_params, filters=city_filters
        )

        # Assert
        assert result == expected_result
        assert len(result.items) == 0
        assert result.total_items == 0
        mock_city_repository.filter.assert_called_once_with(
            pagination_params=pagination_params, filters=city_filters
        )

    async def test_filter_with_multiple_cities(
        self,
        city_use_case: CityUseCase,
        mock_city_repository: AsyncMock,
        pagination_params: PaginationParams,
        city_filters: CityFilters,
    ):
        """Test du filtrage retournant plusieurs villes"""
        # Arrange
        cities = [
            CityEntity(id=1, name="Paris", region_id=1),
            CityEntity(id=2, name="Paray-le-Monial", region_id=2),
        ]
        expected_result = PaginatedResult[CityEntity](
            items=cities, total_items=2, page=1, per_page=10, total_pages=1
        )
        mock_city_repository.filter.return_value = expected_result

        # Act
        result = await city_use_case.filter(
            pagination_params=pagination_params, filters=city_filters
        )

        # Assert
        assert result == expected_result
        assert len(result.items) == 2
        assert result.total_items == 2
        mock_city_repository.filter.assert_called_once_with(
            pagination_params=pagination_params, filters=city_filters
        )

    async def test_filter_repository_error(
        self,
        city_use_case: CityUseCase,
        mock_city_repository: AsyncMock,
        mock_logger: Mock,
        pagination_params: PaginationParams,
        city_filters: CityFilters,
    ):
        """Test de gestion d'erreur lors du filtrage"""
        # Arrange
        repository_error = Exception("Database connection error")
        mock_city_repository.filter.side_effect = repository_error

        # Act & Assert
        with pytest.raises(InternalServerErrorException) as exc_info:
            await city_use_case.filter(
                pagination_params=pagination_params, filters=city_filters
            )

        # Vérification que l'exception est bien levée
        assert str(exc_info.value) == "Server error. Please try again later."
        mock_logger.error.assert_called_once_with(
            "Unexpected error during cities filtering: Database connection error"
        )
        mock_city_repository.filter.assert_called_once_with(
            pagination_params=pagination_params, filters=city_filters
        )
