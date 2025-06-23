import pytest

from core.entities.domain import DomainEntity
from presentation.exceptions import (
    ConflictException,
    DatabaseDoesNotExistException,
    DatabaseIntegrityException,
    InternalServerErrorException,
    NotFoundException,
)


class TestUpdateDomainUseCase:

    async def test_update_domain_success(
        self,
        domain_use_case,
        mock_domain_repository,
    ):
        # Given
        domain_id = 1
        domain_data = DomainEntity(name="Updated Domain", updated_by=1)
        existing_domain = DomainEntity(id=domain_id, name="Original Domain")
        updated_domain_entity = DomainEntity(
            id=domain_id,
            name="Updated Domain",
            updated_by=1,
        )

        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.update.return_value = updated_domain_entity

        # When
        result = await domain_use_case.update(domain_id, domain_data)

        # Then
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.update.assert_called_once_with(domain_id, domain_data)
        assert result == updated_domain_entity
        assert result.updated_by is not None
        assert isinstance(result.updated_by, int)

    async def test_update_domain_success_no_name_change(
        self, domain_use_case, mock_domain_repository
    ):
        # Given
        domain_id = 1
        domain_name = "Same Domain"
        domain_data = DomainEntity(name=domain_name)
        existing_domain = DomainEntity(id=domain_id, name=domain_name)

        mock_domain_repository.get.return_value = existing_domain

        # When
        result = await domain_use_case.update(domain_id, domain_data)

        # Then
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.update.assert_not_called()
        assert result == existing_domain

    async def test_update_domain_not_found(
        self, domain_use_case, mock_domain_repository
    ):
        # Given
        domain_id = 1
        domain_data = DomainEntity(name="Test")
        mock_domain_repository.get.side_effect = DatabaseDoesNotExistException

        # When / Then
        with pytest.raises(NotFoundException):
            await domain_use_case.update(domain_id, domain_data)
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.update.assert_not_called()

    async def test_update_domain_conflict_on_integrity_error(
        self, domain_use_case, mock_domain_repository
    ):
        # Given
        domain_id = 1
        domain_data = DomainEntity(name="Updated Domain")
        existing_domain = DomainEntity(id=domain_id, name="Original Domain")

        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.update.side_effect = DatabaseIntegrityException

        # When / Then
        with pytest.raises(ConflictException):
            await domain_use_case.update(domain_id, domain_data)
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.update.assert_called_once_with(domain_id, domain_data)

    async def test_update_domain_unexpected_error(
        self, domain_use_case, mock_domain_repository
    ):
        # Given
        domain_id = 1
        domain_data = DomainEntity(name="Updated Domain")
        existing_domain = DomainEntity(id=domain_id, name="Original Domain")

        mock_domain_repository.get.return_value = existing_domain
        mock_domain_repository.update.side_effect = Exception("Unexpected error")

        # When / Then
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.update(domain_id, domain_data)
        mock_domain_repository.get.assert_called_once_with(domain_id)
        mock_domain_repository.update.assert_called_once_with(domain_id, domain_data)
