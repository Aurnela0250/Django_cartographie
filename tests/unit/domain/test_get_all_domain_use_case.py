import pytest

from core.entities.pagination import PaginatedResult, PaginationParams
from presentation.exceptions import InternalServerErrorException
from tests.factories import DomainFactory


class TestDomainGetAllUseCase:
    """Unit tests for the get_all method of DomainUseCase."""

    class TestSuccess:
        """Tests for success cases."""

        @pytest.mark.asyncio
        async def test_should_get_all_domains_successfully(
            self,
            domain_use_case,
            mock_domain_repository,
            pagination_params,
            domain_factory,
        ):
            """Test for successful retrieval of all domains."""
            # Given
            sample_domains = [
                DomainFactory.build(),
                DomainFactory.build(),
                DomainFactory.build(),
            ]
            expected_result = PaginatedResult(
                items=sample_domains,
                total_items=3,
                page=1,
                per_page=10,
                total_pages=1,
            )
            mock_domain_repository.get_all.return_value = expected_result

            # When
            result = await domain_use_case.get_all(pagination_params)

            # Then
            assert result == expected_result
            assert len(result.items) == 3
            assert result.total_items == 3
            assert result.page == 1
            assert result.per_page == 10
            assert result.total_pages == 1
            mock_domain_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )

        @pytest.mark.asyncio
        async def test_should_return_empty_result_when_no_domains_exist(
            self,
            domain_use_case,
            mock_domain_repository,
            pagination_params,
        ):
            """Test for retrieval of all domains with an empty result."""
            # Given
            empty_result = PaginatedResult(
                items=[],
                total_items=0,
                page=1,
                per_page=10,
                total_pages=0,
            )
            mock_domain_repository.get_all.return_value = empty_result

            # When
            result = await domain_use_case.get_all(pagination_params)

            # Then
            assert result == empty_result
            assert len(result.items) == 0
            assert result.total_items == 0
            assert result.page == 1
            assert result.per_page == 10
            assert result.total_pages == 0
            mock_domain_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )

        @pytest.mark.asyncio
        async def test_should_handle_different_pagination_parameters(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for retrieval with different pagination parameters."""
            # Given
            custom_pagination = PaginationParams(page=2, per_page=5)
            sample_domains = [
                DomainFactory.build(),
                DomainFactory.build(),
            ]
            expected_result = PaginatedResult(
                items=sample_domains,
                total_items=3,
                page=2,
                per_page=5,
                total_pages=1,
            )
            mock_domain_repository.get_all.return_value = expected_result

            # When
            result = await domain_use_case.get_all(custom_pagination)

            # Then
            assert result == expected_result
            assert len(result.items) == 2
            assert result.total_items == 3
            assert result.page == 2
            assert result.per_page == 5
            mock_domain_repository.get_all.assert_called_once_with(
                pagination_params=custom_pagination
            )

    class TestFailures:
        """Tests for failure cases."""

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_all_failure(
            self,
            domain_use_case,
            mock_domain_repository,
            pagination_params,
        ):
            """Test for error handling during retrieval of all domains."""
            # Given
            mock_domain_repository.get_all.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.get_all(pagination_params)

            mock_domain_repository.get_all.assert_called_once_with(
                pagination_params=pagination_params
            )

    @pytest.mark.asyncio
    async def test_get_all_success(
        self,
        domain_use_case,
        mock_domain_repository,
        pagination_params,
        paginated_result,
    ):
        """Test de récupération de tous les domaines réussie"""
        # Arrange
        mock_domain_repository.get_all.return_value = paginated_result

        # Act
        result = await domain_use_case.get_all(pagination_params)

        # Assert
        assert result == paginated_result
        assert len(result.items) == 3
        assert result.total_items == 3
        assert result.page == 1
        assert result.per_page == 10
        assert result.total_pages == 1
        mock_domain_repository.get_all.assert_called_once_with(
            pagination_params=pagination_params
        )

    @pytest.mark.asyncio
    async def test_get_all_empty_result(
        self,
        domain_use_case,
        mock_domain_repository,
        pagination_params,
    ):
        """Test de récupération de tous les domaines avec résultat vide"""
        # Arrange
        empty_result = PaginatedResult(
            items=[],
            total_items=0,
            page=1,
            per_page=10,
            total_pages=0,
        )
        mock_domain_repository.get_all.return_value = empty_result

        # Act
        result = await domain_use_case.get_all(pagination_params)

        # Assert
        assert result == empty_result
        assert len(result.items) == 0
        assert result.total_items == 0
        assert result.page == 1
        assert result.per_page == 10
        assert result.total_pages == 0
        mock_domain_repository.get_all.assert_called_once_with(
            pagination_params=pagination_params
        )

    @pytest.mark.asyncio
    async def test_get_all_with_different_pagination(
        self, domain_use_case, mock_domain_repository, sample_domains
    ):
        """Test de récupération avec différents paramètres de pagination"""
        # Arrange
        custom_pagination = PaginationParams(page=2, per_page=5)
        paginated_result = PaginatedResult(
            items=sample_domains[:2],  # Première partie des résultats
            total_items=3,
            page=2,
            per_page=5,
            total_pages=1,
        )
        mock_domain_repository.get_all.return_value = paginated_result

        # Act
        result = await domain_use_case.get_all(custom_pagination)

        # Assert
        assert result == paginated_result
        assert len(result.items) == 2
        assert result.total_items == 3
        assert result.page == 2
        assert result.per_page == 5
        mock_domain_repository.get_all.assert_called_once_with(
            pagination_params=custom_pagination
        )

    @pytest.mark.asyncio
    async def test_get_all_repository_error(
        self, domain_use_case, mock_domain_repository, pagination_params
    ):
        """Test de gestion d'erreur lors de la récupération en base"""
        # Arrange
        mock_domain_repository.get_all.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.get_all(pagination_params)

        mock_domain_repository.get_all.assert_called_once_with(
            pagination_params=pagination_params
        )
