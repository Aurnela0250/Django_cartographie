from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from core.container.container import Container
from core.entities.domain import DomainEntity
from core.entities.filters import DomainFilters
from core.entities.pagination import PaginationParams
from core.entities.user import UserEntity
from core.use_cases.domain_use_case import DomainUseCase
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
)
from presentation.schemas.domain import (
    CreateDomainSchema,
    DomainSchema,
    UpdateDomainSchema,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)

router = APIRouter(
    prefix="/domains",
    tags=["Domains"],
)


@router.post(
    "/",
    response_model=DomainSchema,
    status_code=201,
)
@inject
async def create(
    *,
    domain_data: CreateDomainSchema,
    domain_use_case: DomainUseCase = Depends(Provide[Container.domain_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        domain_entity = DomainEntity(**domain_data.model_dump(), created_by=user.id)
        created_domain = await domain_use_case.create(domain_entity)
        return DomainSchema.model_validate(created_domain)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/{domain_id}/",
    response_model=DomainSchema,
    status_code=200,
)
@inject
async def get(
    *,
    domain_id: int = Path(..., title="ID du domaine", gt=0),
    domain_use_case: DomainUseCase = Depends(Provide[Container.domain_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        domain = await domain_use_case.get(domain_id)
        return DomainSchema.model_validate(domain)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[DomainSchema],
    status_code=200,
)
@inject
async def get_all(
    *,
    pagination: Annotated[
        PaginationParamsSchema,
        Query(),
    ],
    domain_use_case: DomainUseCase = Depends(Provide[Container.domain_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await domain_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        DomainSchema,
        DomainSchema.model_validate,
    )


@router.put(
    "/{domain_id}/",
    response_model=DomainSchema,
    status_code=200,
)
@inject
async def update(
    *,
    domain_id: int = Path(..., title="ID du domaine", gt=0),
    domain_data: UpdateDomainSchema,
    domain_use_case: DomainUseCase = Depends(Provide[Container.domain_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        domain_entity = DomainEntity(
            **domain_data.model_dump(),
            updated_by=user.id,
        )
        updated_domain = await domain_use_case.update(domain_id, domain_entity)
        return DomainSchema.model_validate(updated_domain)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{domain_id}/",
    response_model=None,
    status_code=204,
)
@inject
async def delete(
    *,
    domain_id: int = Path(..., title="ID du domaine", gt=0),
    domain_use_case: DomainUseCase = Depends(Provide[Container.domain_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await domain_use_case.delete(domain_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[DomainSchema],
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
        DomainFilters,
        Query(),
    ],
    domain_use_case: DomainUseCase = Depends(Provide[Container.domain_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await domain_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        DomainSchema,
        DomainSchema.model_validate,
    )
