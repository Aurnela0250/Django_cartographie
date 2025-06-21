from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from core.container.container import Container
from core.entities.filters import LevelFilters
from core.entities.level import LevelEntity
from core.entities.pagination import PaginationParams
from core.entities.user import UserEntity
from core.use_cases.level_use_case import LevelUseCase
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)
from presentation.schemas.level import (
    CreateLevelSchema,
    LevelSchema,
    UpdateLevelSchema,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)

router = APIRouter(
    prefix="/levels",
    tags=["Levels"],
)


@router.post(
    "/",
    response_model=LevelSchema,
    status_code=201,
)
@inject
async def create(
    *,
    level_data: CreateLevelSchema,
    level_use_case: LevelUseCase = Depends(Provide[Container.level_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = LevelEntity(**level_data.model_dump(), created_by=user.id)
        created = await level_use_case.create(entity)
        return LevelSchema.model_validate(created)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/{level_id}/",
    response_model=LevelSchema,
    status_code=200,
)
@inject
async def get(
    *,
    level_id: int = Path(..., title="ID du niveau", gt=0),
    level_use_case: LevelUseCase = Depends(Provide[Container.level_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        level = await level_use_case.get(level_id)
        return LevelSchema.model_validate(level)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[LevelSchema],
    status_code=200,
)
@inject
async def get_all(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    level_use_case: LevelUseCase = Depends(Provide[Container.level_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await level_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        LevelSchema,
        LevelSchema.model_validate,
    )


@router.put(
    "/{level_id}/",
    response_model=LevelSchema,
    status_code=200,
)
@inject
async def update(
    *,
    level_id: int = Path(..., title="ID du niveau", gt=0),
    level_data: UpdateLevelSchema,
    level_use_case: LevelUseCase = Depends(Provide[Container.level_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = LevelEntity(
            **level_data.model_dump(),
            updated_by=user.id,
        )
        updated = await level_use_case.update(level_id, entity)
        return LevelSchema.model_validate(updated)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{level_id}/",
    response_model=None,
    status_code=204,
)
@inject
async def delete(
    *,
    level_id: int = Path(..., title="ID du niveau", gt=0),
    level_use_case: LevelUseCase = Depends(Provide[Container.level_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await level_use_case.delete(level_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[LevelSchema],
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
        LevelFilters,
        Query(),
    ],
    level_use_case: LevelUseCase = Depends(Provide[Container.level_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page,
        per_page=pagination.per_page,
    )
    result = await level_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        LevelSchema,
        LevelSchema.model_validate,
    )
