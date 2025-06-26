from unittest.mock import AsyncMock

import pytest

from core.entities.mention import MentionEntity
from core.interfaces.mention_repository import IMentionRepository
from core.use_cases.mention_use_case import MentionUseCase


@pytest.fixture
def mock_mention_repository():
    """Mock for the mention repository with a strict spec."""
    return AsyncMock(spec=IMentionRepository)


@pytest.fixture
def mention_use_case(mock_mention_repository):
    """Fixture to create a MentionUseCase instance with mocks."""
    return MentionUseCase(mention_repository=mock_mention_repository)


@pytest.fixture
def mention_factory():
    """Factory to create MentionEntity instances with default values."""

    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default Mention",
            "domain_id": 1,
            "created_at": None,
            "updated_at": None,
        }
        return MentionEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def sample_mention_data():
    """Fixture to create mention data for input (without ID)."""
    return MentionEntity(
        id=None,
        name="Sciences de la vie",
        domain_id=1,
        created_at=None,
        updated_at=None,
    )


@pytest.fixture
def sample_created_mention():
    """Fixture to create a created mention with ID."""
    return MentionEntity(
        id=1,
        name="Sciences de la vie",
        domain_id=1,
        created_at=None,
        updated_at=None,
    )
