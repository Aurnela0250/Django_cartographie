import pytest

from core.entities.domain import DomainEntity
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)


class TestDomainUpdateUseCase:
    """Unit tests for the update method of DomainUseCase."""

    class TestSuccess:
        """Tests for success cases."""

        @pytest.mark.asyncio
        async def test_should_update_domain_successfully(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for successful domain update."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            updated_domain_data = domain_factory(id=domain_id, name="Mathematics")
            updated_domain_result = domain_factory(id=domain_id, name="Mathematics")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.get_by_name.return_value = None
            mock_domain_repository.update.return_value = updated_domain_result

            # When
            result = await domain_use_case.update(domain_id, updated_domain_data)

            # Then
            assert result == updated_domain_result
            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_called_once_with(
                updated_domain_data.name
            )
            mock_domain_repository.update.assert_called_once_with(
                domain_id, updated_domain_data
            )

        @pytest.mark.asyncio
        async def test_should_update_domain_with_same_name_successfully(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for successful domain update with the same name."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            same_name_data = domain_factory(id=domain_id, name="Science")
            updated_domain_result = domain_factory(id=domain_id, name="Science")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.update.return_value = updated_domain_result

            # When
            result = await domain_use_case.update(domain_id, same_name_data)

            # Then
            assert result == updated_domain_result
            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_not_called()
            mock_domain_repository.update.assert_called_once_with(
                domain_id, same_name_data
            )

        @pytest.mark.asyncio
        async def test_should_update_domain_with_existing_name_for_same_domain(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for successful domain update where the name exists but is the same domain."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            updated_domain_data = domain_factory(id=domain_id, name="Mathematics")
            same_domain_by_name = domain_factory(id=domain_id, name="Mathematics")
            updated_domain_result = domain_factory(id=domain_id, name="Mathematics")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.get_by_name.return_value = same_domain_by_name
            mock_domain_repository.update.return_value = updated_domain_result

            # When
            result = await domain_use_case.update(domain_id, updated_domain_data)

            # Then
            assert result == updated_domain_result
            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_called_once_with(
                updated_domain_data.name
            )
            mock_domain_repository.update.assert_called_once_with(
                domain_id, updated_domain_data
            )

    class TestFailures:
        """Tests for failure cases."""

        @pytest.mark.asyncio
        async def test_should_raise_not_found_when_domain_does_not_exist(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for update of a non-existent domain."""
            # Given
            domain_id = 999
            updated_domain_data = domain_factory(id=domain_id, name="Mathematics")
            mock_domain_repository.get.return_value = None

            # When & Then
            with pytest.raises(NotFoundException):
                await domain_use_case.update(domain_id, updated_domain_data)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_not_called()
            mock_domain_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_name_already_exists(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for update with an already existing name."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            updated_domain_data = domain_factory(id=domain_id, name="Mathematics")
            other_domain = domain_factory(id=2, name="Mathematics")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.get_by_name.return_value = other_domain

            # When & Then
            with pytest.raises(ConflictException):
                await domain_use_case.update(domain_id, updated_domain_data)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_called_once_with(
                updated_domain_data.name
            )
            mock_domain_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_failure(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for error handling during domain retrieval."""
            # Given
            domain_id = 1
            updated_domain_data = domain_factory(id=domain_id, name="Mathematics")
            mock_domain_repository.get.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.update(domain_id, updated_domain_data)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_not_called()
            mock_domain_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for error handling during name existence check."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            updated_domain_data = domain_factory(id=domain_id, name="Mathematics")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.get_by_name.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.update(domain_id, updated_domain_data)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_called_once_with(
                updated_domain_data.name
            )
            mock_domain_repository.update.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_update_failure(
            self,
            domain_use_case,
            mock_domain_repository,
            domain_factory,
        ):
            """Test for error handling during database update."""
            # Given
            domain_id = 1
            existing_domain = domain_factory(id=domain_id, name="Science")
            updated_domain_data = domain_factory(id=domain_id, name="Mathematics")
            mock_domain_repository.get.return_value = existing_domain
            mock_domain_repository.get_by_name.return_value = None
            mock_domain_repository.update.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await domain_use_case.update(domain_id, updated_domain_data)

            mock_domain_repository.get.assert_called_once_with(domain_id)
            mock_domain_repository.get_by_name.assert_called_once_with(
                updated_domain_data.name
            )
            mock_domain_repository.update.assert_called_once_with(
                domain_id, updated_domain_data
            )

    @pytest.mark.asyncio
    async def test_update_success(
        self,
        domain_use_case,
        mock_domain_repository,
        existing_domain,
        updated_domain_data,
        updated_domain_result,
    ):
        """Test de mise à jour de domaine réussie"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.get_by_name.return_value = None
        mock_domain_repository.update.return_value = updated_domain_result

        # Act
        result = await domain_use_case.update(domain_id, updated_domain_data)

        # Assert
        assert result == updated_domain_result
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.get_by_name.assert_called_once_with(
            updated_domain_data.name
        )
        mock_domain_repository.update.assert_called_once_with(
            domain_id, updated_domain_data
        )

    @pytest.mark.asyncio
    async def test_update_same_name_success(
        self,
        domain_use_case,
        mock_domain_repository,
        existing_domain,
        updated_domain_result,
    ):
        """Test de mise à jour de domaine avec le même nom (réussie)"""
        # Arrange
        domain_id = 1
        # Données avec le même nom que le domaine existant
        same_name_data = DomainEntity(
            id=1,
            name="Informatique",  # Même nom
            created_at=None,
            updated_at=None,
        )

        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.update.return_value = updated_domain_result

        # Act
        result = await domain_use_case.update(domain_id, same_name_data)

        # Assert
        assert result == updated_domain_result
        mock_domain_repository.get.assert_called_once_with(domain_id)
        # get_by_name ne doit pas être appelé si le nom n'a pas changé
        mock_domain_repository.get_by_name.assert_not_called()
        mock_domain_repository.update.assert_called_once_with(domain_id, same_name_data)

    @pytest.mark.asyncio
    async def test_update_domain_not_found(
        self, domain_use_case, mock_domain_repository, updated_domain_data
    ):
        """Test de mise à jour d'un domaine inexistant"""
        # Arrange
        domain_id = 999
        mock_domain_repository.get.return_value = None

        # Act & Assert
        with pytest.raises(NotFoundException):
            await domain_use_case.update(domain_id, updated_domain_data)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.get_by_name.assert_not_called()
        mock_domain_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_name_already_exists(
        self,
        domain_use_case,
        mock_domain_repository,
        existing_domain,
        updated_domain_data,
    ):
        """Test de mise à jour avec un nom déjà existant"""
        # Arrange
        domain_id = 1
        # Un autre domaine avec le nouveau nom
        other_domain = DomainEntity(
            id=2,
            name="Sciences Informatiques",
            created_at=None,
            updated_at=None,
        )

        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.get_by_name.return_value = other_domain

        # Act & Assert
        with pytest.raises(ConflictException):
            await domain_use_case.update(domain_id, updated_domain_data)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.get_by_name.assert_called_once_with(
            updated_domain_data.name
        )
        mock_domain_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_name_exists_same_domain(
        self,
        domain_use_case,
        mock_domain_repository,
        existing_domain,
        updated_domain_data,
        updated_domain_result,
    ):
        """Test de mise à jour où le nom existe mais c'est le même domaine (mise à jour autorisée)"""
        # Arrange
        domain_id = 1
        # Le même domaine trouvé par nom (cas où on met à jour avec le même nom)
        same_domain_by_name = DomainEntity(
            id=1,  # Même ID
            name="Sciences Informatiques",
            created_at=None,
            updated_at=None,
        )

        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.get_by_name.return_value = same_domain_by_name
        mock_domain_repository.update.return_value = updated_domain_result

        # Act
        result = await domain_use_case.update(domain_id, updated_domain_data)

        # Assert
        assert result == updated_domain_result
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.get_by_name.assert_called_once_with(
            updated_domain_data.name
        )
        mock_domain_repository.update.assert_called_once_with(
            domain_id, updated_domain_data
        )

    @pytest.mark.asyncio
    async def test_update_repository_get_error(
        self, domain_use_case, mock_domain_repository, updated_domain_data
    ):
        """Test de gestion d'erreur lors de la récupération du domaine existant"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.update(domain_id, updated_domain_data)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.get_by_name.assert_not_called()
        mock_domain_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_repository_get_by_name_error(
        self,
        domain_use_case,
        mock_domain_repository,
        existing_domain,
        updated_domain_data,
    ):
        """Test de gestion d'erreur lors de la vérification d'existence du nom"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.get_by_name.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.update(domain_id, updated_domain_data)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.get_by_name.assert_called_once_with(
            updated_domain_data.name
        )
        mock_domain_repository.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_repository_update_error(
        self,
        domain_use_case,
        mock_domain_repository,
        existing_domain,
        updated_domain_data,
    ):
        """Test de gestion d'erreur lors de la mise à jour en base"""
        # Arrange
        domain_id = 1
        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.get_by_name.return_value = None
        mock_domain_repository.update.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.update(domain_id, updated_domain_data)

        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.get_by_name.assert_called_once_with(
            updated_domain_data.name
        )
        mock_domain_repository.update.assert_called_once_with(
            domain_id, updated_domain_data
        )
