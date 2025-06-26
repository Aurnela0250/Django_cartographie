import pytest
from unittest.mock import AsyncMock

from core.entities.filters import MentionFilters
from core.entities.mention import MentionEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from presentation.exceptions import InternalServerErrorException


async def test_filter_mentions_with_results(mention_use_case, mock_mention_repository):
    """
    GIVEN a mention use case and valid filters
    WHEN filter is called and the repository returns matching mentions
    THEN it should return a paginated result of mentions
    """
    # GIVEN
    pagination_params = PaginationParams(page=1, per_page=10)
    filters = MentionFilters(name="Science")
    mock_mentions = [MentionEntity(id=1, name="Sciences de la vie", domain_id=1)]
    mock_paginated_result = PaginatedResult(
        items=mock_mentions,
        total_items=1,
        page=1,
        per_page=10,
        total_pages=1,
        next_page=None,
        previous_page=None,
    )
    mock_mention_repository.filter = AsyncMock(return_value=mock_paginated_result)

    # WHEN
    result = await mention_use_case.filter(
        pagination_params=pagination_params, filters=filters
    )

    # THEN
    assert isinstance(result, PaginatedResult)
    assert result.items == mock_mentions
    assert result.total_items == 1
    mock_mention_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )


async def test_filter_mentions_no_results(mention_use_case, mock_mention_repository):
    """
    GIVEN a mention use case and valid filters
    WHEN filter is called and the repository returns no matching mentions
    THEN it should return an empty paginated result
    """
    # GIVEN
    pagination_params = PaginationParams(page=1, per_page=10)
    filters = MentionFilters(name="Inexistant")
    mock_paginated_result = PaginatedResult(
        items=[],
        total_items=0,
        page=1,
        per_page=10,
        total_pages=0,
        next_page=None,
        previous_page=None,
    )
    mock_mention_repository.filter = AsyncMock(return_value=mock_paginated_result)

    # WHEN
    result = await mention_use_case.filter(
        pagination_params=pagination_params, filters=filters
    )

    # THEN
    assert isinstance(result, PaginatedResult)
    assert result.items == []
    assert result.total_items == 0
    mock_mention_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )


async def test_filter_mentions_empty_filters(mention_use_case, mock_mention_repository):
    """
    GIVEN a mention use case and empty filters
    WHEN filter is called
    THEN it should work correctly, likely returning all mentions
    """
    # GIVEN
    pagination_params = PaginationParams(page=1, per_page=10)
    filters = MentionFilters()
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
    mock_mention_repository.filter = AsyncMock(return_value=mock_paginated_result)

    # WHEN
    result = await mention_use_case.filter(
        pagination_params=pagination_params, filters=filters
    )

    # THEN
    assert isinstance(result, PaginatedResult)
    assert result.total_items == 2
    mock_mention_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )


async def test_filter_mentions_internal_error(
    mention_use_case, mock_mention_repository
):
    """
    GIVEN a mention use case
    WHEN filter is called and the repository raises a generic exception
    THEN it should re-raise an InternalServerErrorException
    """
    # GIVEN
    pagination_params = PaginationParams(page=1, per_page=10)
    filters = MentionFilters(name="Error")
    error_message = "A repository error occurred"
    mock_mention_repository.filter = AsyncMock(side_effect=Exception(error_message))

    # WHEN / THEN
    with pytest.raises(
        InternalServerErrorException, match="Server error. Please try again later."
    ):
        await mention_use_case.filter(
            pagination_params=pagination_params, filters=filters
        )

    mock_mention_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )


async def test_filter_mentions_pagination_links(
    mention_use_case, mock_mention_repository
):
    """
    GIVEN a mention use case
    WHEN filter is called and there are multiple pages of results
    THEN the paginated result should contain correct next and previous page links
    """
    # GIVEN
    pagination_params = PaginationParams(page=2, per_page=1)
    filters = MentionFilters()
    mock_mentions = [MentionEntity(id=2, name="Mention 2", domain_id=1)]
    mock_paginated_result = PaginatedResult(
        items=mock_mentions,
        total_items=3,
        page=2,
        per_page=1,
        total_pages=3,
        next_page=3,
        previous_page=1,
    )
    mock_mention_repository.filter = AsyncMock(return_value=mock_paginated_result)

    # WHEN
    result = await mention_use_case.filter(
        pagination_params=pagination_params, filters=filters
    )

    # THEN
    assert result.next_page == 3
    assert result.previous_page == 1
    mock_mention_repository.filter.assert_called_once_with(
        pagination_params=pagination_params, filters=filters
    )
