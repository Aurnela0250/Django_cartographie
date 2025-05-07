import logging

from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from pydantic import ValidationError as PydanticValidationError

from core.domain.entities.pagination import PaginationParams
from core.domain.entities.sector_entity import SectorEntity
from core.use_cases.sector_use_case import SectorUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.pagination_schema import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)
from presentation.schemas.sector_schema import SectorCreate, SectorOut, SectorUpdate


@api_controller("/sectors", tags=["Sectors"])
class SectorController:
    """Contrôleur pour la gestion des secteurs"""

    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.sector_use_case = SectorUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_get(
        "",
        response={
            200: PaginatedResultSchema[SectorOut],
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Récupérer tous les secteurs",
        description="Renvoie la liste de tous les secteurs disponibles avec pagination optionnelle",
    )
    def get_all_sectors(
        self,
        request,
        pagination: Query[PaginationParamsSchema],
    ):
        try:
            pagination_params = PaginationParams(
                page=pagination.page, per_page=pagination.per_page
            )
            result = self.sector_use_case.get_all_sectors(pagination_params)
            return 200, PaginatedResultSchema.from_domain_result(
                result,
                SectorOut,
                SectorOut.model_validate,
            )
        except Exception as e:
            self.logger.error(f"Error retrieving all sectors: {str(e)}")
            raise InternalServerError()

    @http_get(
        "/{sector_id}",
        response={200: SectorOut, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Récupérer un secteur par son ID",
        description="Renvoie les détails d'un secteur spécifié par son ID",
    )
    def get_sector(self, sector_id: int):
        try:
            sector = self.sector_use_case.get_sector(sector_id)
            return 200, SectorOut.model_validate(sector)
        except NotFoundError:
            self.logger.warning(f"Sector with ID {sector_id} not found")
            raise
        except Exception as e:
            self.logger.error(f"Error retrieving sector {sector_id}: {str(e)}")
            raise InternalServerError()

    @http_post(
        "",
        response={
            201: SectorOut,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Créer un nouveau secteur",
        description="Crée un nouveau secteur avec les données fournies",
    )
    def create_sector(self, request, sector_data: SectorCreate):
        try:
            sector_entity = SectorEntity(
                **sector_data.model_dump(),
                created_by=request.user.id,
            )
            created_sector = self.sector_use_case.create_sector(sector_entity)
            return 201, SectorOut.model_validate(created_sector)
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during sector creation: {str(e)}")
            raise ValidationError(e)
        except ConflictError:
            self.logger.warning("Conflict error during sector creation")
            raise
        except Exception as e:
            self.logger.error(f"Error creating sector: {str(e)}")
            raise InternalServerError()

    @http_put(
        "/{sector_id}",
        response={
            200: SectorOut,
            404: ErrorResponseSchema,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Mettre à jour un secteur",
        description="Met à jour les données d'un secteur existant",
    )
    def update_sector(self, request, sector_id: int, sector_data: SectorUpdate):
        try:
            existing_sector = self.sector_use_case.get_sector(sector_id)
            update_data = SectorEntity(
                id=existing_sector.id,
                name=(
                    sector_data.name
                    if sector_data.name is not None
                    else existing_sector.name
                ),
                region_id=(
                    sector_data.region_id
                    if sector_data.region_id is not None
                    else existing_sector.region_id
                ),
                created_at=existing_sector.created_at,
                created_by=existing_sector.created_by,
                updated_by=request.user.id,
            )
            updated_sector = self.sector_use_case.update_sector(sector_id, update_data)
            return 200, SectorOut.model_validate(updated_sector)
        except NotFoundError:
            self.logger.warning(f"Sector with ID {sector_id} not found for update")
            raise
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during sector update: {str(e)}")
            raise ValidationError(e)
        except ConflictError:
            self.logger.warning("Conflict error during sector update")
            raise
        except Exception as e:
            self.logger.error(f"Error updating sector {sector_id}: {str(e)}")
            raise InternalServerError()

    @http_delete(
        "/{sector_id}",
        response={204: None, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Supprimer un secteur",
        description="Supprime un secteur existant par son ID",
    )
    def delete_sector(self, sector_id: int):
        try:
            self.sector_use_case.delete_sector(sector_id)
            return 204, None
        except NotFoundError:
            self.logger.warning(f"Sector with ID {sector_id} not found for deletion")
            raise
        except Exception as e:
            self.logger.error(f"Error deleting sector {sector_id}: {str(e)}")
            raise InternalServerError()
