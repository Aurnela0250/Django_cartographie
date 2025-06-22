"""
Configuration et fixtures communes pour les tests unitaires du module City
"""

from unittest.mock import AsyncMock

import pytest

from core.entities.city import CityEntity
from core.interfaces.city_repository import ICityRepository
from core.use_cases.city_use_case import CityUseCase


@pytest.fixture
def mock_city_repository():
    """Mock du repository de ville avec spec strict"""
    return AsyncMock(spec=ICityRepository)


@pytest.fixture
def city_use_case(mock_city_repository):
    """Fixture pour créer une instance de CityUseCase avec des mocks"""
    return CityUseCase(city_repository=mock_city_repository)


@pytest.fixture
def city_factory():
    """Factory pour créer des entités CityEntity avec des valeurs par défaut"""

    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default City",
            "region_id": 1,
            "created_at": None,
            "updated_at": None,
        }
        return CityEntity(**{**defaults, **overrides})

    return _factory
