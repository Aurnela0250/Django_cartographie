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
from infrastructure.cache.cache_service import CacheService
from infrastructure.cache.cache_utils import cache_response
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from infrastructure.external_services.redis_service import RedisService
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
        # Initialiser RedisService et CacheService
        self.redis_service = RedisService()
        self.cache_service = CacheService(
            redis_service=self.redis_service,
            entity_name="establishment",
            logger=self.logger,
        )

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
            # Invalidation du cache des listes
            self.cache_service.invalidate_list_caches()
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
        domain_pagination_params = PaginationParams(
            page=pagination.page, per_page=pagination.per_page
        )
        filter_str = CacheService.generate_filter_cache_key_string(filter_params)

        # Essayer de récupérer depuis le cache
        cached_data = self.cache_service.get_paginated_list(
            pagination_params=domain_pagination_params,
            response_schema_type=PaginatedResultSchema[EstablishmentSchema],
            filter_str=filter_str,
        )
        if cached_data:
            return 200, cached_data

        # Si cache miss
        try:
            establishments_result = self.establishment_use_case.filter_establishments(
                name=filter_params.name,
                acronyme=filter_params.acronyme,
                establishment_type_id=filter_params.establishment_type_id,
                city_id=filter_params.city_id,
                region_id=filter_params.region_id,
                domain_id=filter_params.domain_id,
                level_id=filter_params.level_id,
                pagination_params=domain_pagination_params,
            )

            response_schema = PaginatedResultSchema.from_domain_result(
                establishments_result,
                EstablishmentSchema,
                EstablishmentSchema.model_validate,
            )
            # Mettre en cache le résultat
            self.cache_service.set_paginated_list(
                pagination_params=domain_pagination_params,
                data=response_schema,
                filter_str=filter_str,
            )
            return 200, response_schema
        except ValidationError as e:
            self.logger.warning(f"Validation error occurred: {e}")
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "/{establishment_id}",
        response=EstablishmentSchema,
    )
    @cache_response(
        cache_type="item",
        cache_service=lambda self, *a, **kw: self.cache_service,
        schema_type=EstablishmentSchema,
        get_id=lambda self, establishment_id, **kwargs: establishment_id,
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
            # Invalidation des caches
            self.cache_service.invalidate_detail_cache(establishment_id)
            self.cache_service.invalidate_list_caches()
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
            # Invalidation des caches
            self.cache_service.invalidate_detail_cache(establishment_id)
            self.cache_service.invalidate_list_caches()
            return 204, None
        except NotFoundError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "",
        response=PaginatedResultSchema[EstablishmentSchema],
    )
    @cache_response(
        cache_type="list",
        cache_service=lambda self, *a, **kw: self.cache_service,
        schema_type=PaginatedResultSchema[EstablishmentSchema],
        get_pagination=lambda self, request, pagination, **kwargs: PaginationParams(
            page=pagination.page, per_page=pagination.per_page
        ),
    )
    def get_all_establishments(
        self,
        request,
        pagination: Query[PaginationParamsSchema],
    ):
        """Get all establishments"""
        try:
            domain_pagination_params = PaginationParams(
                page=pagination.page, per_page=pagination.per_page
            )
            establishments_result = self.establishment_use_case.get_all_establishments(
                domain_pagination_params
            )
            return PaginatedResultSchema.from_domain_result(
                establishments_result,
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
            rating_value = rating_data.rating
            user_id = request.auth.get("user_id")

            success = self.establishment_use_case.rate_establishment(
                establishment_id=establishment_id, user_id=user_id, rating=rating_value
            )

            if success:
                self.logger.info(
                    f"Établissement {establishment_id} noté avec succès par l'utilisateur {user_id}"
                )
                self.cache_service.invalidate_detail_cache(establishment_id)
                self.cache_service.invalidate_list_caches()
                return 201, None
            else:
                self.logger.warning(
                    f"L'utilisateur {user_id} a déjà noté l'établissement {establishment_id} ou autre conflit."
                )
                # Correction: Passer explicitement le message et None pour les headers
                # Le message métier est loggué, la réponse API reste standardisée
                raise ConflictError()

        except NotFoundError as e:
            self.logger.warning(f"Établissement {establishment_id} non trouvé")
            raise e
        except ValidationError as e:
            self.logger.warning(f"Erreur de validation: {e}")
            raise e
        except ConflictError as e:
            self.logger.warning(f"Conflit lors de la notation: {e}")
            raise e
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la notation de l'établissement: {e}", exc_info=True
            )
            raise InternalServerError()
            raise InternalServerError()
            self.logger.warning(f"Conflit lors de la notation: {e}")
