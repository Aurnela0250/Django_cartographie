from unittest.mock import AsyncMock, Mock

import pytest

from core.entities.domain import DomainEntity
from core.entities.filters import DomainFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.domain_repository import IDomainRepository
from core.use_cases.domain_use_case import DomainUseCase


@pytest.fixture
def mock_domain_repository():
    """Mock for the domain repository with a strict spec."""
    return AsyncMock(spec=IDomainRepository)


@pytest.fixture
def domain_use_case(mock_domain_repository):
    """Fixture to create a DomainUseCase instance with mocks."""
    return DomainUseCase(domain_repository=mock_domain_repository)


@pytest.fixture
def domain_factory():
    """Factory to create DomainEntity instances with default values."""

    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default Domain",
            "created_at": None,
            "updated_at": None,
        }
        return DomainEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def sample_domain():
    """Fixture to create a sample DomainEntity for tests."""
    return DomainEntity(
        id=1,
        name="Informatique",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def pagination_params():
    """Fixture to create PaginationParams for tests."""
    return PaginationParams(page=1, per_page=10)


@pytest.fixture
def domain_filters():
    """Fixture to create DomainFilters for tests."""
    return DomainFilters(name="Informatique")


@pytest.fixture
def mock_logger():
    """Mock for logger used in domain use cases."""
    return Mock()


@pytest.fixture
def sample_domain_data():
    """Fixture to create domain data for input (without ID)."""
    return DomainEntity(
        id=None,
        name="Sciences Informatiques",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def sample_created_domain():
    """Fixture to create a created domain with ID."""
    return DomainEntity(
        id=1,
        name="Sciences Informatiques",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def sample_domains(domain_factory):
    """Fixture to create a list of sample domains."""
    return [
        domain_factory(id=1, name="Informatique"),
        domain_factory(id=2, name="Mathématiques"),
        domain_factory(id=3, name="Sciences"),
    ]


@pytest.fixture
def paginated_result(sample_domains):
    """Fixture to create a paginated result with sample domains."""
    return PaginatedResult[DomainEntity](
        items=sample_domains,
        total_items=3,
        page=1,
        per_page=10,
        total_pages=1,
    )


@pytest.fixture
def existing_domain():
    """Fixture to create an existing domain for update tests."""
    return DomainEntity(
        id=1,
        name="Informatique",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def updated_domain_data():
    """Fixture to create domain update data."""
    return DomainEntity(
        id=1,
        name="Sciences Informatiques",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def updated_domain_result():
    """Fixture to create an updated domain result."""
    return DomainEntity(
        id=1,
        name="Sciences Informatiques",
        created_at=None,
        updated_at=None,
    )
