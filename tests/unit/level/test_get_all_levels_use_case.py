from unittest.mock import AsyncMock

import pytest

from core.entities.level import LevelEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.use_cases.level_use_case import LevelUseCase
from presentation.exceptions import InternalServerErrorException


@pytest.mark.asyncio
async def test_get_all_levels_successfully(
    level_use_case: LevelUseCase, mock_level_repository: AsyncMock
):
    """
    Should return a PaginatedResult of LevelEntity on successful retrieval.
    """
    # Arrange
    expected_levels = [
        LevelEntity(id=1, name="Level 1"),
        LevelEntity(id=2, name="Level 2"),
    ]
    pagination = PaginationParams(page=1, per_page=10)
    expected_result = PaginatedResult(
        items=expected_levels,
        total_items=len(expected_levels),
        page=pagination.page,
        per_page=pagination.per_page,
        total_pages=1,
    )
    mock_level_repository.get_all.return_value = expected_result

    # Act
    result = await level_use_case.get_all(pagination)

    # Assert
    assert result == expected_result
    mock_level_repository.get_all.assert_called_once_with(pagination_params=pagination)


@pytest.mark.asyncio
async def test_get_all_levels_empty_list(
    level_use_case: LevelUseCase, mock_level_repository: AsyncMock
):
    """
    Should return an empty PaginatedResult when no levels exist.
    """
    # Arrange
    pagination = PaginationParams(page=1, per_page=10)
    expected_result = PaginatedResult(
        items=[],
        total_items=0,
        page=pagination.page,
        per_page=pagination.per_page,
        total_pages=0,
    )
    mock_level_repository.get_all.return_value = expected_result

    # Act
    result = await level_use_case.get_all(pagination)

    # Assert
    assert result == expected_result
    mock_level_repository.get_all.assert_called_once_with(pagination_params=pagination)


@pytest.mark.asyncio
async def test_get_all_levels_internal_server_error(
    level_use_case: LevelUseCase, mock_level_repository: AsyncMock
):
    """
    Should raise InternalServerErrorException on repository failure.
    """
    # Arrange
    pagination = PaginationParams(page=1, per_page=10)
    mock_level_repository.get_all.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(InternalServerErrorException):
        await level_use_case.get_all(pagination)

    mock_level_repository.get_all.assert_called_once_with(pagination_params=pagination)
