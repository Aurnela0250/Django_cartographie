from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from core.container.container import Container
from core.entities.establishment import EstablishmentEntity
from core.entities.filters import EstablishmentFilters
from core.entities.pagination import PaginationParams
from core.entities.user import UserEntity
from core.use_cases.establishment_use_case import EstablishmentUseCase
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)
from presentation.schemas.establishment import (
    EstablishmentSchema,
    CreateEstablishmentSchema,
    UpdateEstablishmentSchema,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)

router = APIRouter(
    prefix="/establishments",
    tags=["Establishments"],
)


@router.post(
    "/",
    response_model=EstablishmentSchema,
    status_code=201,
)
@inject
async def create(
    *,
    establishment_data: CreateEstablishmentSchema,
    establishment_use_case: EstablishmentUseCase = Depends(
        Provide[Container.establishment_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = EstablishmentEntity(
            **establishment_data.model_dump(), created_by=user.id
        )
        created = await establishment_use_case.create(entity)
        return EstablishmentSchema.model_validate(created)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/{establishment_id}/",
    response_model=EstablishmentSchema,
    status_code=200,
)
@inject
async def get(
    *,
    establishment_id: int = Path(..., title="ID de l'établissement", gt=0),
    establishment_use_case: EstablishmentUseCase = Depends(
        Provide[Container.establishment_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        establishment = await establishment_use_case.get(establishment_id)
        return EstablishmentSchema.model_validate(establishment)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[EstablishmentSchema],
    status_code=200,
)
@inject
async def get_all(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    establishment_use_case: EstablishmentUseCase = Depends(
        Provide[Container.establishment_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await establishment_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        EstablishmentSchema,
        EstablishmentSchema.model_validate,
    )


@router.put(
    "/{establishment_id}/",
    response_model=EstablishmentSchema,
    status_code=200,
)
@inject
async def update(
    *,
    establishment_id: int = Path(..., title="ID de l'établissement", gt=0),
    establishment_data: UpdateEstablishmentSchema,
    establishment_use_case: EstablishmentUseCase = Depends(
        Provide[Container.establishment_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = EstablishmentEntity(
            **establishment_data.model_dump(),
            updated_by=user.id,
        )
        updated = await establishment_use_case.update(establishment_id, entity)
        return EstablishmentSchema.model_validate(updated)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{establishment_id}/",
    response_model=None,
    status_code=204,
)
@inject
async def delete(
    *,
    establishment_id: int = Path(..., title="ID de l'établissement", gt=0),
    establishment_use_case: EstablishmentUseCase = Depends(
        Provide[Container.establishment_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await establishment_use_case.delete(establishment_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[EstablishmentSchema],
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
        EstablishmentFilters,
        Query(),
    ],
    establishment_use_case: EstablishmentUseCase = Depends(
        Provide[Container.establishment_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await establishment_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        EstablishmentSchema,
        EstablishmentSchema.model_validate,
    )
