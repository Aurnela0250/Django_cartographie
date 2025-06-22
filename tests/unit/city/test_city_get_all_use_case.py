import pytest

from core.entities.pagination import PaginatedResult, PaginationParams
from presentation.exceptions import InternalServerErrorException


class TestCityGetAllUseCase:
    """Tests unitaires pour la méthode get_all de CityUseCase"""

    class TestSuccess:
        """Tests des cas de succès"""

        @pytest.mark.asyncio
        async def test_should_get_all_cities_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de récupération de toutes les villes réussie"""
            # Given
            pagination_params = PaginationParams(page=1, per_page=10)
            sample_cities = [
                city_factory(id=1, name="Paris", region_id=1),
                city_factory(id=2, name="Lyon", region_id=2),
                city_factory(id=3, name="Marseille", region_id=3),
            ]
            paginated_result = PaginatedResult(
                items=sample_cities, total_items=3, page=1, per_page=10, total_pages=1
            )
            mock_city_repository.get_all.return_value = paginated_result

            # When
            result = await city_use_case.get_all(pagination_params)

            # Then
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
        async def test_should_return_empty_result_when_no_cities_exist(
            self, city_use_case, mock_city_repository
        ):
            """Test de récupération de toutes les villes avec résultat vide"""
            # Given
            pagination_params = PaginationParams(page=1, per_page=10)
            empty_result = PaginatedResult(
                items=[], total_items=0, page=1, per_page=10, total_pages=0
            )
            mock_city_repository.get_all.return_value = empty_result

            # When
            result = await city_use_case.get_all(pagination_params)

            # Then
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
        async def test_should_handle_different_pagination_parameters(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de récupération avec différents paramètres de pagination"""
            # Given
            custom_pagination = PaginationParams(page=2, per_page=5)
            sample_cities = [
                city_factory(id=1, name="Paris", region_id=1),
                city_factory(id=2, name="Lyon", region_id=2),
            ]
            paginated_result = PaginatedResult(
                items=sample_cities, total_items=2, page=2, per_page=5, total_pages=1
            )
            mock_city_repository.get_all.return_value = paginated_result

            # When
            result = await city_use_case.get_all(custom_pagination)

            # Then
            assert result == paginated_result
            assert len(result.items) == 2
            assert result.total_items == 2
            assert result.page == 2
            assert result.per_page == 5
            mock_city_repository.get_all.assert_called_once_with(
                pagination_params=custom_pagination
            )

    class TestFailures:
        """Tests des cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_repository_failure(
            self, city_use_case, mock_city_repository
        ):
            """Test de gestion d'erreur lors de la récupération en base"""
            # Given
            pagination_params = PaginationParams(page=1, per_page=10)
            mock_city_repository.get_all.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.get_all(pagination_params)

            mock_city_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )
