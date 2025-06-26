from unittest.mock import AsyncMock

import pytest

from core.entities.level import LevelEntity
from core.interfaces.level_repository import ILevelRepository
from core.use_cases.level_use_case import LevelUseCase


@pytest.fixture
def mock_level_repository():
    """Mock for the level repository with a strict spec."""
    return AsyncMock(spec=ILevelRepository)


@pytest.fixture
def level_use_case(mock_level_repository):
    """Fixture to create a LevelUseCase instance with mocks."""
    return LevelUseCase(level_repository=mock_level_repository)


@pytest.fixture
def level_factory():
    """Factory to create LevelEntity instances with default values."""

    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default Level",
            "created_at": None,
            "updated_at": None,
        }
        return LevelEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def sample_level_data():
    """Fixture to create level data for input (without ID)."""
    return LevelEntity(
        id=None,
        name="Master",
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def sample_created_level():
    """Fixture to create a created level with ID."""
    return LevelEntity(
        id=1,
        name="Master",
        created_at=None,
        updated_at=None,
    )
