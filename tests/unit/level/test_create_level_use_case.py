import pytest

from core.entities.level import LevelEntity
from core.use_cases.level_use_case import LevelUseCase
from presentation.exceptions import (
    ConflictException,
    DatabaseException,
    DatabaseIntegrityException,
    InternalServerErrorException,
)


class TestCreateLevelUseCase:
    class TestSuccess:
        @pytest.mark.asyncio
        async def test_create_level_success(
            self,
            level_use_case: LevelUseCase,
            mock_level_repository,
            sample_level_data: LevelEntity,
            sample_created_level: LevelEntity,
        ):
            # Given
            mock_level_repository.create.return_value = sample_created_level

            # When
            created_level = await level_use_case.create(level_data=sample_level_data)

            # Then
            mock_level_repository.create.assert_called_once_with(sample_level_data)
            assert created_level == sample_created_level

    class TestFailures:
        @pytest.mark.asyncio
        async def test_create_level_conflict_on_integrity_error(
            self,
            level_use_case: LevelUseCase,
            mock_level_repository,
            sample_level_data: LevelEntity,
        ):
            # Given
            mock_level_repository.create.side_effect = DatabaseIntegrityException(
                "Duplicate entry"
            )

            # When / Then
            with pytest.raises(ConflictException):
                await level_use_case.create(level_data=sample_level_data)
            mock_level_repository.create.assert_called_once_with(sample_level_data)

        @pytest.mark.asyncio
        async def test_create_level_database_error_on_operational_error(
            self,
            level_use_case: LevelUseCase,
            mock_level_repository,
            sample_level_data: LevelEntity,
        ):
            # Given
            mock_level_repository.create.side_effect = DatabaseException("DB error")

            # When / Then
            with pytest.raises(InternalServerErrorException):
                await level_use_case.create(level_data=sample_level_data)
            mock_level_repository.create.assert_called_once_with(sample_level_data)

        @pytest.mark.asyncio
        async def test_create_level_unexpected_error(
            self,
            level_use_case: LevelUseCase,
            mock_level_repository,
            sample_level_data: LevelEntity,
        ):
            # Given
            mock_level_repository.create.side_effect = Exception("Unexpected error")

            # When / Then
            with pytest.raises(InternalServerErrorException):
                await level_use_case.create(level_data=sample_level_data)
            mock_level_repository.create.assert_called_once_with(sample_level_data)
