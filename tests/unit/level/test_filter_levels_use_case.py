from unittest.mock import AsyncMock

import pytest

from core.entities.filters import LevelFilters
from core.entities.level import LevelEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from presentation.exceptions import InternalServerErrorException


@pytest.mark.asyncio
async def test_filter_with_results(level_use_case, mock_level_repository):
    # Arrange
    filters = LevelFilters(name="L1")
    pagination_params = PaginationParams(page=1, per_page=10)
    expected_levels = [LevelEntity(id=1, name="L1")]
    paginated_result = PaginatedResult(
        items=expected_levels, total_items=1, page=1, per_page=10, total_pages=1
    )

    mock_level_repository.filter = AsyncMock(return_value=paginated_result)

    # Act
    result = await level_use_case.filter(
        pagination_params=pagination_params, filters=filters
    )

    # Assert
    mock_level_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )
    assert result == paginated_result
    assert result.items[0].name == "L1"


@pytest.mark.asyncio
async def test_filter_with_no_results(level_use_case, mock_level_repository):
    # Arrange
    filters = LevelFilters(name="NonExistent")
    pagination_params = PaginationParams(page=1, per_page=10)
    paginated_result = PaginatedResult(
        items=[], total_items=0, page=1, per_page=10, total_pages=0
    )

    mock_level_repository.filter = AsyncMock(return_value=paginated_result)

    # Act
    result = await level_use_case.filter(
        pagination_params=pagination_params, filters=filters
    )

    # Assert
    mock_level_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )
    assert result == paginated_result
    assert len(result.items) == 0


@pytest.mark.asyncio
async def test_filter_with_empty_filters(level_use_case, mock_level_repository):
    # Arrange
    filters = LevelFilters()
    pagination_params = PaginationParams(page=1, per_page=10)
    expected_levels = [LevelEntity(id=1, name="L1"), LevelEntity(id=2, name="L2")]
    paginated_result = PaginatedResult(
        items=expected_levels, total_items=2, page=1, per_page=10, total_pages=1
    )

    mock_level_repository.filter = AsyncMock(return_value=paginated_result)

    # Act
    result = await level_use_case.filter(
        pagination_params=pagination_params, filters=filters
    )

    # Assert
    mock_level_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )
    assert result == paginated_result


@pytest.mark.asyncio
async def test_filter_raises_internal_server_error(
    level_use_case, mock_level_repository
):
    # Arrange
    filters = LevelFilters(name="L1")
    pagination_params = PaginationParams(page=1, per_page=10)

    mock_level_repository.filter.side_effect = Exception("Generic repository error")

    # Act & Assert
    with pytest.raises(InternalServerErrorException):
        await level_use_case.filter(
            pagination_params=pagination_params, filters=filters
        )
