import pytest

from presentation.exceptions import ConflictException, InternalServerErrorException


class TestDomainCreateUseCase:
    """Unit tests for the create method of DomainUseCase."""

    class TestSuccess:
        """Tests for success cases."""

        @pytest.mark.asyncio
        async def test_should_create_domain_successfully(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for successful domain creation."""
            # Given
            new_domain = domain_factory(name="Science")
            created_domain = domain_factory(id=1, name="Science")
            mock_domain_repository.get_by_name.return_value = None
            mock_domain_repository.create.return_value = created_domain

            # When
            result = await domain_use_case.create(new_domain)

            # Then
            assert result == created_domain
            mock_domain_repository.get_by_name.assert_called_once_with(new_domain.name)
            mock_domain_repository.create.assert_called_once_with(new_domain)

    class TestFailures:
        """Tests for failure cases."""

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_domain_already_exists(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for domain creation with an already existing name."""
            # Given
            new_domain = domain_factory(name="Science")
            existing_domain = domain_factory(id=1, name="Science")
            mock_domain_repository.get_by_name.return_value = existing_domain

            # When & Then
            with pytest.raises(ConflictException):
                await domain_use_case.create(new_domain)

            mock_domain_repository.get_by_name.assert_called_once_with(new_domain.name)
            mock_domain_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for error handling during the existence check."""
            # Given
            new_domain = domain_factory(name="Science")
            mock_domain_repository.get_by_name.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.create(new_domain)

            mock_domain_repository.get_by_name.assert_called_once_with(new_domain.name)
            mock_domain_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_create_failure(
            self, domain_use_case, mock_domain_repository, domain_factory
        ):
            """Test for error handling during database creation."""
            # Given
            new_domain = domain_factory(name="Science")
            mock_domain_repository.get_by_name.return_value = None
            mock_domain_repository.create.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.create(new_domain)

            mock_domain_repository.get_by_name.assert_called_once_with(new_domain.name)
            mock_domain_repository.create.assert_called_once_with(new_domain)

    @pytest.mark.asyncio
    async def test_create_success(
        self,
        domain_use_case,
        mock_domain_repository,
        sample_domain_data,
        sample_created_domain,
    ):
        """Test de création de domaine réussie"""
        # Arrange
        mock_domain_repository.get_by_name.return_value = None
        mock_domain_repository.create.return_value = sample_created_domain

        # Act
        result = await domain_use_case.create(sample_domain_data)

        # Assert
        assert result == sample_created_domain
        mock_domain_repository.get_by_name.assert_called_once_with(
            sample_domain_data.name
        )
        mock_domain_repository.create.assert_called_once_with(sample_domain_data)

    @pytest.mark.asyncio
    async def test_create_domain_already_exists(
        self,
        domain_use_case,
        mock_domain_repository,
        sample_domain_data,
        sample_created_domain,
    ):
        """Test de création de domaine avec nom déjà existant"""
        # Arrange
        mock_domain_repository.get_by_name.return_value = sample_created_domain

        # Act & Assert
        with pytest.raises(ConflictException):
            await domain_use_case.create(sample_domain_data)

        mock_domain_repository.get_by_name.assert_called_once_with(
            sample_domain_data.name
        )
        mock_domain_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_repository_get_by_name_error(
        self, domain_use_case, mock_domain_repository, sample_domain_data
    ):
        """Test de gestion d'erreur lors de la vérification d'existence"""
        # Arrange
        mock_domain_repository.get_by_name.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.create(sample_domain_data)

        mock_domain_repository.get_by_name.assert_called_once_with(
            sample_domain_data.name
        )
        mock_domain_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_repository_create_error(
        self, domain_use_case, mock_domain_repository, sample_domain_data
    ):
        """Test de gestion d'erreur lors de la création en base"""
        # Arrange
        mock_domain_repository.get_by_name.return_value = None
        mock_domain_repository.create.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.create(sample_domain_data)

        mock_domain_repository.get_by_name.assert_called_once_with(
            sample_domain_data.name
        )
        mock_domain_repository.create.assert_called_once_with(sample_domain_data)
