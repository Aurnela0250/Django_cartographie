import logging

from ninja import Query
from ninja_extra import (
    api_controller,
    http_delete,
    http_get,
    http_post,
    http_put,
)

from core.domain.entities.formation_authorization_entity import (
    FormationAuthorizationEntity,
)
from core.domain.entities.formation_entity import FormationEntity
from core.domain.entities.pagination import PaginationParams
from core.use_cases.formation_use_case import FormationUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    ConflictError,
    DatabaseError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.formation_authorization_schema import (
    CreateFormationAuthorizationSchema,
    UpdateFormationAuthorizationSchema,
)
from presentation.schemas.formation_schema import (
    CreateFormationSchema,
    FormationSchema,
    UpdateFormationSchema,
)
from presentation.schemas.pagination_schema import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)


@api_controller("/formations", tags=["Formations"], auth=jwt_auth)
class FormationController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.formation_use_case = FormationUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_post("/", response={201: FormationSchema})
    def create_formation(
        self,
        request,
        formation_data: CreateFormationSchema,
    ):
        """Create a new formation"""
        try:
            entity_data = FormationEntity(
                **formation_data.model_dump(),
                created_by=request.auth.get("user_id"),
            )

            formation = self.formation_use_case.create_formation(entity_data)
            return 201, FormationSchema.from_orm(formation)
        except ConflictError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get("/{formation_id}", response=FormationSchema)
    def get_formation(self, formation_id: int):
        """Get a formation by ID"""
        try:
            formation = self.formation_use_case.get_formation(formation_id)
            return FormationSchema.from_orm(formation)
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_put("/{formation_id}", response=FormationSchema)
    def update_formation(
        self,
        request,
        formation_id: int,
        formation_data: UpdateFormationSchema,
    ):
        """Update an existing formation"""
        try:
            # Get the existing formation first
            current_formation = self.formation_use_case.get_formation(formation_id)

            # Update with new data, keeping existing values for fields not in the update
            update_data = current_formation.model_dump()
            update_data.update(formation_data.model_dump(exclude_unset=True))
            update_data["updated_by"] = request.auth.get("user_id")

            entity_to_update = FormationEntity(**update_data)

            updated_formation = self.formation_use_case.update_formation(
                formation_id, entity_to_update
            )
            return FormationSchema.from_orm(updated_formation)
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

    @http_delete("/{formation_id}", response={204: None})
    def delete_formation(self, formation_id: int):
        """Delete a formation"""
        try:
            self.formation_use_case.delete_formation(formation_id)
            return 204, None
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "/",
        response=PaginatedResultSchema[FormationSchema],
    )
    def get_all_formations(
        self,
        request,
        pagination: Query[PaginationParamsSchema],
    ):
        """Get all formations"""
        try:
            pagination_params = PaginationParams(
                page=pagination.page, per_page=pagination.per_page
            )

            formations = self.formation_use_case.get_all_formations(pagination_params)

            return 200, PaginatedResultSchema.from_domain_result(
                formations,
                FormationSchema,
                FormationSchema.model_validate,
            )

        except ValidationError as e:
            self.logger.warning(f"Validation error occurred: {e}")
            raise e
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            raise InternalServerError()

    @http_post("/{formation_id}/authorization", response=FormationSchema)
    def create_authorization(
        self,
        request,
        formation_id: int,
        authorization_data: CreateFormationAuthorizationSchema,
    ):
        """Create an authorization for a formation"""
        try:
            entity_data = FormationAuthorizationEntity(
                **authorization_data.model_dump(),
                created_by=request.auth.get("user_id"),
            )

            formation = self.formation_use_case.create_authorization(
                formation_id, entity_data
            )
            return FormationSchema.from_orm(formation)
        except NotFoundError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_put("/{formation_id}/authorization", response=FormationSchema)
    def update_authorization(
        self,
        request,
        formation_id: int,
        authorization_data: UpdateFormationAuthorizationSchema,
    ):
        """Update the authorization of a formation"""
        try:
            # Get the existing formation first
            current_formation = self.formation_use_case.get_formation(formation_id)

            if not current_formation.authorization:
                raise NotFoundError()

            # Update with new data, keeping existing values for fields not in the update
            auth_update_data = current_formation.authorization.model_dump()
            auth_update_data.update(authorization_data.model_dump(exclude_unset=True))
            auth_update_data["updated_by"] = request.auth.get("user_id")

            entity_to_update = FormationAuthorizationEntity(**auth_update_data)

            updated_formation = self.formation_use_case.update_authorization(
                formation_id, entity_to_update
            )
            return FormationSchema.from_orm(updated_formation)
        except NotFoundError as e:
            raise e
        except ValidationError as e:
            raise e
        except DatabaseError as e:
            raise e
        except Exception:
            raise InternalServerError()
