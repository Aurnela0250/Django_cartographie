import logging
from typing import Optional
from uuid import UUID

from tortoise.exceptions import DoesNotExist, IntegrityError

from apps.tortoise.formation.models import Formation as TortoiseFormation
from core.entities.filters import FormationFilters
from core.entities.formation import FormationEntity
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.formation_repository import IFormationRepository
from infrastructure.db.tortoise.metadata import FormationToEntityMetadata
from infrastructure.db.tortoise.model_to_entity import formation_to_entity
from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
)

logger = logging.getLogger(__name__)


class FormationRepository(IFormationRepository):
    """
    Implémentation du repository pour les formations utilisant Tortoise ORM
    """

    async def _to_entity(self, formation_model: TortoiseFormation) -> FormationEntity:
        try:
            logger.debug(
                f"Converting formation model to entity for formation ID: {formation_model.id}"
            )
            return await formation_to_entity(
                formation_model,
                metadata=FormationToEntityMetadata(
                    level=True,
                    mention=True,
                    establishment=False,
                    authorization=True,
                ),
            )
        except Exception as e:
            logger.error(f"Error converting formation model to entity: {e}")
            raise DatabaseException(cause=e)

    async def create(self, data: FormationEntity) -> FormationEntity:
        try:
            logger.info(f"Creating new formation: {data.name}")
            formation_model = await TortoiseFormation.create(
                name=data.name,
                description=data.description,
                duration=data.duration,
                level_id=data.level_id,
                mention_id=data.mention_id,
                establishment_id=data.establishment_id,
                authorization_id=data.authorization_id,
                created_by_id=data.created_by,
            )
            result = await self._to_entity(formation_model)
            logger.info(f"Formation created successfully with ID: {result.id}")
            return result
        except IntegrityError as e:
            logger.error(f"Error creating formation '{data.name}': {e}")
            raise DatabaseIntegrityException(cause=e)
        except Exception as e:
            logger.error(f"Error creating formation '{data.name}': {e}")
            raise DatabaseException(cause=e)

    async def get(self, id: UUID | int) -> Optional[FormationEntity]:
        try:
            logger.debug(f"Getting formation by ID: {id}")
            formation_model = await TortoiseFormation.get(id=id).prefetch_related(
                "establishment", "domain", "created_by", "updated_by"
            )
            result = await self._to_entity(formation_model)
            logger.debug(f"Formation found: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Formation with ID {id} not found: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error getting formation with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[FormationEntity]:
        try:
            logger.debug(
                f"Getting all formations - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            formation_models = (
                await TortoiseFormation.all()
                .prefetch_related("establishment", "domain", "created_by", "updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseFormation.all().count()

            entities = [await self._to_entity(model) for model in formation_models]

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
                f"Retrieved {len(entities)} formations out of {total_count} total"
            )
            return result
        except Exception as e:
            logger.error(f"Error getting all formations: {e}")
            raise DatabaseException(cause=e)

    async def update(self, id: UUID | int, data: FormationEntity) -> FormationEntity:
        try:
            logger.info(f"Updating formation with ID: {id}")
            formation_model = await TortoiseFormation.get(id=id)

            formation_model.name = data.name
            if data.description is not None:
                formation_model.description = data.description
            if data.duration is not None:
                formation_model.duration = data.duration
            if data.level_id is not None:
                formation_model.level_id = data.level_id
            if data.mention_id is not None:
                formation_model.mention_id = data.mention_id
            if data.establishment_id is not None:
                formation_model.establishment_id = data.establishment_id
            if data.authorization_id is not None:
                formation_model.authorization_id = data.authorization_id
            if data.updated_by is not None:
                formation_model.updated_by_id = data.updated_by

            await formation_model.save()
            await formation_model.refresh_from_db()

            result = await self._to_entity(formation_model)
            logger.info(f"Formation updated successfully: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Formation with ID {id} not found for update: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except IntegrityError as e:
            logger.error(f"Error updating formation with ID {id}: {e}")
            raise DatabaseIntegrityException(cause=e)
        except Exception as e:
            logger.error(f"Error updating formation with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting formation with ID: {id}")
            formation_model = await TortoiseFormation.get(id=id)
            formation_name = formation_model.name
            await formation_model.delete()
            logger.info(f"Formation '{formation_name}' deleted successfully")
            return True
        except DoesNotExist as e:
            logger.warning(f"Formation with ID {id} not found for deletion: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error deleting formation with ID {id}: {e}")
            raise DatabaseException(cause=e)

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: FormationFilters,
    ) -> PaginatedResult[FormationEntity]:
        try:
            logger.debug(f"Filtering formations with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseFormation.all().prefetch_related(
                "establishment",
                "domain",
                "created_by",
                "updated_by",
            )

            filter_dict = filters.to_orm_dict()

            if filter_dict:
                query = query.filter(**filter_dict)

            formation_models = await query.offset(offset).limit(limit)

            total_count = (
                await TortoiseFormation.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseFormation.all().count()
            )

            entities = [await self._to_entity(model) for model in formation_models]

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
                f"Filtered {len(entities)} formations out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            logger.error(f"Error filtering formations with criteria {filters}: {e}")
            raise DatabaseException(cause=e)

    async def count(self, **kwargs) -> int:
        try:
            logger.debug(f"Counting formations with criteria: {kwargs}")
            if kwargs:
                count = await TortoiseFormation.filter(**kwargs).count()
            else:
                count = await TortoiseFormation.all().count()
            logger.debug(f"Formation count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting formations with criteria {kwargs}: {e}")
            raise DatabaseException(cause=e)

    async def get_by_name(self, name: str) -> Optional[FormationEntity]:
        try:
            logger.debug(f"Getting formation by name: {name}")
            formation_model = await TortoiseFormation.get(name=name).prefetch_related(
                "establishment", "domain", "created_by", "updated_by"
            )
            result = await self._to_entity(formation_model)
            logger.debug(f"Formation found by name: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Formation with name '{name}' not found: {e}")
            raise DatabaseDoesNotExistException(cause=e)
        except Exception as e:
            logger.error(f"Error getting formation by name '{name}': {e}")
            raise DatabaseException(cause=e)
