import pytest

from presentation.exceptions import InternalServerErrorException, NotFoundException


class TestDomainDeleteUseCase:
    """Unit tests for the delete method of DomainUseCase."""

    class TestSuccess:
        """Tests for success cases."""

        @pytest.mark.asyncio
        async def test_should_delete_domain_successfully(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for successful domain deletion."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.delete.return_value = True

            # When
            result = await domain_use_case.delete(domain_id)

            # Then
            assert result is True
            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.delete.assert_called_once_with(domain_id)

    class TestFailures:
        """Tests for failure cases."""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_domain_does_not_exist(
            self, domain_use_case, mock_domain_repository
        ):
            """Test for deletion of a non-existent domain."""
            # Given
            domain_id = 999
            mock_domain_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await domain_use_case.delete(domain_id)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self, domain_use_case, mock_domain_repository
        ):
            """Test for error handling during the existence check."""
            # Given
            domain_id = 1
            mock_domain_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.delete(domain_id)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.delete.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_delete_failure(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for error handling during database deletion."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.delete.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.delete(domain_id)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.delete.assert_called_once_with(domain_id)

        @pytest.mark.asyncio
        async def test_should_return_false_when_delete_fails(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for deletion that returns False (failure)."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.delete.return_value = False

            # When
            result = await domain_use_case.delete(domain_id)

            # Then
            assert result is False
            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.delete.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_delete_success(
        self, domain_use_case, mock_domain_repository, sample_domain
    ):
        """Test de suppression de domaine réussie"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.return_value = sample_domain
        mock_domain_repository.delete.return_value = True

        # Act
        result = await domain_use_case.delete(domain_id)

        # Assert
        assert result is True
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.delete.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_delete_domain_not_found(
        self, domain_use_case, mock_domain_repository
    ):
        """Test de suppression d'un domaine inexistant"""
        # Arrange
        domain_id = 999
        mock_domain_repository.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            await domain_use_case.delete(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_repository_get_error(
        self, domain_use_case, mock_domain_repository
    ):
        """Test de gestion d'erreur lors de la vérification d'existence"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.delete(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_repository_delete_error(
        self, domain_use_case, mock_domain_repository, sample_domain
    ):
        """Test de gestion d'erreur lors de la suppression en base"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.return_value = sample_domain
        mock_domain_repository.delete.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.delete(domain_id)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.delete.assert_called_once_with(domain_id)

    @pytest.mark.asyncio
    async def test_delete_returns_false(
        self, domain_use_case, mock_domain_repository, sample_domain
    ):
        """Test de suppression qui retourne False (échec de suppression)"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.return_value = sample_domain
        mock_domain_repository.delete.return_value = False

        # Act
        result = await domain_use_case.delete(domain_id)

        # Assert
        assert result is False
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.delete.assert_called_once_with(domain_id)
