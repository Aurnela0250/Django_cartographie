from unittest.mock import AsyncMock

import pytest

from core.entities.establishment import EstablishmentEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.rate import RateEntity
from core.interfaces.establishment_repository import IEstablishmentRepository
from core.interfaces.rate_repository import IRateRepository
from core.use_cases.establishment_use_case import EstablishmentUseCase


@pytest.fixture
def mock_establishment_repository():
    return AsyncMock(spec=IEstablishmentRepository)


@pytest.fixture
def mock_rate_repository():
    return AsyncMock(spec=IRateRepository)


@pytest.fixture
def establishment_use_case(mock_establishment_repository, mock_rate_repository):
    return EstablishmentUseCase(
        establishment_repository=mock_establishment_repository,
        rate_repository=mock_rate_repository,
    )


@pytest.fixture
def establishment_factory():
    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default Establishment",
            "description": "Default Description",
            "address": "Default Address",
            "phone": "1234567890",
            "email": "default@example.com",
            "website": "http://default.com",
            "establishment_type_id": 1,
            "region_id": 1,
            "city_id": 1,
            "created_at": None,
            "updated_at": None,
        }
        return EstablishmentEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def rate_factory():
    def _factory(**overrides):
        defaults = {
            "id": None,
            "user_id": 1,
            "establishment_id": 1,
            "rating": 4.5,
            "created_at": None,
            "updated_at": None,
        }
        return RateEntity(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def pagination_params_factory():
    def _factory(**overrides):
        defaults = {
            "page": 1,
            "page_size": 10,
        }
        return PaginationParams(**{**defaults, **overrides})

    return _factory


@pytest.fixture
def paginated_result_factory(establishment_factory):
    def _factory(items=None, total_items=0, page=1, per_page=10):
        if items is None:
            items = [establishment_factory() for _ in range(total_items)]
        total_pages = (total_items + per_page - 1) // per_page
        return PaginatedResult(
            items=items,
            total_items=total_items,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    return _factory
