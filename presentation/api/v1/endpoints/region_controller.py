import logging
from typing import List

from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from pydantic import ValidationError as PydanticValidationError

from core.domain.entities.region_entity import RegionEntity
from core.use_cases.region_use_case import RegionUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.region_schema import RegionCreate, RegionOut, RegionUpdate


@api_controller("/regions", tags=["Regions"])
class RegionController:
    """Contrôleur pour la gestion des régions"""

    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.region_use_case = RegionUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_get(
        "",
        response={200: List[RegionOut], 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Récupérer toutes les régions",
        description="Renvoie la liste de toutes les régions disponibles",
    )
    def get_all_regions(self):
        """Récupère toutes les régions"""
        try:
            regions = self.region_use_case.get_all_regions()
            return 200, [RegionOut.model_validate(region) for region in regions]
        except Exception as e:
            self.logger.error(f"Error retrieving all regions: {str(e)}")
            raise InternalServerError()

    @http_get(
        "/{region_id}",
        response={200: RegionOut, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Récupérer une région par son ID",
        description="Renvoie les détails d'une région spécifiée par son ID",
    )
    def get_region(self, region_id: int):
        """Récupère une région par son ID"""
        try:
            region = self.region_use_case.get_region(region_id)
            return 200, RegionOut.model_validate(region)
        except NotFoundError:
            self.logger.warning(f"Region with ID {region_id} not found")
            raise
        except Exception as e:
            self.logger.error(f"Error retrieving region {region_id}: {str(e)}")
            raise InternalServerError()

    @http_post(
        "",
        response={
            201: RegionOut,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Créer une nouvelle région",
        description="Crée une nouvelle région avec les données fournies",
    )
    def create_region(self, request, region_data: RegionCreate):
        """Crée une nouvelle région"""
        try:
            region_entity = RegionEntity(
                **region_data.model_dump(),
                created_by=request.user.id,
            )
            created_region = self.region_use_case.create_region(region_entity)
            return 201, RegionOut.model_validate(created_region)
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during region creation: {str(e)}")
            raise ValidationError(e)
        except ConflictError:
            self.logger.warning("Conflict error during region creation")
            raise
        except Exception as e:
            self.logger.error(f"Error creating region: {str(e)}")
            raise InternalServerError()

    @http_put(
        "/{region_id}",
        response={
            200: RegionOut,
            404: ErrorResponseSchema,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Mettre à jour une région",
        description="Met à jour les données d'une région existante",
    )
    def update_region(self, request, region_id: int, region_data: RegionUpdate):
        """Met à jour une région existante"""
        try:
            # Récupérer d'abord la région existante
            existing_region = self.region_use_case.get_region(region_id)

            # Mettre à jour seulement les champs fournis
            update_data = RegionEntity(
                id=existing_region.id,
                name=(
                    region_data.name
                    if region_data.name is not None
                    else existing_region.name
                ),
                code=(
                    region_data.code
                    if region_data.code is not None
                    else existing_region.code
                ),
                created_at=existing_region.created_at,
                created_by=existing_region.created_by,
                updated_by=request.user.id,
            )

            updated_region = self.region_use_case.update_region(region_id, update_data)
            return 200, RegionOut.model_validate(updated_region)
        except NotFoundError:
            self.logger.warning(f"Region with ID {region_id} not found for update")
            raise
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during region update: {str(e)}")
            raise ValidationError(e)
        except ConflictError:
            self.logger.warning("Conflict error during region update")
            raise
        except Exception as e:
            self.logger.error(f"Error updating region {region_id}: {str(e)}")
            raise InternalServerError()

    @http_delete(
        "/{region_id}",
        response={204: None, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Supprimer une région",
        description="Supprime une région existante par son ID",
    )
    def delete_region(self, region_id: int):
        """Supprime une région"""
        try:
            self.region_use_case.delete_region(region_id)
            return 204, None
        except NotFoundError:
            self.logger.warning(f"Region with ID {region_id} not found for deletion")
            raise
        except Exception as e:
            self.logger.error(f"Error deleting region {region_id}: {str(e)}")
            raise InternalServerError()
