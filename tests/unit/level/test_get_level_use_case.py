import pytest
from unittest.mock import AsyncMock

from core.entities.level import LevelEntity
from core.use_cases.level_use_case import LevelUseCase
from presentation.exceptions import DatabaseDoesNotExistException, NotFoundException


class TestGetLevelUseCase:
    class TestSuccess:
        @pytest.mark.asyncio
        async def test_get_level_successfully(
            self,
            level_use_case: LevelUseCase,
            mock_level_repository: AsyncMock,
            sample_created_level: LevelEntity,
        ):
            # Given
            assert (
                sample_created_level.id is not None
            ), "Sample created level must have an ID for this test"
            level_id = sample_created_level.id
            mock_level_repository.get.return_value = sample_created_level

            # When
            result = await level_use_case.get(level_id)

            # Then
            mock_level_repository.get.assert_called_once_with(level_id)
            assert result == sample_created_level

    class TestFailures:
        @pytest.mark.asyncio
        async def test_get_level_raises_not_found(
            self,
            level_use_case: LevelUseCase,
            mock_level_repository: AsyncMock,
        ):
            # Given
            level_id = 999  # An ID that doesn't exist
            mock_level_repository.get.side_effect = DatabaseDoesNotExistException

            # When / Then
            with pytest.raises(NotFoundException):
                await level_use_case.get(level_id)
            mock_level_repository.get.assert_called_once_with(level_id)
