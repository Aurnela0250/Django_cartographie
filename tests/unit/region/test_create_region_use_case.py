import pytest

from core.use_cases.region_use_case import ConflictException
from infrastructure.db.tortoise.region_repository_impl import DatabaseIntegrityException


class TestCreateRegionUseCase:

    @pytest.mark.asyncio
    async def test_create_region_success(
        self,
        region_use_case,
        mock_region_repository,
        sample_region_data,
        sample_created_region,
    ):
        # Given
        mock_region_repository.create.return_value = sample_created_region

        # When
        created_region = await region_use_case.create(region_data=sample_region_data)

        # Then
        mock_region_repository.create.assert_called_once_with(sample_region_data)
        assert created_region == sample_created_region

    @pytest.mark.asyncio
    async def test_create_region_conflict_on_integrity_error(
        self, region_use_case, mock_region_repository, sample_region_data
    ):
        # Given
        mock_region_repository.create.side_effect = DatabaseIntegrityException(
            "Duplicate entry"
        )

        # When / Then
        with pytest.raises(ConflictException):
            await region_use_case.create(region_data=sample_region_data)
        mock_region_repository.create.assert_called_once_with(sample_region_data)
