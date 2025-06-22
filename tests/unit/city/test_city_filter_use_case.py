import pytest

from core.entities.filters import CityFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from presentation.exceptions import InternalServerErrorException


class TestCityFilterUseCase:
    """Tests unitaires pour la méthode filter de CityUseCase"""

    class TestSuccess:
        """Tests des cas de succès"""

        @pytest.mark.asyncio
        async def test_should_filter_cities_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test du filtrage avec succès"""
            # Given
            pagination_params = PaginationParams(page=1, per_page=10)
            city_filters = CityFilters(name="Paris")
            sample_city = city_factory(id=1, name="Paris", region_id=1)
            expected_result = PaginatedResult(
                items=[sample_city], total_items=1, page=1, per_page=10, total_pages=1
            )
            mock_city_repository.filter.return_value = expected_result

            # When
            result = await city_use_case.filter(
                pagination_params=pagination_params, filters=city_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 1
            assert result.items[0].name == "Paris"
            mock_city_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=city_filters
            )

        @pytest.mark.asyncio
        async def test_should_return_empty_result_when_no_cities_match(
            self, city_use_case, mock_city_repository
        ):
            """Test du filtrage avec résultat vide"""
            # Given
            pagination_params = PaginationParams(page=1, per_page=10)
            city_filters = CityFilters(name="UnknownCity")
            expected_result = PaginatedResult(
                items=[], total_items=0, page=1, per_page=10, total_pages=0
            )
            mock_city_repository.filter.return_value = expected_result

            # When
            result = await city_use_case.filter(
                pagination_params=pagination_params, filters=city_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 0
            assert result.total_items == 0
            mock_city_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=city_filters
            )

        @pytest.mark.asyncio
        async def test_should_return_multiple_cities(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test du filtrage retournant plusieurs villes"""
            # Given
            pagination_params = PaginationParams(page=1, per_page=10)
            city_filters = CityFilters(name="Paris")
            cities = [
                city_factory(id=1, name="Paris", region_id=1),
                city_factory(id=2, name="Paray-le-Monial", region_id=2),
            ]
            expected_result = PaginatedResult(
                items=cities, total_items=2, page=1, per_page=10, total_pages=1
            )
            mock_city_repository.filter.return_value = expected_result

            # When
            result = await city_use_case.filter(
                pagination_params=pagination_params, filters=city_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 2
            assert result.total_items == 2
            mock_city_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=city_filters
            )

    class TestFailures:
        """Tests des cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_repository_failure(
            self, city_use_case, mock_city_repository
        ):
            """Test de gestion d'erreur lors du filtrage"""
            # Given
            pagination_params = PaginationParams(page=1, per_page=10)
            city_filters = CityFilters(name="Paris")
            mock_city_repository.filter.side_effect = Exception(
                "Database connection error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.filter(
                    pagination_params=pagination_params, filters=city_filters
                )

            mock_city_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=city_filters
            )
