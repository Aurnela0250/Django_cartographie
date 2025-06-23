import logging
from typing import Optional
from uuid import UUID

from tortoise.exceptions import DoesNotExist, IntegrityError

from apps.tortoise.level.models import Level as TortoiseLevel
from core.entities.filters import LevelFilters
from core.entities.level import LevelEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.level_repository import ILevelRepository
from infrastructure.db.tortoise.model_to_entity import level_to_entity
from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
)

logger = logging.getLogger(__name__)


class LevelRepository(ILevelRepository):
    """
    Implémentation du repository pour les niveaux utilisant Tortoise ORM
    """

    async def _to_entity(self, level_model: TortoiseLevel) -> LevelEntity:
        try:
            logger.debug(
                f"Converting level model to entity for level ID: {level_model.id}"
            )
            return await level_to_entity(level_model)
        except Exception as e:
            logger.error(f"Error converting level model to entity: {e}")
            raise DatabaseException(cause=e)

    async def create(self, data: LevelEntity) -> LevelEntity:
        try:
            logger.info(f"Creating new level: {data.name}")
            level_model = await TortoiseLevel.create(
                name=data.name,
                acronym=data.acronym,
                created_by_id=data.created_by,
            )
            result = await self._to_entity(level_model)
            logger.info(f"Level created successfully with ID: {result.id}")
            return result
        except IntegrityError as e:
            logger.error(
                f"Error creating level '{data.name}' due to integrity error: {e}"
            )
            raise DatabaseIntegrityException(cause=e)
        except Exception as e:
            logger.error(f"Error creating level '{data.name}': {e}")
            raise DatabaseException(cause=e)

    async def get(self, id: UUID | int) -> Optional[LevelEntity]:
        try:
            logger.debug(f"Getting level by ID: {id}")
            level_model = await TortoiseLevel.get(id=id).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(level_model)
            logger.debug(f"Level found: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Level with ID {id} not found: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error getting level with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[LevelEntity]:
        try:
            logger.debug(
                f"Getting all levels - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            level_models = (
                await TortoiseLevel.all()
                .prefetch_related("created_by", "updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseLevel.all().count()

            entities = [await self._to_entity(model) for model in level_models]

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

            logger.info(f"Retrieved {len(entities)} levels out of {total_count} total")
            return result
        except Exception as e:
            logger.error(f"Error getting all levels: {e}")
            raise DatabaseException(cause=e)

    async def update(self, id: UUID | int, data: LevelEntity) -> LevelEntity:
        try:
            logger.info(f"Updating level with ID: {id}")
            level_model = await TortoiseLevel.get(id=id)

            level_model.name = data.name
            if data.acronym is not None:
                level_model.acronym = data.acronym
            if data.updated_by is not None:
                level_model.updated_by_id = data.updated_by

            await level_model.save()
            await level_model.refresh_from_db()

            result = await self._to_entity(level_model)
            logger.info(f"Level updated successfully: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Level with ID {id} not found for update: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except IntegrityError as e:
            logger.error(
                f"Error updating level with ID {id} due to integrity error: {e}"
            )
            raise DatabaseIntegrityException(cause=e)
        except Exception as e:
            logger.error(f"Error updating level with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting level with ID: {id}")
            level_model = await TortoiseLevel.get(id=id)
            level_name = level_model.name
            await level_model.delete()
            logger.info(f"Level '{level_name}' deleted successfully")
            return True
        except DoesNotExist as e:
            logger.warning(f"Level with ID {id} not found for deletion: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error deleting level with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: LevelFilters,
    ) -> PaginatedResult[LevelEntity]:
        try:
            logger.debug(f"Filtering levels with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseLevel.all().prefetch_related("created_by", "updated_by")

            filter_dict = filters.to_orm_dict()

            if filter_dict:
                query = query.filter(**filter_dict)

            level_models = await query.offset(offset).limit(limit)

            total_count = (
                await TortoiseLevel.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseLevel.all().count()
            )

            entities = [await self._to_entity(model) for model in level_models]

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
                f"Filtered {len(entities)} levels out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            logger.error(f"Error filtering levels with criteria {filters}: {e}")
            raise DatabaseException(cause=e)

    async def count(self, **kwargs) -> int:
        try:
            logger.debug(f"Counting levels with criteria: {kwargs}")
            if kwargs:
                count = await TortoiseLevel.filter(**kwargs).count()
            else:
                count = await TortoiseLevel.all().count()
            logger.debug(f"Level count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting levels with criteria {kwargs}: {e}")
            raise DatabaseException(cause=e)

    async def get_by_name(self, name: str) -> Optional[LevelEntity]:
        try:
            logger.debug(f"Getting level by name: {name}")
            level_model = await TortoiseLevel.get(name=name).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(level_model)
            logger.debug(f"Level found by name: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Level with name '{name}' not found: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error getting level by name '{name}': {e}")
            raise DatabaseException(cause=e)

    async def get_by_acronym(self, acronym: str) -> Optional[LevelEntity]:
        try:
            logger.debug(f"Getting level by acronym: {acronym}")
            level_model = await TortoiseLevel.get(acronym=acronym).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(level_model)
            logger.debug(f"Level found by acronym: {result.acronym}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Level with acronym '{acronym}' not found: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error getting level by acronym '{acronym}': {e}")
            raise DatabaseException(cause=e)
