import logging
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel, TypeAdapter

from core.domain.entities.pagination import PaginationParams
from infrastructure.external_services.redis_service import RedisService
from presentation.schemas.pagination_schema import PaginatedResultSchema

T = TypeVar("T", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

DEFAULT_CACHE_TTL_DETAIL_SECONDS = 3600  # 1 heure
DEFAULT_CACHE_TTL_LIST_SECONDS = 600  # 10 minutes


class CacheService:
    def __init__(
        self,
        redis_service: RedisService,
        entity_name: str,  # e.g., "establishment", "formation"
        logger: Optional[logging.Logger] = None,
    ):
        self.redis_service = redis_service
        self.entity_name = entity_name
        self.logger = logger or logging.getLogger(__name__)

        # Default TTLs (can be overridden if needed per entity type)
        self.ttl_detail_seconds = DEFAULT_CACHE_TTL_DETAIL_SECONDS
        self.ttl_list_seconds = DEFAULT_CACHE_TTL_LIST_SECONDS

        # Cache key prefixes and version keys
        self.detail_prefix = f"{self.entity_name}_detail"
        self.list_all_prefix = f"{self.entity_name}_all"
        self.list_filter_prefix = f"{self.entity_name}_filter"

        self.version_key_all = f"{self.entity_name}_all_version"
        self.version_key_filter = f"{self.entity_name}_filter_version"

    def _get_current_version(self, version_key: str) -> int:
        version = self.redis_service.get(version_key)
        return int(version) if version is not None else 0

    def _increment_version(self, version_key: str):
        client = self.redis_service.get_client()
        if client is not None:
            client.incr(version_key)
            self.logger.info(
                f"Cache version key '{version_key}' incremented for '{self.entity_name}'."
            )
        else:
            self.logger.error("Redis client is None, cannot increment version key.")

    def invalidate_detail_cache(self, item_id: Any):
        cache_key = f"{self.detail_prefix}:{item_id}"
        if self.redis_service.exists(cache_key):
            self.redis_service.delete(cache_key)
            self.logger.info(f"Cache invalidated for key: {cache_key}")

    def invalidate_list_caches(self):
        self._increment_version(self.version_key_all)
        self._increment_version(self.version_key_filter)
        self.logger.info(f"List caches invalidated for '{self.entity_name}'.")

    def get_item(self, item_id: Any, schema_type: Type[T]) -> Optional[T]:
        cache_key = f"{self.detail_prefix}:{item_id}"
        cached_data = self.redis_service.get(cache_key)
        if cached_data:
            self.logger.info(f"Cache hit for {self.entity_name} detail: {cache_key}")
            return schema_type.model_validate_json(cached_data)
        self.logger.info(f"Cache miss for {self.entity_name} detail: {cache_key}")
        return None

    def set_item(self, item_id: Any, item_data: BaseModel, ttl: Optional[int] = None):
        if not isinstance(item_data, BaseModel):
            self.logger.error(
                f"Item data for {self.entity_name} ID {item_id} is not a Pydantic model."
            )
            return

        cache_key = f"{self.detail_prefix}:{item_id}"
        ttl_to_use = ttl if ttl is not None else self.ttl_detail_seconds
        try:
            self.redis_service.set(
                cache_key, item_data.model_dump_json(), exp=ttl_to_use
            )
            self.logger.info(
                f"Cache set for {self.entity_name} detail: {cache_key} with TTL {ttl_to_use}s"
            )
        except Exception as e:
            self.logger.error(
                f"Error setting cache for {self.entity_name} detail {cache_key}: {e}"
            )

    def get_paginated_list(
        self,
        pagination_params: PaginationParams,
        response_schema_type: Type[
            PaginatedResultSchema[SchemaType]
        ],  # e.g. PaginatedResultSchema[EstablishmentSchema]
        filter_str: Optional[str] = None,  # For filtered lists
    ) -> Optional[PaginatedResultSchema[SchemaType]]:
        is_filtered_list = filter_str is not None
        version_key = (
            self.version_key_filter if is_filtered_list else self.version_key_all
        )
        base_prefix = (
            self.list_filter_prefix if is_filtered_list else self.list_all_prefix
        )

        current_version = self._get_current_version(version_key)

        cache_key_parts = [
            base_prefix,
            f"v{current_version}",
        ]
        if is_filtered_list:
            cache_key_parts.append(f"filters_{filter_str}")

        cache_key_parts.extend(
            [f"page_{pagination_params.page}", f"per_page_{pagination_params.per_page}"]
        )
        cache_key = ":".join(cache_key_parts)

        cached_data = self.redis_service.get(cache_key)
        if cached_data:
            self.logger.info(f"Cache hit for {self.entity_name} list: {cache_key}")
            try:
                # TypeAdapter is needed for generic types like PaginatedResultSchema[SchemaType]
                adapter = TypeAdapter(response_schema_type)
                return adapter.validate_json(cached_data)
            except Exception as e:
                self.logger.error(
                    f"Error parsing cached list for {self.entity_name} from key {cache_key}: {e}"
                )
                return None
        self.logger.info(f"Cache miss for {self.entity_name} list: {cache_key}")
        return None

    def set_paginated_list(
        self,
        pagination_params: PaginationParams,
        data: PaginatedResultSchema[SchemaType],
        filter_str: Optional[str] = None,  # For filtered lists
        ttl: Optional[int] = None,
    ):
        if not isinstance(data, PaginatedResultSchema):
            self.logger.error(
                f"Data for {self.entity_name} list is not a PaginatedResultSchema model."
            )
            return

        is_filtered_list = filter_str is not None
        version_key = (
            self.version_key_filter if is_filtered_list else self.version_key_all
        )
        base_prefix = (
            self.list_filter_prefix if is_filtered_list else self.list_all_prefix
        )

        current_version = self._get_current_version(version_key)

        cache_key_parts = [
            base_prefix,
            f"v{current_version}",
        ]
        if is_filtered_list:
            cache_key_parts.append(f"filters_{filter_str}")

        cache_key_parts.extend(
            [f"page_{pagination_params.page}", f"per_page_{pagination_params.per_page}"]
        )
        cache_key = ":".join(cache_key_parts)

        ttl_to_use = ttl if ttl is not None else self.ttl_list_seconds
        try:
            self.redis_service.set(cache_key, data.model_dump_json(), exp=ttl_to_use)
            self.logger.info(
                f"Cache set for {self.entity_name} list: {cache_key} with TTL {ttl_to_use}s"
            )
        except Exception as e:
            self.logger.error(
                f"Error setting cache for {self.entity_name} list {cache_key}: {e}"
            )

    @staticmethod
    def generate_filter_cache_key_string(filter_params: BaseModel) -> str:
        """Génère une chaîne stable à partir des paramètres de filtre pour la clé de cache."""
        params_dict = filter_params.model_dump(exclude_none=True)
        return "_".join(f"{k}:{v}" for k, v in sorted(params_dict.items()))
