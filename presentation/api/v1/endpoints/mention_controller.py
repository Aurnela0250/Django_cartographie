import logging

from ninja import Query
from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import IsAuthenticated

from core.domain.entities.pagination import PaginationParams
from core.use_cases.mention_use_case import MentionUseCase
from infrastructure.cache.cache_service import CacheService
from infrastructure.cache.cache_utils import cache_response
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.mention_schema import (
    CreateMentionSchema,
    MentionSchema,
    UpdateMentionSchema,
)
from presentation.schemas.pagination_schema import (
    PaginatedResultSchema,
    PaginationParamsSchema,
)


@api_controller(
    "/mentions",
    tags=["Mentions"],
    auth=jwt_auth,
    permissions=[IsAuthenticated],
)
class MentionController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.mention_use_case = MentionUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)
        from infrastructure.external_services.redis_service import RedisService

        self.redis_service = RedisService()
        self.cache_service = CacheService(
            redis_service=self.redis_service, entity_name="mention", logger=self.logger
        )

    @http_post(
        "",
        response={
            201: MentionSchema,
            400: ErrorResponseSchema,
            404: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def create_mention(self, request, payload: CreateMentionSchema):
        """Creates a new mention."""
        try:
            mention = self.mention_use_case.create(payload, request.user.id)
            # Utiliser from_orm pour pydantic v1 ou model_validate pour pydantic v2
            return 201, MentionSchema.from_orm(mention)
        except Exception as e:
            self.logger.error(f"Error creating mention: {e}")
            raise e

    @http_get(
        "/{mention_id}",
        response={
            200: MentionSchema,
            404: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    @cache_response(
        cache_type="item",
        cache_service=lambda self, *a, **kw: self.cache_service,
        schema_type=MentionSchema,
        get_id=lambda self, request, mention_id, **kwargs: mention_id,
    )
    def get_mention(self, request, mention_id: int):
        """Retrieves a specific mention by its ID."""
        mention = self.mention_use_case.get(mention_id)
        return MentionSchema.from_orm(mention)

    @http_get(
        "",
        response={
            200: PaginatedResultSchema[MentionSchema],
            500: ErrorResponseSchema,
        },
    )
    @cache_response(
        cache_type="list",
        cache_service=lambda self, *a, **kw: self.cache_service,
        schema_type=PaginatedResultSchema[MentionSchema],
        get_pagination=lambda self, request, pagination, **kwargs: PaginationParams(
            page=pagination.page, per_page=pagination.per_page
        ),
    )
    def get_all_mentions(
        self,
        request,
        pagination: Query[PaginationParamsSchema],
    ):
        """Retrieves all mentions."""
        pagination_params = PaginationParams(
            page=pagination.page, per_page=pagination.per_page
        )
        mentions = self.mention_use_case.get_all(pagination_params)
        return PaginatedResultSchema.from_domain_result(
            mentions,
            MentionSchema,
            MentionSchema.model_validate,
        )

    @http_put(
        "/{mention_id}",
        response={
            200: MentionSchema,
            400: ErrorResponseSchema,
            404: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def update_mention(self, request, mention_id: int, payload: UpdateMentionSchema):
        """Updates an existing mention."""
        try:
            updated_mention = self.mention_use_case.update(
                mention_id, payload, request.user.id
            )
            return MentionSchema.from_orm(updated_mention)
        except Exception as e:
            raise e

    @http_delete(
        "/{mention_id}",
        response={204: None, 404: ErrorResponseSchema, 500: ErrorResponseSchema},
    )
    def delete_mention(self, request, mention_id: int):
        """Deletes a mention."""
        try:
            self.mention_use_case.delete(mention_id)
            return 204, None
        except Exception as e:
            raise e
