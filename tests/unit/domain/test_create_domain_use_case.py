from unittest.mock import Mock

import pytest

from core.entities.domain import DomainEntity
from core.interfaces.domain_repository import IDomainRepository
from core.use_cases.domain_use_case import DomainUseCase
from presentation.exceptions import (
    ConflictException,
    DatabaseException,
    DatabaseIntegrityException,
    InternalServerErrorException,
)


class TestCreateDomainUseCase:
    @pytest.fixture
    def mock_domain_repository(self):
        return Mock(spec=IDomainRepository)

    @pytest.fixture
    def domain_use_case(self, mock_domain_repository):
        return DomainUseCase(mock_domain_repository)

    async def test_create_domain_success(self, domain_use_case, mock_domain_repository):
        # Given
        domain_name = "Test Domain"
        domain_to_create = DomainEntity(name=domain_name)
        expected_domain = DomainEntity(name=domain_name)

        mock_domain_repository.create.return_value = expected_domain

        # When
        created_domain = await domain_use_case.create(domain_data=domain_to_create)

        # Then
        mock_domain_repository.create.assert_called_once_with(domain_to_create)
        assert created_domain == expected_domain

    async def test_create_domain_conflict_on_integrity_error(
        self, domain_use_case, mock_domain_repository
    ):
        # Given
        domain_name = "Test Domain"
        domain_to_create = DomainEntity(name=domain_name)
        mock_domain_repository.create.side_effect = DatabaseIntegrityException(
            "Duplicate entry"
        )

        # When / Then
        with pytest.raises(ConflictException):
            await domain_use_case.create(domain_data=domain_to_create)
        mock_domain_repository.create.assert_called_once_with(domain_to_create)

    async def test_create_domain_database_error_on_operational_error(
        self, domain_use_case, mock_domain_repository
    ):
        # Given
        domain_name = "Test Domain"
        domain_to_create = DomainEntity(name=domain_name)
        mock_domain_repository.create.side_effect = DatabaseException("DB error")

        # When / Then
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.create(domain_data=domain_to_create)
        mock_domain_repository.create.assert_called_once_with(domain_to_create)

    async def test_create_domain_unexpected_error(
        self, domain_use_case, mock_domain_repository
    ):
        # Given
        domain_name = "Test Domain"
        domain_to_create = DomainEntity(name=domain_name)
        mock_domain_repository.create.side_effect = Exception("Unexpected error")

        # When / Then
        with pytest.raises(InternalServerErrorException):
            await domain_use_case.create(domain_data=domain_to_create)
        mock_domain_repository.create.assert_called_once_with(domain_to_create)
