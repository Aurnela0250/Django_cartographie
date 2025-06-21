from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from core.container.container import Container
from core.entities.establishment_type import EstablishmentTypeEntity
from core.entities.filters import EstablishmentTypeFilters
from core.entities.pagination import PaginationParams
from core.entities.user import UserEntity
from core.use_cases.establishment_type_use_case import EstablishmentTypeUseCase
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)
from presentation.schemas.establishment_type import (
    EstablishmentTypeSchema,
    CreateEstablishmentTypeSchema,
    UpdateEstablishmentTypeSchema,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)

router = APIRouter(
    prefix="/establishment-types",
    tags=["Establishment Types"],
)


@router.post(
    "/",
    response_model=EstablishmentTypeSchema,
    status_code=201,
)
@inject
async def create(
    *,
    establishment_type_data: CreateEstablishmentTypeSchema,
    establishment_type_use_case: EstablishmentTypeUseCase = Depends(
        Provide[Container.establishment_type_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = EstablishmentTypeEntity(
            **establishment_type_data.model_dump(),
            created_by=user.id,
        )
        created = await establishment_type_use_case.create(entity)
        return EstablishmentTypeSchema.model_validate(created)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/{establishment_type_id}/",
    response_model=EstablishmentTypeSchema,
    status_code=200,
)
@inject
async def get(
    *,
    establishment_type_id: int = Path(
        ...,
        title="ID du type d'établissement",
        gt=0,
    ),
    establishment_type_use_case: EstablishmentTypeUseCase = Depends(
        Provide[Container.establishment_type_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        establishment_type = await establishment_type_use_case.get(
            establishment_type_id
        )
        return EstablishmentTypeSchema.model_validate(establishment_type)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[EstablishmentTypeSchema],
    status_code=200,
)
@inject
async def get_all(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    establishment_type_use_case: EstablishmentTypeUseCase = Depends(
        Provide[Container.establishment_type_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page,
        per_page=pagination.per_page,
    )
    result = await establishment_type_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        EstablishmentTypeSchema,
        EstablishmentTypeSchema.model_validate,
    )


@router.put(
    "/{establishment_type_id}/",
    response_model=EstablishmentTypeSchema,
    status_code=200,
)
@inject
async def update(
    *,
    establishment_type_id: int = Path(
        ...,
        title="ID du type d'établissement",
        gt=0,
    ),
    establishment_type_data: UpdateEstablishmentTypeSchema,
    establishment_type_use_case: EstablishmentTypeUseCase = Depends(
        Provide[Container.establishment_type_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        entity = EstablishmentTypeEntity(
            **establishment_type_data.model_dump(),
            updated_by=user.id,
        )
        updated = await establishment_type_use_case.update(
            establishment_type_id,
            entity,
        )
        return EstablishmentTypeSchema.model_validate(updated)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{establishment_type_id}/",
    response_model=None,
    status_code=204,
)
@inject
async def delete(
    *,
    establishment_type_id: int = Path(
        ...,
        title="ID du type d'établissement",
        gt=0,
    ),
    establishment_type_use_case: EstablishmentTypeUseCase = Depends(
        Provide[Container.establishment_type_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await establishment_type_use_case.delete(establishment_type_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[EstablishmentTypeSchema],
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
        EstablishmentTypeFilters,
        Query(),
    ],
    establishment_type_use_case: EstablishmentTypeUseCase = Depends(
        Provide[Container.establishment_type_use_case]
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page,
        per_page=pagination.per_page,
    )
    result = await establishment_type_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        EstablishmentTypeSchema,
        EstablishmentTypeSchema.model_validate,
    )
