# Nouvelle implémentation fonctionnelle FastAPI
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from core.container.container import Container
from core.entities.filters import RegionFilters
from core.entities.pagination import PaginationParams
from core.entities.region import RegionEntity
from core.entities.user import UserEntity
from core.use_cases.region_use_case import RegionUseCase
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)
from presentation.schemas.region import (
    CreateRegionSchema,
    RegionSchema,
    UpdateRegionSchema,
)

router = APIRouter(
    prefix="/regions",
    tags=["Regions"],
)


@router.post(
    "/",
    response_model=RegionSchema,
    status_code=201,
)
@inject
async def create(
    *,
    region_data: CreateRegionSchema,
    region_use_case: RegionUseCase = Depends(
        Provide[Container.region_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        region_entity = RegionEntity(
            **region_data.model_dump(),
            created_by=user.id,
        )
        region = await region_use_case.create(region_entity)
        return RegionSchema.model_validate(region)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/{region_id}/",
    response_model=RegionSchema,
    status_code=200,
)
@inject
async def get(
    *,
    region_id: int = Path(..., title="ID de la région", gt=0),
    region_use_case: RegionUseCase = Depends(
        Provide[Container.region_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        region = await region_use_case.get(region_id)
        return RegionSchema.model_validate(region)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[RegionSchema],
    status_code=200,
)
@inject
async def get_all(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    region_use_case: RegionUseCase = Depends(
        Provide[Container.region_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page,
        per_page=pagination.per_page,
    )
    result = await region_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        RegionSchema,
        RegionSchema.model_validate,
    )


@router.put(
    "/{region_id}/",
    response_model=RegionSchema,
    status_code=200,
)
@inject
async def update(
    *,
    region_id: int = Path(..., title="ID de la région", gt=0),
    region_data: UpdateRegionSchema,
    region_use_case: RegionUseCase = Depends(Provide[Container.region_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        region_entity = RegionEntity(
            **region_data.model_dump(),
            updated_by=user.id,
        )
        updated_region = await region_use_case.update(
            region_id,
            region_entity,
        )
        return RegionSchema.model_validate(updated_region)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{region_id}/",
    response_model=None,
    status_code=204,
)
@inject
async def delete(
    *,
    region_id: int = Path(..., title="ID de la région", gt=0),
    region_use_case: RegionUseCase = Depends(Provide[Container.region_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await region_use_case.delete(region_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[RegionSchema],
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
        RegionFilters,
        Query(),
    ],
    region_use_case: RegionUseCase = Depends(
        Provide[Container.region_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page,
        per_page=pagination.per_page,
    )
    result = await region_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        RegionSchema,
        RegionSchema.model_validate,
    )
