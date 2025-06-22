import pytest

from core.entities.establishment_type import EstablishmentTypeEntity
from core.entities.pagination import PaginatedResult
from presentation.exceptions import InternalServerErrorException


class TestEstablishmentTypeFilterUseCase:
    """Tests unitaires pour la méthode filter de EstablishmentTypeUseCase"""

    class TestSuccess:
        """Tests pour les cas de succès"""

        @pytest.mark.asyncio
        async def test_should_filter_establishment_types_successfully(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
            pagination_params,
            establishment_type_filters,
        ):
            """Test pour le filtrage réussi des types d'établissement"""
            # Given
            establishment_type = establishment_type_factory(id=1, name="Lycée")
            expected_result = PaginatedResult[EstablishmentTypeEntity](
                items=[establishment_type],
                total_items=1,
                page=1,
                per_page=10,
                total_pages=1,
            )
            mock_establishment_type_repository.filter.return_value = expected_result

            # When
            result = await establishment_type_use_case.filter(
                pagination_params=pagination_params, filters=establishment_type_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 1
            assert result.items[0].name == "Lycée"
            mock_establishment_type_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=establishment_type_filters
            )

        @pytest.mark.asyncio
        async def test_should_return_empty_result_when_no_matches(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            pagination_params,
            establishment_type_filters,
        ):
            """Test pour le filtrage avec résultat vide"""
            # Given
            expected_result = PaginatedResult[EstablishmentTypeEntity](
                items=[], total_items=0, page=1, per_page=10, total_pages=0
            )
            mock_establishment_type_repository.filter.return_value = expected_result

            # When
            result = await establishment_type_use_case.filter(
                pagination_params=pagination_params, filters=establishment_type_filters
            )

            # Then
            assert result == expected_result
            assert len(result.items) == 0
            assert result.total_items == 0
            mock_establishment_type_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=establishment_type_filters
            )

    class TestFailures:
        """Tests pour les cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_repository_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            pagination_params,
            establishment_type_filters,
        ):
            """Test pour la gestion d'erreur lors du filtrage"""
            # Given
            mock_establishment_type_repository.filter.side_effect = Exception(
                "Database connection error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.filter(
                    pagination_params=pagination_params,
                    filters=establishment_type_filters,
                )

            mock_establishment_type_repository.filter.assert_called_once_with(
                pagination_params=pagination_params, filters=establishment_type_filters
            )
