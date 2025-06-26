from unittest.mock import Mock

import pytest

from core.entities.mention import MentionEntity
from core.use_cases.mention_use_case import MentionUseCase
from presentation.exceptions import DatabaseDoesNotExistException, NotFoundException


@pytest.mark.asyncio
async def test_get_mention_successfully(
    mention_use_case: MentionUseCase, mock_mention_repository: Mock
):
    # Arrange
    mention_id = 1
    expected_mention = MentionEntity(id=mention_id, name="Mention 1", domain_id=1)
    mock_mention_repository.get.return_value = expected_mention

    # Act
    result = await mention_use_case.get(mention_id)

    # Assert
    assert result == expected_mention
    mock_mention_repository.get.assert_called_once_with(mention_id)


@pytest.mark.asyncio
async def test_get_mention_not_found(
    mention_use_case: MentionUseCase, mock_mention_repository: Mock
):
    # Arrange
    mention_id = 1
    mock_mention_repository.get.side_effect = DatabaseDoesNotExistException(
        "Mention not found"
    )

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        await mention_use_case.get(mention_id)

    assert "Mention not found" in str(exc_info.value)
    mock_mention_repository.get.assert_called_once_with(mention_id)
