from unittest.mock import AsyncMock

import pytest

from presentation.exceptions import (
    ConflictException,
    DatabaseIntegrityException,
    InternalServerErrorException,
)


class TestCreateMentionUseCase:
    @pytest.mark.asyncio
    async def test_create_mention_success(
        self,
        mention_use_case,
        mock_mention_repository,
        sample_mention_data,
        sample_created_mention,
    ):
        # Given
        mock_mention_repository.create = AsyncMock(return_value=sample_created_mention)

        # When
        created_mention = await mention_use_case.create(
            mention_data=sample_mention_data
        )

        # Then
        mock_mention_repository.create.assert_called_once_with(sample_mention_data)
        assert created_mention == sample_created_mention

    @pytest.mark.asyncio
    async def test_create_mention_conflict_on_integrity_error(
        self, mention_use_case, mock_mention_repository, sample_mention_data
    ):
        # Given
        mock_mention_repository.create.side_effect = DatabaseIntegrityException(
            "Duplicate entry"
        )

        # When / Then
        with pytest.raises(ConflictException):
            await mention_use_case.create(mention_data=sample_mention_data)
        mock_mention_repository.create.assert_called_once_with(sample_mention_data)

    @pytest.mark.asyncio
    async def test_create_mention_unexpected_error(
        self, mention_use_case, mock_mention_repository, sample_mention_data
    ):
        # Given
        mock_mention_repository.create.side_effect = Exception("Unexpected error")

        # When / Then
        with pytest.raises(InternalServerErrorException):
            await mention_use_case.create(mention_data=sample_mention_data)
        mock_mention_repository.create.assert_called_once_with(sample_mention_data)
