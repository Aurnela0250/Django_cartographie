import logging

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
    EstablishmentFilterParamsSchema,
    EstablishmentSchema,
    RateEstablishmentSchema,
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
        self.logger = logging.getLogger(__name__)

    @http_post(
        "",
        response={201: EstablishmentSchema},
    )
    def create_establishment(
        self,
        request,
        establishment_data: CreateEstablishmentSchema,
    ):
        """Create a new establishment"""
        try:
            entity_data = EstablishmentEntity(
                **establishment_data.model_dump(),
                created_by=request.auth.get("user_id"),
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

    @http_get(
        "/filter",
        response=PaginatedResultSchema[EstablishmentSchema],
    )
    def filter_establishments(
        self,
        request,
        filter_params: Query[EstablishmentFilterParamsSchema],
        pagination: Query[PaginationParamsSchema],
    ):
        """Filtrer les établissements selon différents critères"""
        try:
            pagination_params = PaginationParams(
                page=pagination.page, per_page=pagination.per_page
            )

            establishments = self.establishment_use_case.filter_establishments(
                name=filter_params.name,
                acronyme=filter_params.acronyme,
                establishment_type_id=filter_params.establishment_type_id,
                city_id=filter_params.city_id,
                region_id=filter_params.region_id,
                domain_id=filter_params.domain_id,
                level_id=filter_params.level_id,  # Ajout du paramètre
                pagination_params=pagination_params,
            )

            return 200, PaginatedResultSchema.from_domain_result(
                establishments,
                EstablishmentSchema,
                EstablishmentSchema.model_validate,
            )
        except ValidationError as e:
            self.logger.warning(f"Validation error occurred: {e}")
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "/{establishment_id}",
        response=EstablishmentSchema,
    )
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

    @http_put(
        "/{establishment_id}",
        response=EstablishmentSchema,
    )
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

    @http_delete(
        "/{establishment_id}",
        response={204: None},
    )
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
        "",
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
                establishments,
                EstablishmentSchema,
                EstablishmentSchema.model_validate,
            )

        except ValidationError as e:
            self.logger.warning(f"Validation error occurred: {e}")
            raise e
        except Exception:
            raise InternalServerError()

    @http_post(
        "/{establishment_id}/rate",
        response={201: None, 409: None},
    )
    def rate_establishment(
        self,
        request,
        establishment_id: int,
        rating_data: RateEstablishmentSchema,
    ):
        """Noter un établissement (un utilisateur ne peut voter qu'une fois par établissement)"""
        try:
            # Récupération de la valeur du rating
            rating_value = rating_data.rating

            # Récupération de l'ID de l'utilisateur depuis le token JWT
            user_id = request.auth.get("user_id")

            # Appel au use case pour noter l'établissement
            success = self.establishment_use_case.rate_establishment(
                establishment_id=establishment_id, user_id=user_id, rating=rating_value
            )

            # Si la notation a réussi, retourner un code 201 (Created)
            if success:
                self.logger.info(
                    f"Établissement {establishment_id} noté avec succès par l'utilisateur {user_id}"
                )
                return 201, None
            else:
                # Si l'utilisateur a déjà noté cet établissement, retourner un code 409 (Conflict)
                self.logger.warning(
                    f"L'utilisateur {user_id} a déjà noté l'établissement {establishment_id}"
                )
                raise ConflictError()

        except NotFoundError as e:
            self.logger.warning(f"Établissement {establishment_id} non trouvé")
            raise e
        except ValidationError as e:
            self.logger.warning(f"Erreur de validation: {e}")
            raise e
        except ConflictError:
            self.logger.warning("L'utilisateur a déjà voté pour cet établissement")
            raise
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la notation de l'établissement: {e}", exc_info=True
            )
            raise InternalServerError()
