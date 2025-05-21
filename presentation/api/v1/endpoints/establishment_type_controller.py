from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from core.domain.entities.establishment_type_entity import EstablishmentTypeEntity
from core.domain.entities.pagination import PaginationParams
from core.use_cases.establishment_type_use_case import EstablishmentTypeUseCase
from infrastructure.cache.cache_service import CacheService
from infrastructure.cache.cache_utils import cache_response
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    ConflictError,
    DatabaseError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.establishment_type_schema import (
    CreateEstablishmentTypeSchema,
    EstablishmentTypeSchema,
    UpdateEstablishmentTypeSchema,
)
from presentation.schemas.pagination_schema import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)


@api_controller("/establishment-types", tags=["Establishment Types"], auth=jwt_auth)
class EstablishmentTypeController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.establishment_type_use_case = EstablishmentTypeUseCase(self.unit_of_work)
        from infrastructure.external_services.redis_service import RedisService

        self.redis_service = RedisService()
        self.cache_service = CacheService(
            redis_service=self.redis_service,
            entity_name="establishment_type",
        )

    @http_post(
        "",
        response={201: EstablishmentTypeSchema},
    )
    def create_establishment_type(
        self,
        request,
        establishment_type_data: CreateEstablishmentTypeSchema,
    ):
        """Create a new establishment type"""
        try:
            entity_data = EstablishmentTypeEntity(
                **establishment_type_data.model_dump(),
                created_by=request.auth.get("user_id")
            )

            establishment_type = (
                self.establishment_type_use_case.create_establishment_type(entity_data)
            )
            return 201, EstablishmentTypeSchema.from_orm(establishment_type)
        except ConflictError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "/{establishment_type_id}",
        response=EstablishmentTypeSchema,
    )
    @cache_response(
        cache_type="item",
        cache_service=lambda self, *a, **kw: self.cache_service,
        schema_type=EstablishmentTypeSchema,
        get_id=lambda self, establishment_type_id, **kwargs: establishment_type_id,
    )
    def get_establishment_type(self, establishment_type_id: int):
        establishment_type = self.establishment_type_use_case.get_establishment_type(
            establishment_type_id
        )
        return EstablishmentTypeSchema.from_orm(establishment_type)

    @http_put(
        "/{establishment_type_id}",
        response=EstablishmentTypeSchema,
    )
    def update_establishment_type(
        self,
        request,
        establishment_type_id: int,
        establishment_type_data: UpdateEstablishmentTypeSchema,
    ):
        """Update an existing establishment type"""
        try:
            # Get the existing establishment type first
            current_establishment_type = (
                self.establishment_type_use_case.get_establishment_type(
                    establishment_type_id
                )
            )

            # Update with new data, keeping existing values for fields not in the update
            update_data = current_establishment_type.model_dump()
            update_data.update(establishment_type_data.model_dump(exclude_unset=True))
            update_data["updated_by"] = request.auth.get("user_id")

            entity_to_update = EstablishmentTypeEntity(**update_data)

            updated_establishment_type = (
                self.establishment_type_use_case.update_establishment_type(
                    establishment_type_id, entity_to_update
                )
            )
            return EstablishmentTypeSchema.from_orm(updated_establishment_type)
        except NotFoundError as e:
            raise e
        except ConflictError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_delete(
        "/{establishment_type_id}",
        response={204: None},
    )
    def delete_establishment_type(self, establishment_type_id: int):
        """Delete an establishment type"""
        try:
            self.establishment_type_use_case.delete_establishment_type(
                establishment_type_id
            )
            return 204, None
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "",
        response=PaginatedResultSchema[EstablishmentTypeSchema],
    )
    @cache_response(
        cache_type="list",
        cache_service=lambda self, *a, **kw: self.cache_service,
        schema_type=PaginatedResultSchema[EstablishmentTypeSchema],
        get_pagination=lambda self, request, pagination, **kwargs: PaginationParams(
            page=pagination.page, per_page=pagination.per_page
        ),
    )
    def get_all_establishment_types(
        self,
        request,
        pagination: Query[PaginationParamsSchema],
    ):
        pagination_params = PaginationParams(
            page=pagination.page, per_page=pagination.per_page
        )
        establishment_types = (
            self.establishment_type_use_case.get_all_establishment_types(
                pagination_params
            )
        )
        return PaginatedResultSchema.from_domain_result(
            establishment_types,
            EstablishmentTypeSchema,
            EstablishmentTypeSchema.model_validate,
        )
