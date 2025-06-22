import pytest

from core.entities.pagination import PaginatedResult
from presentation.exceptions import InternalServerErrorException


class TestEstablishmentTypeGetAllUseCase:
    """Tests unitaires pour la méthode get_all de EstablishmentTypeUseCase"""

    class TestSuccess:
        """Tests pour les cas de succès"""

        @pytest.mark.asyncio
        async def test_should_get_all_establishment_types_successfully(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            establishment_type_factory,
            pagination_params,
        ):
            """Test pour la récupération réussie de tous les types d'établissement"""
            # Given
            establishment_types = [
                establishment_type_factory(id=1, name="Lycée"),
                establishment_type_factory(id=2, name="Collège"),
                establishment_type_factory(id=3, name="Université"),
            ]
            expected_result = PaginatedResult(
                items=establishment_types,
                total_items=3,
                page=1,
                per_page=10,
                total_pages=1,
            )
            mock_establishment_type_repository.get_all.return_value = expected_result

            # When
            result = await establishment_type_use_case.get_all(pagination_params)

            # Then
            assert result == expected_result
            assert len(result.items) == 3
            assert result.total_items == 3
            assert result.page == 1
            assert result.per_page == 10
            assert result.total_pages == 1
            mock_establishment_type_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )

        @pytest.mark.asyncio
        async def test_should_return_empty_result_when_no_establishment_types(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            pagination_params,
        ):
            """Test pour la récupération avec résultat vide"""
            # Given
            empty_result = PaginatedResult(
                items=[], total_items=0, page=1, per_page=10, total_pages=0
            )
            mock_establishment_type_repository.get_all.return_value = empty_result

            # When
            result = await establishment_type_use_case.get_all(pagination_params)

            # Then
            assert result == empty_result
            assert len(result.items) == 0
            assert result.total_items == 0
            assert result.page == 1
            assert result.per_page == 10
            assert result.total_pages == 0
            mock_establishment_type_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )

    class TestFailures:
        """Tests pour les cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_repository_failure(
            self,
            establishment_type_use_case,
            mock_establishment_type_repository,
            pagination_params,
        ):
            """Test pour la gestion d'erreur lors de la récupération en base"""
            # Given
            mock_establishment_type_repository.get_all.side_effect = Exception(
                "Database error"
            )

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await establishment_type_use_case.get_all(pagination_params)

            mock_establishment_type_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )
