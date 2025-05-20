import logging

from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from pydantic import ValidationError as PydanticValidationError

from core.domain.entities.level_entity import LevelEntity
from core.domain.entities.pagination import PaginationParams
from core.use_cases.level_use_case import LevelUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.level_schema import LevelCreate, LevelOut, LevelUpdate
from presentation.schemas.pagination_schema import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)


@api_controller("/levels", tags=["Levels"])
class LevelController:
    """Controller for managing levels"""

    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.level_use_case = LevelUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_get(
        "",
        response={
            200: PaginatedResultSchema[LevelOut],
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Retrieve all levels",
        description="Returns a list of all available levels with pagination",
    )
    def get_all_levels(
        self,
        request,
        pagination: Query[PaginationParamsSchema],
    ):
        """Retrieves all levels with pagination (page=1 and per_page=10 by default)"""
        try:
            pagination_params = PaginationParams(
                page=pagination.page, per_page=pagination.per_page
            )

            result = self.level_use_case.get_all_levels(pagination_params)

            # Convertir le PaginatedResult en PaginatedResultSchema
            return 200, PaginatedResultSchema.from_domain_result(
                result, LevelOut, LevelOut.model_validate
            )

        except Exception as e:
            self.logger.error(f"Error retrieving all levels: {str(e)}")
            raise InternalServerError()

    @http_get(
        "/{level_id}",
        response={200: LevelOut, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Retrieve a level by its ID",
        description="Returns the details of a level specified by its ID",
    )
    def get_level(self, request, level_id: int):
        """Retrieves a level by its ID"""
        try:
            level = self.level_use_case.get_level(level_id)
            return 200, LevelOut.model_validate(level)
        except NotFoundError:
            self.logger.warning(f"Level with ID {level_id} not found")
            raise
        except Exception as e:
            self.logger.error(f"Error retrieving level {level_id}: {str(e)}")
            raise InternalServerError()

    @http_post(
        "",
        response={
            201: LevelOut,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Create a new level",
        description="Creates a new level with the provided data",
    )
    def create_level(self, request, level_data: LevelCreate):
        """Creates a new level"""
        try:
            level_entity = LevelEntity(
                **level_data.model_dump(),
                created_by=request.user.id,
            )
            created_level = self.level_use_case.create_level(level_entity)
            return 201, LevelOut.model_validate(created_level)
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during level creation: {str(e)}")
            raise ValidationError(e)
        except ConflictError:
            self.logger.warning("Conflict error during level creation")
            raise
        except Exception as e:
            self.logger.error(f"Error creating level: {str(e)}")
            raise InternalServerError()

    @http_put(
        "/{level_id}",
        response={
            200: LevelOut,
            404: ErrorResponseSchema,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Update a level",
        description="Updates the data of an existing level",
    )
    def update_level(self, request, level_id: int, level_data: LevelUpdate):
        """Updates an existing level"""
        try:
            # First, retrieve the existing level
            existing_level = self.level_use_case.get_level(level_id)

            # Update only the provided fields
            update_data = LevelEntity(
                id=existing_level.id,
                name=(
                    level_data.name
                    if level_data.name is not None
                    else existing_level.name
                ),
                acronyme=(
                    level_data.acronyme
                    if level_data.acronyme is not None
                    else existing_level.acronyme
                ),
                created_at=existing_level.created_at,
                created_by=existing_level.created_by,
                updated_by=request.user.id,
            )

            updated_level = self.level_use_case.update_level(level_id, update_data)
            return 200, LevelOut.model_validate(updated_level)
        except NotFoundError:
            self.logger.warning(f"Level with ID {level_id} not found for update")
            raise
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during level update: {str(e)}")
            raise ValidationError(e)
        except ConflictError:
            self.logger.warning("Conflict error during level update")
            raise
        except Exception as e:
            self.logger.error(f"Error updating level {level_id}: {str(e)}")
            raise InternalServerError()

    @http_delete(
        "/{level_id}",
        response={204: None, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Delete a level",
        description="Deletes an existing level by its ID",
    )
    def delete_level(self, request, level_id: int):
        """Deletes a level"""
        try:
            self.level_use_case.delete_level(level_id)
            return 204, None
        except NotFoundError:
            self.logger.warning(f"Level with ID {level_id} not found for deletion")
            raise
        except Exception as e:
            self.logger.error(f"Error deleting level {level_id}: {str(e)}")
            raise InternalServerError()
