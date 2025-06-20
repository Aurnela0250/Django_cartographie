import logging
from typing import Optional
from uuid import UUID

from tortoise.exceptions import DoesNotExist, FieldError

from apps.tortoise.establishment.models import Establishment as TortoiseEstablishment
from core.entities.establishment_entity import EstablishmentEntity
from core.entities.filters import EstablishmentFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.establishment_repository import IEstablishmentRepository
from infrastructure.db.tortoise.metadata import EstablishmentToEntityMetadata
from infrastructure.db.tortoise.model_to_entity import establishment_to_entity

logger = logging.getLogger(__name__)


class EstablishmentRepository(IEstablishmentRepository):
    """
    Implémentation du repository pour les établissements utilisant Tortoise ORM
    """

    async def _to_entity(
        self, establishment_model: TortoiseEstablishment
    ) -> EstablishmentEntity:
        try:
            logger.debug(
                f"Converting establishment model to entity for establishment ID: {establishment_model.id}"
            )
            return await establishment_to_entity(
                establishment_model,
                metadata=EstablishmentToEntityMetadata(
                    establishment_type=True,
                    city=True,
                    formations=True,
                ),
            )
        except Exception as e:
            logger.error(f"Error converting establishment model to entity: {e}")
            raise

    async def create(self, data: EstablishmentEntity) -> EstablishmentEntity:
        try:
            logger.info(f"Creating new establishment: {data.name}")
            establishment_model = await TortoiseEstablishment.create(
                name=data.name,
                city_id=data.city_id,
                establishment_type_id=data.establishment_type_id,
                created_by_id=data.created_by,
            )
            result = await self._to_entity(establishment_model)
            logger.info(f"Establishment created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating establishment '{data.name}': {e}")
            raise

    async def get(self, id: UUID | int) -> Optional[EstablishmentEntity]:
        try:
            logger.debug(f"Getting establishment by ID: {id}")
            establishment_model = await TortoiseEstablishment.get(
                id=id
            ).prefetch_related("city", "establishment_type", "created_by", "updated_by")
            result = await self._to_entity(establishment_model)
            logger.debug(f"Establishment found: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"Establishment with ID {id} not found or error occurred: {e}"
            )
            return None

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[EstablishmentEntity]:
        try:
            logger.debug(
                f"Getting all establishments - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            establishment_models = (
                await TortoiseEstablishment.all()
                .prefetch_related(
                    "city", "establishment_type", "created_by", "updated_by"
                )
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseEstablishment.all().count()

            entities = [await self._to_entity(model) for model in establishment_models]

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
                f"Retrieved {len(entities)} establishments out of {total_count} total"
            )
            return result
        except Exception as e:
            logger.error(f"Error getting all establishments: {e}")
            raise

    async def update(
        self, id: UUID | int, data: EstablishmentEntity
    ) -> EstablishmentEntity:
        try:
            logger.info(f"Updating establishment with ID: {id}")
            establishment_model = await TortoiseEstablishment.get(id=id)

            establishment_model.name = data.name
            if data.city_id is not None:
                establishment_model.city_id = data.city_id
            if data.establishment_type_id is not None:
                establishment_model.establishment_type_id = data.establishment_type_id
            if data.updated_by is not None:
                establishment_model.updated_by_id = data.updated_by

            await establishment_model.save()
            await establishment_model.refresh_from_db()

            result = await self._to_entity(establishment_model)
            logger.info(f"Establishment updated successfully: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"Establishment with ID {id} not found or error occurred during update: {e}"
            )
            raise

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting establishment with ID: {id}")
            establishment_model = await TortoiseEstablishment.get(id=id)
            establishment_name = establishment_model.name
            await establishment_model.delete()
            logger.info(f"Establishment '{establishment_name}' deleted successfully")
            return True
        except Exception as e:
            logger.warning(
                f"Establishment with ID {id} not found or error occurred during deletion: {e}"
            )
            raise

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: EstablishmentFilters,
    ) -> PaginatedResult[EstablishmentEntity]:
        try:
            logger.debug(f"Filtering establishments with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseEstablishment.all().prefetch_related(
                "city", "establishment_type", "created_by", "updated_by"
            )

            filter_dict = filters.to_orm_dict()

            if filter_dict:
                query = query.filter(**filter_dict)

            establishment_models = await query.offset(offset).limit(limit)

            total_count = (
                await TortoiseEstablishment.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseEstablishment.all().count()
            )

            entities = [await self._to_entity(model) for model in establishment_models]

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
                f"Filtered {len(entities)} establishments out of {total_count} matching criteria"
            )
            return result
        except FieldError as e:
            logger.error(
                f"If the field to prefetch on is not a relation, or not found: {e}"
            )
            raise e
        except Exception as e:
            logger.error(f"Error filtering establishments with criteria {filters}: {e}")
            raise e

    async def count(self, **kwargs) -> int:
        try:
            logger.debug(f"Counting establishments with criteria: {kwargs}")
            if kwargs:
                count = await TortoiseEstablishment.filter(**kwargs).count()
            else:
                count = await TortoiseEstablishment.all().count()
            logger.debug(f"Establishment count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting establishments with criteria {kwargs}: {e}")
            raise

    async def get_by_name(self, name: str) -> Optional[EstablishmentEntity]:
        try:
            logger.debug(f"Getting establishment by name: {name}")
            establishment_model = await TortoiseEstablishment.get(
                name=name
            ).prefetch_related("city", "establishment_type", "created_by", "updated_by")
            result = await self._to_entity(establishment_model)
            logger.debug(f"Establishment found by name: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Establishment with name '{name}' not found: {e}")
            return None
        except Exception as e:
            logger.warning(
                f"Establishment with name '{name}' not found or error occurred: {e}"
            )
            return None
