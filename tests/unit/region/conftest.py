from unittest.mock import AsyncMock

import pytest

from core.entities.region import RegionEntity
from core.interfaces.region_repository import IRegionRepository
from core.use_cases.region_use_case import RegionUseCase


@pytest.fixture
def mock_region_repository():
    """Mock for the region repository with a strict spec."""
    return AsyncMock(spec=IRegionRepository)


@pytest.fixture
def region_use_case(mock_region_repository):
    """Fixture to create a RegionUseCase instance with mocks."""
    return RegionUseCase(region_repository=mock_region_repository)


@pytest.fixture
def region_factory():
    """Factory to create RegionEntity instances with default values."""

    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default Region",
            "created_at": None,
            "updated_at": None,
        }
        return RegionEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def sample_region_data():
    """Fixture to create region data for input (without ID)."""
    return RegionEntity(
        id=None,
        name="Analamanga",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def sample_created_region():
    """Fixture to create a created region with ID."""
    return RegionEntity(
        id=1,
        name="Analamanga",
        created_at=None,
        updated_at=None,
    )
