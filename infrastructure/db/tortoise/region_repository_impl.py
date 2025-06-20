import logging
from typing import Optional
from uuid import UUID

from apps.tortoise.region.models import Region as TortoiseRegion
from core.entities.filters import RegionFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.region_entity import RegionEntity
from core.interfaces.region_repository import IRegionRepository
from infrastructure.db.tortoise.model_to_entity import region_to_entity

logger = logging.getLogger(__name__)


class RegionRepository(IRegionRepository):
    """
    Implémentation du repository pour les régions utilisant Tortoise ORM
    """

    async def _to_entity(self, region_model: TortoiseRegion) -> RegionEntity:
        try:
            logger.debug(
                f"Converting region model to entity for region ID: {region_model.id}"
            )
            return await region_to_entity(region_model)
        except Exception as e:
            logger.error(f"Error converting region model to entity: {e}")
            raise

    async def create(self, data: RegionEntity) -> RegionEntity:
        try:
            logger.info(f"Creating new region: {data.name}")
            region_model = await TortoiseRegion.create(
                name=data.name,
                created_by_id=data.created_by,
            )
            result = await self._to_entity(region_model)
            logger.info(f"Region created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating region '{data.name}': {e}")
            raise

    async def get(self, id: UUID | int) -> Optional[RegionEntity]:
        try:
            logger.debug(f"Getting region by ID: {id}")
            region_model = await TortoiseRegion.get(id=id).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(region_model)
            logger.debug(f"Region found: {result.name}")
            return result
        except Exception as e:
            logger.warning(f"Region with ID {id} not found or error occurred: {e}")
            return None

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[RegionEntity]:
        try:
            logger.debug(
                f"Getting all regions - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            region_models = (
                await TortoiseRegion.all()
                .prefetch_related("created_by", "updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseRegion.all().count()

            entities = [await self._to_entity(model) for model in region_models]

            total_pages = (
                total_count + pagination_params.per_page - 1
            ) // pagination_params.per_page
            next_page = (
                pagination_params.page + 1
                if pagination_params.page < total_pages
                else None
            )
            previous_page = (
                pagination_params.page - 1 if pagination_params.page > 1 else None
            )

            result = PaginatedResult(
                items=entities,
                total_items=total_count,
                page=pagination_params.page,
                per_page=pagination_params.per_page,
                total_pages=total_pages,
                next_page=next_page,
                previous_page=previous_page,
            )

            logger.info(f"Retrieved {len(entities)} regions out of {total_count} total")
            return result
        except Exception as e:
            logger.error(f"Error getting all regions: {e}")
            raise

    async def update(self, id: UUID | int, data: RegionEntity) -> RegionEntity:
        try:
            logger.info(f"Updating region with ID: {id}")
            region_model = await TortoiseRegion.get(id=id)

            region_model.name = data.name
            if data.updated_by is not None:
                region_model.updated_by_id = data.updated_by

            await region_model.save()
            await region_model.refresh_from_db()

            result = await self._to_entity(region_model)
            logger.info(f"Region updated successfully: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"Region with ID {id} not found or error occurred during update: {e}"
            )
            raise

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting region with ID: {id}")
            region_model = await TortoiseRegion.get(id=id)
            region_name = region_model.name
            await region_model.delete()
            logger.info(f"Region '{region_name}' deleted successfully")
            return True
        except Exception as e:
            logger.warning(
                f"Region with ID {id} not found or error occurred during deletion: {e}"
            )
            raise

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: RegionFilters,
    ) -> PaginatedResult[RegionEntity]:
        try:
            logger.debug(f"Filtering regions with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseRegion.all().prefetch_related("created_by", "updated_by")
            filter_dict = filters.to_orm_dict()

            if filter_dict:
                query = query.filter(**filter_dict)

            region_models = await query.offset(offset).limit(limit)

            total_count = (
                await TortoiseRegion.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseRegion.all().count()
            )

            entities = [await self._to_entity(model) for model in region_models]

            total_pages = (
                total_count + pagination_params.per_page - 1
            ) // pagination_params.per_page
            next_page = (
                pagination_params.page + 1
                if pagination_params.page < total_pages
                else None
            )
            previous_page = (
                pagination_params.page - 1 if pagination_params.page > 1 else None
            )

            result = PaginatedResult(
                items=entities,
                total_items=total_count,
                page=pagination_params.page,
                per_page=pagination_params.per_page,
                total_pages=total_pages,
                next_page=next_page,
                previous_page=previous_page,
            )

            logger.info(
                f"Filtered {len(entities)} regions out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            logger.error(f"Error filtering regions with criteria {filters}: {e}")
            raise

    async def count(self, **kwargs) -> int:
        try:
            logger.debug(f"Counting regions with criteria: {kwargs}")
            if kwargs:
                count = await TortoiseRegion.filter(**kwargs).count()
            else:
                count = await TortoiseRegion.all().count()
            logger.debug(f"Region count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting regions with criteria {kwargs}: {e}")
            raise

    async def get_by_name(self, name: str) -> Optional[RegionEntity]:
        try:
            logger.debug(f"Getting region by name: {name}")
            region_model = await TortoiseRegion.get(name=name).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(region_model)
            logger.debug(f"Region found by name: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"Region with name '{name}' not found or error occurred: {e}"
            )
            return None
