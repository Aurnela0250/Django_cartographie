import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestDomainGetUseCase:
    """Unit tests for the get method of DomainUseCase."""

    class TestSuccess:
        """Tests for success cases."""

        @pytest.mark.asyncio
        async def test_should_get_domain_successfully(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for successful domain retrieval."""
            # Given
            domain_id = 1
            sample_domain = domain_factory(id=domain_id, name="Science")
            mock_domain_repository.get.return_value = sample_domain

            # When
            result = await domain_use_case.get(domain_id)

            # Then
            assert result == sample_domain
            mock_domain_repository.get.assert_called_once_with(domain_id)

    class TestFailures:
        """Tests for failure cases."""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_domain_does_not_exist(
            self, domain_use_case, mock_domain_repository
        ):
            """Test for retrieval of a non-existent domain."""
            # Given
            domain_id = 999
            mock_domain_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await domain_use_case.get(domain_id)

            mock_domain_repository.get.assert_called_once_with(domain_id)

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self, domain_use_case, mock_domain_repository
        ):
            """Test for error handling during domain retrieval."""
            # Given
            domain_id = 1
            mock_domain_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.get(domain_id)

            mock_domain_repository.get.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_get_success(
        self, domain_use_case, mock_domain_repository, sample_domain
    ):
        """Test de récupération de domaine réussie"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.return_value = sample_domain

        # Act
        result = await domain_use_case.get(domain_id)

        # Assert
        assert result == sample_domain
        mock_domain_repository.get.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_get_domain_not_found(self, domain_use_case, mock_domain_repository):
        """Test de récupération d'un domaine inexistant"""
        # Arrange
        domain_id = 999
        mock_domain_repository.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            await domain_use_case.get(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_get_repository_error(self, domain_use_case, mock_domain_repository):
        """Test de gestion d'erreur lors de la récupération en base"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.get(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)
