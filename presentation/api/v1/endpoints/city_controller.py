from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from core.container.container import Container
from core.entities.city import CityEntity
from core.entities.filters import CityFilters
from core.entities.pagination import PaginationParams
from core.entities.user import UserEntity
from core.use_cases.city_use_case import CityUseCase
from presentation.constants.response_example import (
    create_city_responses,
    delete_city_responses,
    filter_cities_responses,
    get_all_cities_responses,
    get_city_responses,
    update_city_responses,
)
from presentation.dependencies.auth_dependencies import get_current_user
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    NotFoundException,
    UnauthorizedException,
)
from presentation.schemas.city import (
    CitySchema,
    CreateCitySchema,
    UpdateCitySchema,
)
from presentation.schemas.pagination import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post(
    "/",
    response_model=CitySchema,
    status_code=201,
    responses=create_city_responses,
)
@inject
async def create(
    *,
    city_data: CreateCitySchema,
    city_use_case: CityUseCase = Depends(Provide[Container.city_use_case]),
    user: UserEntity = Depends(get_current_user),
):

    try:
        city_entity = CityEntity(**city_data.model_dump(), created_by=user.id)
        city = await city_use_case.create(city_entity)
        print(city)
        return CitySchema.model_validate(city)
    except ConflictException as e:
        raise e
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/filter/",
    response_model=PaginatedResultSchema[CitySchema],
    status_code=200,
    responses=filter_cities_responses,
)
@inject
async def filter(
    *,
    pagination: PaginationParamsSchema = Depends(),
    filters: CityFilters = Depends(),
    city_use_case: CityUseCase = Depends(
        Provide[Container.city_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await city_use_case.filter(pagination_params, filters)
    return PaginatedResultSchema.from_domain_result(
        result,
        CitySchema,
        CitySchema.model_validate,
    )


@router.get(
    "/{city_id}/",
    response_model=CitySchema,
    status_code=200,
    responses=get_city_responses,
)
# @cache_response(
#     cache_type="item",
#     cache_service=lambda  *a, **kw: self.cache_service,
#     schema_type=CitySchema,
#     get_id=lambda  request, city_id, **kwargs: city_id,
# )
@inject
async def get(
    *,
    city_id: int = Path(..., title="ID de la ville", gt=0),
    city_use_case: CityUseCase = Depends(Provide[Container.city_use_case]),
    user: UserEntity = Depends(get_current_user),
):
    try:
        city = await city_use_case.get(city_id)
        return CitySchema.model_validate(city)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.get(
    "/",
    response_model=PaginatedResultSchema[CitySchema],
    status_code=200,
    responses=get_all_cities_responses,
)
@inject
async def get_all(
    *,
    pagination: PaginationParamsSchema = Depends(),
    city_use_case: CityUseCase = Depends(
        Provide[Container.city_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):
    pagination_params = PaginationParams(
        page=pagination.page, per_page=pagination.per_page
    )
    result = await city_use_case.get_all(pagination_params)
    return PaginatedResultSchema.from_domain_result(
        result,
        CitySchema,
        CitySchema.model_validate,
    )


@router.put(
    "/{city_id}/",
    response_model=CitySchema,
    status_code=200,
    responses=update_city_responses,
)
@inject
async def update(
    *,
    city_id: int = Path(
        ...,
        title="ID de la ville",
        gt=0,
    ),
    city_data: UpdateCitySchema,
    city_use_case: CityUseCase = Depends(
        Provide[Container.city_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):

    try:
        if user.id is None:
            raise UnauthorizedException(
                message="Could not validate credentials for update action"
            )

        update_payload = city_data.model_dump(exclude_unset=True)
        updated_city = await city_use_case.update(city_id, update_payload, user.id)
        return CitySchema.model_validate(updated_city)
    except ConflictException as e:
        raise ConflictException(cause=e)
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)


@router.delete(
    "/{city_id}/",
    response_model=None,
    status_code=204,
    responses=delete_city_responses,
)
@inject
async def deletew(
    *,
    city_id: int = Path(..., title="ID de la ville", gt=0),
    city_use_case: CityUseCase = Depends(
        Provide[Container.city_use_case],
    ),
    user: UserEntity = Depends(get_current_user),
):
    try:
        await city_use_case.delete(city_id)
        return None
    except NotFoundException as e:
        raise NotFoundException(cause=e)
    except Exception as e:
        raise InternalServerErrorException(cause=e)
