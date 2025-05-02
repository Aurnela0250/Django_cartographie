import logging
from typing import List

from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from pydantic import ValidationError as PydanticValidationError

from core.domain.entities.domain_entity import DomainEntity
from core.use_cases.domain_use_case import DomainUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.domain_schema import DomainCreate, DomainOut, DomainUpdate
from presentation.schemas.error_schema import ErrorResponseSchema


@api_controller("/domains", tags=["Domains"])
class DomainController:
    """Contrôleur pour la gestion des domaines"""

    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.domain_use_case = DomainUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_get(
        "",
        response={200: List[DomainOut], 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Récupérer tous les domaines",
        description="Renvoie la liste de tous les domaines disponibles",
    )
    def get_all_domains(self, request):
        try:
            domains = self.domain_use_case.get_all_domains()
            return 200, [DomainOut.model_validate(domain) for domain in domains]
        except Exception as e:
            self.logger.error(f"Error retrieving all domains: {str(e)}")
            raise InternalServerError()

    @http_get(
        "/{domain_id}",
        response={200: DomainOut, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Récupérer un domaine par son ID",
        description="Renvoie les détails d'un domaine spécifié par son ID",
    )
    def get_domain(self, request, domain_id: int):
        try:
            domain = self.domain_use_case.get_domain(domain_id)
            return 200, DomainOut.model_validate(domain)
        except NotFoundError as e:
            self.logger.warning(f"Domain with ID {domain_id} not found")
            raise e
        except Exception as e:
            self.logger.error(f"Error retrieving domain {domain_id}: {str(e)}")
            raise InternalServerError()

    @http_post(
        "",
        response={
            201: DomainOut,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Créer un nouveau domaine",
        description="Crée un nouveau domaine avec les données fournies",
    )
    def create_domain(self, request, domain_data: DomainCreate):
        try:
            # Mettre à jour created_by dans le dictionnaire avant l'instanciation
            domain_dict = domain_data.model_dump()
            domain_dict["created_by"] = request.user.id
            domain_entity = DomainEntity(**domain_dict)

            created_domain = self.domain_use_case.create_domain(domain_entity)
            return 201, DomainOut.model_validate(created_domain)
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during domain creation: {str(e)}")
            raise ValidationError(e)
        except ConflictError as e:
            self.logger.warning("Conflict error during domain creation")
            raise e
        except Exception as e:
            self.logger.error(f"Error creating domain: {str(e)}")
            raise InternalServerError()

    @http_put(
        "/{domain_id}",
        response={
            200: DomainOut,
            404: ErrorResponseSchema,
            409: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
        summary="Mettre à jour un domaine",
        description="Met à jour les données d'un domaine existant",
    )
    def update_domain(self, request, domain_id: int, domain_data: DomainUpdate):
        try:
            existing_domain = self.domain_use_case.get_domain(domain_id)
            update_data = DomainEntity(
                id=existing_domain.id,
                name=(
                    domain_data.name
                    if domain_data.name is not None
                    else existing_domain.name
                ),
                created_at=existing_domain.created_at,
                created_by=existing_domain.created_by,
                updated_by=request.user.id,
            )
            updated_domain = self.domain_use_case.update_domain(domain_id, update_data)
            return 200, DomainOut.model_validate(updated_domain)
        except NotFoundError as e:
            self.logger.warning(f"Domain with ID {domain_id} not found for update")
            raise e
        except PydanticValidationError as e:
            self.logger.warning(f"Validation error during domain update: {str(e)}")
            raise ValidationError(e)
        except ConflictError:
            self.logger.warning("Conflict error during domain update")
            raise
        except Exception as e:
            self.logger.error(f"Error updating domain {domain_id}: {str(e)}")
            raise InternalServerError()

    @http_delete(
        "/{domain_id}",
        response={204: None, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
        auth=jwt_auth,
        summary="Supprimer un domaine",
        description="Supprime un domaine existant par son ID",
    )
    def delete_domain(self, request, domain_id: int):
        try:
            self.domain_use_case.delete_domain(domain_id)
            return 204, None
        except NotFoundError:
            self.logger.warning(f"Domain with ID {domain_id} not found for deletion")
            raise
        except Exception as e:
            self.logger.error(f"Error deleting domain {domain_id}: {str(e)}")
            raise InternalServerError()
