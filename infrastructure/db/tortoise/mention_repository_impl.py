import logging
from typing import Optional
from uuid import UUID

from tortoise.exceptions import DoesNotExist, IntegrityError

from apps.tortoise.mention.models import Mention as TortoiseMention
from core.entities.filters import MentionFilters
from core.entities.mention import MentionEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.mention_repository import IMentionRepository
from infrastructure.db.tortoise.model_to_entity import mention_to_entity
from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
)

logger = logging.getLogger(__name__)


class MentionRepository(IMentionRepository):
    """
    Implémentation du repository pour les mentions utilisant Tortoise ORM
    """

    async def _to_entity(self, mention_model: TortoiseMention) -> MentionEntity:
        try:
            logger.debug(
                f"Converting mention model to entity for mention ID: {mention_model.id}"
            )
            return await mention_to_entity(mention_model)
        except Exception as e:
            logger.error(f"Error converting mention model to entity: {e}")
            raise DatabaseException(cause=e)

    async def create(self, data: MentionEntity) -> MentionEntity:
        try:
            logger.info(f"Creating new mention: {data.name}")
            mention_model = await TortoiseMention.create(
                name=data.name,
                created_by_id=data.created_by,
            )
            result = await self._to_entity(mention_model)
            logger.info(f"Mention created successfully with ID: {result.id}")
            return result
        except IntegrityError as e:
            logger.error(f"Integrity error creating mention '{data.name}': {e}")
            raise DatabaseIntegrityException(cause=e)
        except Exception as e:
            logger.error(f"Error creating mention '{data.name}': {e}")
            raise DatabaseException(cause=e)

    async def get(self, id: UUID | int) -> Optional[MentionEntity]:
        try:
            logger.debug(f"Getting mention by ID: {id}")
            mention_model = await TortoiseMention.get(id=id).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(mention_model)
            logger.debug(f"Mention found: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Mention with ID {id} not found.")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error getting mention with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[MentionEntity]:
        try:
            logger.debug(
                f"Getting all mentions - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            mention_models = (
                await TortoiseMention.all()
                .prefetch_related("created_by", "updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseMention.all().count()

            entities = [await self._to_entity(model) for model in mention_models]

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
                f"Retrieved {len(entities)} mentions out of {total_count} total"
            )
            return result
        except Exception as e:
            logger.error(f"Error getting all mentions: {e}")
            raise DatabaseException(cause=e)

    async def update(self, id: UUID | int, data: MentionEntity) -> MentionEntity:
        try:
            logger.info(f"Updating mention with ID: {id}")
            mention_model = await TortoiseMention.get(id=id)

            mention_model.name = data.name
            mention_model.domain_id = data.domain_id
            if data.updated_by is not None:
                mention_model.updated_by_id = data.updated_by

            await mention_model.save()
            await mention_model.refresh_from_db()

            result = await self._to_entity(mention_model)
            logger.info(f"Mention updated successfully: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Mention with ID {id} not found for update.")
            raise DatabaseDoesNotExistException(cause=e)
        except IntegrityError as e:
            logger.error(f"Integrity error updating mention with ID {id}: {e}")
            raise DatabaseIntegrityException(cause=e)
        except Exception as e:
            logger.error(f"Error updating mention with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting mention with ID: {id}")
            mention_model = await TortoiseMention.get(id=id)
            mention_name = mention_model.name
            await mention_model.delete()
            logger.info(f"Mention '{mention_name}' deleted successfully")
            return True
        except DoesNotExist as e:
            logger.warning(f"Mention with ID {id} not found for deletion.")
            raise DatabaseDoesNotExistException(cause=e)
        except IntegrityError as e:
            logger.error(f"Integrity error deleting mention with ID {id}: {e}")
            raise DatabaseIntegrityException(cause=e)
        except Exception as e:
            logger.error(f"Error deleting mention with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: MentionFilters,
    ) -> PaginatedResult[MentionEntity]:
        try:
            logger.debug(f"Filtering mentions with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseMention.all().prefetch_related("created_by", "updated_by")

            filter_dict = filters.to_orm_dict()

            if filter_dict:
                query = query.filter(**filter_dict)

            mention_models = await query.offset(offset).limit(limit)

            total_count = (
                await TortoiseMention.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseMention.all().count()
            )

            entities = [await self._to_entity(model) for model in mention_models]

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
                f"Filtered {len(entities)} mentions out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            logger.error(f"Error filtering mentions with criteria {filters}: {e}")
            raise DatabaseException(cause=e)

    async def count(self, **kwargs) -> int:
        try:
            logger.debug(f"Counting mentions with criteria: {kwargs}")
            if kwargs:
                count = await TortoiseMention.filter(**kwargs).count()
            else:
                count = await TortoiseMention.all().count()
            logger.debug(f"Mention count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting mentions with criteria {kwargs}: {e}")
            raise DatabaseException(cause=e)

    async def get_by_name(self, name: str) -> Optional[MentionEntity]:
        try:
            logger.debug(f"Getting mention by name: {name}")
            mention_model = await TortoiseMention.get(name=name).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(mention_model)
            logger.debug(f"Mention found by name: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Mention with name '{name}' not found.")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error getting mention by name '{name}': {e}")
            raise DatabaseException(cause=e)
