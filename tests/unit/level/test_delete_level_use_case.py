from unittest.mock import AsyncMock

import pytest

from core.use_cases.level_use_case import LevelUseCase
from presentation.exceptions import DatabaseDoesNotExistException, NotFoundException

pytestmark = pytest.mark.asyncio


async def test_delete_level_successfully(
    level_use_case: LevelUseCase, mock_level_repository: AsyncMock
):
    """
    Test case: Successfully deletes a level.
    """
    # Arrange
    level_id = 1
    mock_level_repository.delete.return_value = True

    # Act
    result = await level_use_case.delete(level_id)

    # Assert
    assert result is True
    mock_level_repository.delete.assert_called_once_with(level_id)


async def test_delete_level_not_found(
    level_use_case: LevelUseCase, mock_level_repository: AsyncMock
):
    """
    Test case: Level to be deleted is not found.
    """
    # Arrange
    level_id = 999
    mock_level_repository.delete.side_effect = DatabaseDoesNotExistException(
        "Level not found"
    )

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        await level_use_case.delete(level_id)

    assert "Resource not found" in str(exc_info.value)
    mock_level_repository.delete.assert_called_once_with(level_id)
