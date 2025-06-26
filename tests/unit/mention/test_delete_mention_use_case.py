import pytest
from presentation.exceptions import (
    DatabaseDoesNotExistException,
    NotFoundException,
)

pytestmark = pytest.mark.asyncio


async def test_delete_mention_successfully(mention_use_case, mock_mention_repository):
    # Arrange
    mention_id = 1
    mock_mention_repository.delete.return_value = True

    # Act
    result = await mention_use_case.delete(mention_id)

    # Assert
    assert result is True
    mock_mention_repository.delete.assert_called_once_with(mention_id)


async def test_delete_mention_not_found(mention_use_case, mock_mention_repository):
    # Arrange
    mention_id = 1
    mock_mention_repository.delete.side_effect = DatabaseDoesNotExistException(
        "Mention not found"
    )

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        await mention_use_case.delete(mention_id)

    assert "Mention not found" in str(exc_info.value)
    mock_mention_repository.delete.assert_called_once_with(mention_id)
