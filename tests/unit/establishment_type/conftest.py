"""Fixtures communes pour les tests de establishment_type"""

from unittest.mock import AsyncMock, Mock

import pytest

from core.entities.establishment_type import EstablishmentTypeEntity
from core.entities.filters import EstablishmentTypeFilters
from core.entities.pagination import PaginationParams
from core.interfaces.establishment_type_repository import IEstablishmentTypeRepository
from core.use_cases.establishment_type_use_case import EstablishmentTypeUseCase


@pytest.fixture
def mock_establishment_type_repository():
    """Mock du repository de type d'établissement avec spec strict"""
    return AsyncMock(spec=IEstablishmentTypeRepository)


@pytest.fixture
def mock_logger():
    """Mock du logger"""
    return Mock()


@pytest.fixture
def establishment_type_use_case(mock_establishment_type_repository):
    """Fixture pour créer une instance de EstablishmentTypeUseCase avec des mocks"""
    return EstablishmentTypeUseCase(
        establishment_type_repository=mock_establishment_type_repository,
    )


@pytest.fixture
def establishment_type_factory():
    """Factory pour créer des entités EstablishmentType de test"""

    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default Establishment Type",
            "created_at": None,
            "updated_at": None,
        }
        return EstablishmentTypeEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def pagination_params():
    """Paramètres de pagination d'exemple"""
    return PaginationParams(page=1, per_page=10)


@pytest.fixture
def establishment_type_filters():
    """Filtres d'exemple pour les types d'établissement"""
    return EstablishmentTypeFilters(name="Lycée")
