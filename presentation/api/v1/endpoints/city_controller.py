from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from core.domain.entities.pagination import PaginationParams
from core.use_cases.city_use_case import CityUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    BadRequestError,
    ConflictError,
    DatabaseError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.city_schema import (
    CitySchema,
    CreateCitySchemaRequest,
    CreateCitySchemaResponse,
    UpdateCitySchema,
)
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.pagination_schema import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)


@api_controller("/cities", tags=["Cities"], auth=jwt_auth)
class CityController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.city_use_case = CityUseCase(self.unit_of_work)

    @http_post(
        "/",
        response={
            201: CreateCitySchemaResponse,
            400: ErrorResponseSchema,
            401: ErrorResponseSchema,
            409: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def create_city(self, request, city_data: CreateCitySchemaRequest):
        try:
            city = self.city_use_case.create(
                city_data,
                created_by=request.user.id,
            )
            return 201, CreateCitySchemaResponse.from_orm(city)
        except ConflictError:
            raise ConflictError()
        except ValidationError:
            raise BadRequestError()
        except DatabaseError:
            raise DatabaseError()
        except Exception:
            raise InternalServerError()

    @http_get(
        "/{city_id}",
        response={
            200: CitySchema,
            401: ErrorResponseSchema,
            404: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def get_city(self, request, city_id: int):
        try:
            city = self.city_use_case.get(city_id)
            return CitySchema.from_orm(city)
        except NotFoundError:
            raise NotFoundError()
        except Exception:
            raise InternalServerError()

    @http_get(
        "/",
        response={
            200: PaginatedResultSchema[CitySchema],
            401: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def get_all_cities(self, request, pagination: Query[PaginationParamsSchema]):
        try:
            pagination_params = PaginationParams(
                page=pagination.page, per_page=pagination.per_page
            )
            result = self.city_use_case.get_all(pagination_params)
            return 200, PaginatedResultSchema.from_domain_result(
                result,
                CitySchema,
                CitySchema.from_orm,
            )
        except Exception:
            raise InternalServerError()

    @http_put(
        "/{city_id}",
        response={
            200: CitySchema,
            400: ErrorResponseSchema,
            401: ErrorResponseSchema,
            404: ErrorResponseSchema,
            409: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def update_city(self, request, city_id: int, city_data: UpdateCitySchema):
        try:
            updated_city = self.city_use_case.update(
                city_id,
                city_data,
                updated_by=request.user.id,
            )
            return CitySchema.from_orm(updated_city)
        except ValidationError:
            raise BadRequestError()
        except NotFoundError:
            raise NotFoundError()
        except ConflictError:
            raise ConflictError()
        except DatabaseError:
            raise DatabaseError()
        except Exception:
            raise InternalServerError()

    @http_delete(
        "/{city_id}",
        response={
            204: None,
            401: ErrorResponseSchema,
            404: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def delete_city(self, request, city_id: int):
        try:
            self.city_use_case.delete(city_id)
            return 204, None
        except NotFoundError:
            raise NotFoundError()
        except Exception:
            raise InternalServerError()
