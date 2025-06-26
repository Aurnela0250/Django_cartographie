from unittest.mock import AsyncMock

import pytest

from core.entities.mention import MentionEntity
from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseIntegrityException,
)
from presentation.exceptions import (
    ConflictException,
    NotFoundException,
)


@pytest.mark.asyncio
async def test_update_mention_successfully(mention_use_case, mock_mention_repository):
    # Arrange
    mention_id = 1
    mention_data = {"name": "Updated Mention", "domain_id": 1}
    mention_entity_to_update = MentionEntity(**mention_data)
    updated_mention_entity = MentionEntity(id=mention_id, **mention_data)

    mock_mention_repository.update = AsyncMock(return_value=updated_mention_entity)

    # Act
    result = await mention_use_case.update(mention_id, mention_data)

    # Assert
    assert result == updated_mention_entity
    mock_mention_repository.update.assert_called_once_with(
        mention_id, mention_entity_to_update
    )


@pytest.mark.asyncio
async def test_update_mention_not_found(mention_use_case, mock_mention_repository):
    # Arrange
    mention_id = 1
    mention_data = {"name": "NonExistent Mention", "domain_id": 1}
    mention_entity_to_update = MentionEntity(**mention_data)
    mock_mention_repository.update = AsyncMock(
        side_effect=DatabaseDoesNotExistException("Mention not found")
    )

    # Act & Assert
    with pytest.raises(NotFoundException):
        await mention_use_case.update(mention_id, mention_data)
    mock_mention_repository.update.assert_called_once_with(
        mention_id, mention_entity_to_update
    )


@pytest.mark.asyncio
async def test_update_mention_conflict(mention_use_case, mock_mention_repository):
    # Arrange
    mention_id = 1
    mention_data = {"name": "Duplicate Mention", "domain_id": 1}
    mention_entity_to_update = MentionEntity(**mention_data)
    mock_mention_repository.update = AsyncMock(
        side_effect=DatabaseIntegrityException("Mention name already exists")
    )

    # Act & Assert
    with pytest.raises(ConflictException):
        await mention_use_case.update(mention_id, mention_data)
    mock_mention_repository.update.assert_called_once_with(
        mention_id, mention_entity_to_update
    )
