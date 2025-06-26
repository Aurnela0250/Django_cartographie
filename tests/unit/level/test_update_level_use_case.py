import pytest

from presentation.exceptions import (
    ConflictException,
    DatabaseDoesNotExistException,
    DatabaseIntegrityException,
    NotFoundException,
)


@pytest.mark.asyncio
async def test_update_level_successfully(
    level_use_case, mock_level_repository, level_factory
):
    """
    Test that a level is updated successfully.
    """
    # Arrange
    level_id = 1
    level_data = {"name": "Updated Level", "acronym": "UL"}
    existing_level = level_factory(id=level_id, name="Old Level", acronym="OL")
    updated_level = level_factory(id=level_id, **level_data)

    mock_level_repository.get.return_value = existing_level
    mock_level_repository.update.return_value = updated_level

    # Act
    result = await level_use_case.update(level_id, level_data)

    # Assert
    mock_level_repository.get.assert_called_once_with(level_id)
    mock_level_repository.update.assert_called_once()
    assert result == updated_level


@pytest.mark.asyncio
async def test_update_level_not_found(level_use_case, mock_level_repository):
    """
    Test that NotFoundException is raised when the level to update does not exist.
    """
    # Arrange
    level_id = 999
    level_data = {"name": "Non-existent Level"}
    mock_level_repository.get.side_effect = DatabaseDoesNotExistException(
        "Level not found"
    )

    # Act & Assert
    with pytest.raises(NotFoundException):
        await level_use_case.update(level_id, level_data)

    mock_level_repository.get.assert_called_once_with(level_id)
    mock_level_repository.update.assert_not_called()


@pytest.mark.asyncio
async def test_update_level_conflict(
    level_use_case, mock_level_repository, level_factory
):
    """
    Test that ConflictException is raised on integrity error (e.g., duplicate name).
    """
    # Arrange
    level_id = 1
    level_data = {"name": "Existing Name"}
    existing_level = level_factory(id=level_id, name="Old Level", acronym="OL")

    mock_level_repository.get.return_value = existing_level
    mock_level_repository.update.side_effect = DatabaseIntegrityException(
        "Duplicate name"
    )

    # Act & Assert
    with pytest.raises(ConflictException):
        await level_use_case.update(level_id, level_data)

    mock_level_repository.get.assert_called_once_with(level_id)
    mock_level_repository.update.assert_called_once()
