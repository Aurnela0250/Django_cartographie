from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from core.container.container import Container
from core.entities.filters import MentionFilters
from core.entities.mention import MentionEntity
from core.entities.pagination import PaginationParams
from core.entities.user import UserEntity
from core.use_cases.mention_use_case import MentionUseCase
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)
from presentation.schemas.mention import (
    MentionSchema,
    CreateMentionSchema,
    UpdateMentionSchema,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)

router = APIRouter(
    prefix="/mentions",
    tags=["Mentions"],
)


@router.post(
    "/",
    response_model=MentionSchema,
    status_code=201,
)
@inject
async def create(
    *,
    mention_data: CreateMentionSchema,
    mention_use_case: MentionUseCase = Depends(Provide[Container.mention_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        mention_entity = MentionEntity(**mention_data.model_dump(), created_by=user.id)
        mention = await mention_use_case.create(mention_entity)
        return MentionSchema.model_validate(mention)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/{mention_id}/",
    response_model=MentionSchema,
    status_code=200,
)
@inject
async def get(
    *,
    mention_id: int = Path(..., title="ID de la mention", gt=0),
    mention_use_case: MentionUseCase = Depends(Provide[Container.mention_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        mention = await mention_use_case.get(mention_id)
        return MentionSchema.model_validate(mention)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[MentionSchema],
    status_code=200,
)
@inject
async def get_all(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    mention_use_case: MentionUseCase = Depends(Provide[Container.mention_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await mention_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        MentionSchema,
        MentionSchema.model_validate,
    )


@router.put(
    "/{mention_id}/",
    response_model=MentionSchema,
    status_code=200,
)
@inject
async def update(
    *,
    mention_id: int = Path(..., title="ID de la mention", gt=0),
    mention_data: UpdateMentionSchema,
    mention_use_case: MentionUseCase = Depends(Provide[Container.mention_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        mention_entity = MentionEntity(
            **mention_data.model_dump(),
            updated_by=user.id,
        )
        updated_mention = await mention_use_case.update(
            mention_id,
            mention_entity,
        )
        return MentionSchema.model_validate(updated_mention)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{mention_id}/",
    response_model=None,
    status_code=204,
)
@inject
async def delete(
    *,
    mention_id: int = Path(..., title="ID de la mention", gt=0),
    mention_use_case: MentionUseCase = Depends(Provide[Container.mention_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await mention_use_case.delete(mention_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[MentionSchema],
    status_code=200,
)
@inject
async def filter(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    filters: Annotated[
        MentionFilters,
        Query(),
    ],
    mention_use_case: MentionUseCase = Depends(Provide[Container.mention_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await mention_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        MentionSchema,
        MentionSchema.model_validate,
    )
