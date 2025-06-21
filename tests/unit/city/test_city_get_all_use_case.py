from unittest.mock import AsyncMock

import pytest

from core.entities.city import CityEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.use_cases.city_use_case import CityUseCase
from presentation.exceptions import InternalServerErrorException


class TestCityGetAllUseCase:
    """Tests unitaires pour la méthode get_all de CityUseCase"""

    @pytest.fixture
    def mock_city_repository(self):
        """Mock du repository de ville"""
        mock_repo = AsyncMock()
        mock_repo.get_all = AsyncMock()
        return mock_repo

    @pytest.fixture
    def city_use_case(self, mock_city_repository):
        """Fixture pour créer une instance de CityUseCase avec des mocks"""
        return CityUseCase(
            city_repository=mock_city_repository,
        )

    @pytest.fixture
    def pagination_params(self):
        """Fixture pour les paramètres de pagination"""
        return PaginationParams(page=1, per_page=10)

    @pytest.fixture
    def sample_cities(self):
        """Fixture pour une liste de villes de test"""
        return [
            CityEntity(
                id=1,
                name="Paris",
                region_id=1,
                created_at=None,
                updated_at=None,
            ),
            CityEntity(
                id=2,
                name="Lyon",
                region_id=2,
                created_at=None,
                updated_at=None,
            ),
            CityEntity(
                id=3,
                name="Marseille",
                region_id=3,
                created_at=None,
                updated_at=None,
            ),
        ]

    @pytest.fixture
    def paginated_result(self, sample_cities):
        """Fixture pour un résultat paginé"""
        return PaginatedResult(
            items=sample_cities, total_items=3, page=1, per_page=10, total_pages=1
        )

    @pytest.mark.asyncio
    async def test_get_all_success(
        self, city_use_case, mock_city_repository, pagination_params, paginated_result
    ):
        """Test de récupération de toutes les villes réussie"""
        # Arrange
        mock_city_repository.get_all.return_value = paginated_result

        # Act
        result = await city_use_case.get_all(pagination_params)

        # Assert
        assert result == paginated_result
        assert len(result.items) == 3
        assert result.total_items == 3
        assert result.page == 1
        assert result.per_page == 10
        assert result.total_pages == 1
        mock_city_repository.get_all.assert_called_once_with(
            pagination_params=pagination_params
        )

    @pytest.mark.asyncio
    async def test_get_all_empty_result(
        self, city_use_case, mock_city_repository, pagination_params
    ):
        """Test de récupération de toutes les villes avec résultat vide"""
        # Arrange
        empty_result = PaginatedResult(
            items=[], total_items=0, page=1, per_page=10, total_pages=0
        )
        mock_city_repository.get_all.return_value = empty_result

        # Act
        result = await city_use_case.get_all(pagination_params)

        # Assert
        assert result == empty_result
        assert len(result.items) == 0
        assert result.total_items == 0
        assert result.page == 1
        assert result.per_page == 10
        assert result.total_pages == 0
        mock_city_repository.get_all.assert_called_once_with(
            pagination_params=pagination_params
        )

    @pytest.mark.asyncio
    async def test_get_all_with_different_pagination(
        self, city_use_case, mock_city_repository, sample_cities
    ):
        """Test de récupération avec différents paramètres de pagination"""
        # Arrange
        custom_pagination = PaginationParams(page=2, per_page=5)
        paginated_result = PaginatedResult(
            items=sample_cities[:2],  # Première partie des résultats
            total_items=3,
            page=2,
            per_page=5,
            total_pages=1,
        )
        mock_city_repository.get_all.return_value = paginated_result

        # Act
        result = await city_use_case.get_all(custom_pagination)

        # Assert
        assert result == paginated_result
        assert len(result.items) == 2
        assert result.total_items == 3
        assert result.page == 2
        assert result.per_page == 5
        mock_city_repository.get_all.assert_called_once_with(
            pagination_params=custom_pagination
        )

    @pytest.mark.asyncio
    async def test_get_all_repository_error(
        self, city_use_case, mock_city_repository, pagination_params
    ):
        """Test de gestion d'erreur lors de la récupération en base"""
        # Arrange
        mock_city_repository.get_all.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await city_use_case.get_all(pagination_params)

        mock_city_repository.get_all.assert_called_once_with(
            pagination_params=pagination_params
        )
