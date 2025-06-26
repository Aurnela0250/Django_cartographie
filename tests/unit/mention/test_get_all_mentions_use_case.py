from unittest.mock import AsyncMock

import pytest

from core.entities.mention import MentionEntity
from core.entities.pagination import PaginationParams
from presentation.exceptions import InternalServerErrorException
from presentation.schemas.pagination import PaginatedResult


# Test for successful retrieval of all mentions
async def test_get_all_mentions_success(mention_use_case, mock_mention_repository):
    """
    GIVEN a mention use case
    WHEN get_all is called
    THEN it should return a paginated result of mentions
    """
    # GIVEN
    mock_mentions = [
        MentionEntity(id=1, name="Mention 1", domain_id=1),
        MentionEntity(id=2, name="Mention 2", domain_id=1),
    ]
    mock_paginated_result = PaginatedResult(
        items=mock_mentions,
        total_items=2,
        page=1,
        per_page=10,
        total_pages=1,
        next_page=None,
        previous_page=None,
    )
    mock_mention_repository.get_all = AsyncMock(return_value=mock_paginated_result)

    # WHEN
    pagination_params = PaginationParams(page=1, per_page=10)
    result = await mention_use_case.get_all(pagination_params=pagination_params)

    # THEN
    assert isinstance(result, PaginatedResult)
    assert result.items == mock_mentions
    assert result.total_items == 2
    mock_mention_repository.get_all.assert_called_once_with(
        pagination_params=pagination_params
    )


# Test for the case where the repository returns an empty paginated result
async def test_get_all_mentions_empty(mention_use_case, mock_mention_repository):
    """
    GIVEN a mention use case
    WHEN get_all is called and the repository returns an empty list
    THEN it should return an empty paginated result
    """
    # GIVEN
    mock_paginated_result = PaginatedResult(
        items=[],
        total_items=0,
        page=1,
        per_page=10,
        total_pages=0,
        next_page=None,
        previous_page=None,
    )
    mock_mention_repository.get_all = AsyncMock(return_value=mock_paginated_result)

    # WHEN
    pagination_params = PaginationParams(page=1, per_page=10)
    result = await mention_use_case.get_all(pagination_params=pagination_params)

    # THEN
    assert isinstance(result, PaginatedResult)
    assert result.items == []
    assert result.total_items == 0
    mock_mention_repository.get_all.assert_called_once_with(
        pagination_params=pagination_params
    )


# Test for a generic exception from the repository, which should be re-raised as InternalServerErrorException
async def test_get_all_mentions_internal_error(
    mention_use_case, mock_mention_repository
):
    """
    GIVEN a mention use case
    WHEN get_all is called and the repository raises a generic exception
    THEN it should re-raise an InternalServerErrorException
    """
    # GIVEN
    error_message = "A repository error occurred"
    mock_mention_repository.get_all = AsyncMock(side_effect=Exception(error_message))

    # WHEN / THEN
    with pytest.raises(InternalServerErrorException, match="Server error. Please try again later."):
        pagination_params = PaginationParams(page=1, per_page=10)
        await mention_use_case.get_all(pagination_params=pagination_params)

    mock_mention_repository.get_all.assert_called_once_with(
        pagination_params=pagination_params
    )
