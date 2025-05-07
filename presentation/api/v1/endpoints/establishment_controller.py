from ninja import Query
from ninja_extra import (
    api_controller,
    http_delete,
    http_get,
    http_post,
    http_put,
)

from core.domain.entities.establishment_entity import EstablishmentEntity
from core.domain.entities.pagination import PaginationParams
from core.use_cases.establishment_use_case import EstablishmentUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    ConflictError,
    DatabaseError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.establishment_schema import (
    CreateEstablishmentSchema,
    EstablishmentSchema,
    UpdateEstablishmentSchema,
)
from presentation.schemas.pagination_schema import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)


@api_controller("/establishments", tags=["Establishments"], auth=jwt_auth)
class EstablishmentController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.establishment_use_case = EstablishmentUseCase(self.unit_of_work)

    @http_post("/", response={201: EstablishmentSchema})
    def create_establishment(
        self,
        request,
        establishment_data: CreateEstablishmentSchema,
    ):
        """Create a new establishment"""
        try:
            entity_data = EstablishmentEntity(
                **establishment_data.model_dump(),
                created_by=request.auth.get("user_id")
            )

            establishment = self.establishment_use_case.create_establishment(
                entity_data
            )
            return 201, EstablishmentSchema.from_orm(establishment)
        except ConflictError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get("/{establishment_id}", response=EstablishmentSchema)
    def get_establishment(self, establishment_id: int):
        """Get an establishment by ID"""
        try:
            establishment = self.establishment_use_case.get_establishment(
                establishment_id
            )
            return EstablishmentSchema.from_orm(establishment)
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_put("/{establishment_id}", response=EstablishmentSchema)
    def update_establishment(
        self,
        request,
        establishment_id: int,
        establishment_data: UpdateEstablishmentSchema,
    ):
        """Update an existing establishment"""
        try:
            # Get the existing establishment first
            current_establishment = self.establishment_use_case.get_establishment(
                establishment_id
            )

            # Update with new data, keeping existing values for fields not in the update
            update_data = current_establishment.model_dump()
            update_data.update(establishment_data.model_dump(exclude_unset=True))
            update_data["updated_by"] = request.auth.get("user_id")

            entity_to_update = EstablishmentEntity(**update_data)

            updated_establishment = self.establishment_use_case.update_establishment(
                establishment_id, entity_to_update
            )
            return EstablishmentSchema.from_orm(updated_establishment)
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

    @http_delete("/{establishment_id}", response={204: None})
    def delete_establishment(self, establishment_id: int):
        """Delete an establishment"""
        try:
            self.establishment_use_case.delete_establishment(establishment_id)
            return 204, None
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "/",
        response=PaginatedResultSchema[EstablishmentSchema],
    )
    def get_all_establishments(
        self,
        request,
        pagination: Query[PaginationParamsSchema],
    ):
        """Get all establishments"""
        try:
            pagination_params = PaginationParams(
                page=pagination.page, per_page=pagination.per_page
            )

            establishments = self.establishment_use_case.get_all_establishments(
                pagination_params
            )

            return 200, PaginatedResultSchema.from_domain_result(
                establishments, EstablishmentSchema, EstablishmentSchema.model_validate
            )

        except Exception:
            raise InternalServerError()
