from typing import List

from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from core.domain.entities.establishment_type_entity import EstablishmentTypeEntity
from core.use_cases.establishment_type_use_case import EstablishmentTypeUseCase
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


@api_controller("/establishment-types", tags=["Establishment Types"], auth=jwt_auth)
class EstablishmentTypeController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.establishment_type_use_case = EstablishmentTypeUseCase(self.unit_of_work)

    @http_post("/", response={201: EstablishmentTypeSchema})
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

    @http_get("/{establishment_type_id}", response=EstablishmentTypeSchema)
    def get_establishment_type(self, establishment_type_id: int):
        """Get an establishment type by ID"""
        try:
            establishment_type = (
                self.establishment_type_use_case.get_establishment_type(
                    establishment_type_id
                )
            )
            return EstablishmentTypeSchema.from_orm(establishment_type)
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_put("/{establishment_type_id}", response=EstablishmentTypeSchema)
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

    @http_delete("/{establishment_type_id}", response={204: None})
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

    @http_get("/", response=List[EstablishmentTypeSchema])
    def get_all_establishment_types(self):
        """Get all establishment types"""
        try:
            establishment_types = (
                self.establishment_type_use_case.get_all_establishment_types()
            )
            return [EstablishmentTypeSchema.from_orm(et) for et in establishment_types]
        except Exception:
            raise InternalServerError()
