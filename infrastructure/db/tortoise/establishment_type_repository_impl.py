import logging
from typing import Optional
from uuid import UUID

from apps.tortoise.establishment_type.models import (
    EstablishmentType as TortoiseEstablishmentType,
)
from core.entities.establishment_type import EstablishmentTypeEntity
from core.entities.filters import EstablishmentTypeFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.establishment_type_repository import IEstablishmentTypeRepository
from infrastructure.db.tortoise.model_to_entity import establishment_type_to_entity

logger = logging.getLogger(__name__)


class EstablishmentTypeRepository(IEstablishmentTypeRepository):
    """
    Implémentation du repository pour les types d'établissements utilisant Tortoise ORM
    """

    async def _to_entity(
        self, establishment_type_model: TortoiseEstablishmentType
    ) -> EstablishmentTypeEntity:
        try:
            logger.debug(
                f"Converting establishment type model to entity for ID: {establishment_type_model.id}"
            )
            return await establishment_type_to_entity(establishment_type_model)
        except Exception as e:
            logger.error(f"Error converting establishment type model to entity: {e}")
            raise

    async def create(self, data: EstablishmentTypeEntity) -> EstablishmentTypeEntity:
        try:
            logger.info(f"Creating new establishment type: {data.name}")
            establishment_type_model = await TortoiseEstablishmentType.create(
                name=data.name,
                created_by_id=data.created_by,
            )
            result = await self._to_entity(establishment_type_model)
            logger.info(f"Establishment type created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating establishment type '{data.name}': {e}")
            raise

    async def get(self, id: UUID | int) -> Optional[EstablishmentTypeEntity]:
        try:
            logger.debug(f"Getting establishment type by ID: {id}")
            establishment_type_model = await TortoiseEstablishmentType.get(
                id=id
            ).prefetch_related("created_by", "updated_by")
            result = await self._to_entity(establishment_type_model)
            logger.debug(f"Establishment type found: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"Establishment type with ID {id} not found or error occurred: {e}"
            )
            return None

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[EstablishmentTypeEntity]:
        try:
            logger.debug(
                f"Getting all establishment types - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            establishment_type_models = (
                await TortoiseEstablishmentType.all()
                .prefetch_related("created_by", "updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseEstablishmentType.all().count()

            entities = [
                await self._to_entity(model) for model in establishment_type_models
            ]

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
                f"Retrieved {len(entities)} establishment types out of {total_count} total"
            )
            return result
        except Exception as e:
            logger.error(f"Error getting all establishment types: {e}")
            raise

    async def update(
        self, id: UUID | int, data: EstablishmentTypeEntity
    ) -> EstablishmentTypeEntity:
        try:
            logger.info(f"Updating establishment type with ID: {id}")
            establishment_type_model = await TortoiseEstablishmentType.get(id=id)

            establishment_type_model.name = data.name
            if data.updated_by is not None:
                establishment_type_model.updated_by_id = data.updated_by

            await establishment_type_model.save()
            await establishment_type_model.refresh_from_db()

            result = await self._to_entity(establishment_type_model)
            logger.info(f"Establishment type updated successfully: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"Establishment type with ID {id} not found or error occurred during update: {e}"
            )
            raise

    async def delete(self, id: UUID | int) -> bool:
        try:
            logger.info(f"Deleting establishment type with ID: {id}")
            establishment_type_model = await TortoiseEstablishmentType.get(id=id)
            establishment_type_name = establishment_type_model.name
            await establishment_type_model.delete()
            logger.info(
                f"Establishment type '{establishment_type_name}' deleted successfully"
            )
            return True
        except Exception as e:
            logger.warning(
                f"Establishment type with ID {id} not found or error occurred during deletion: {e}"
            )
            raise

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: EstablishmentTypeFilters,
    ) -> PaginatedResult[EstablishmentTypeEntity]:
        try:
            logger.debug(f"Filtering establishment types with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseEstablishmentType.all().prefetch_related(
                "created_by", "updated_by"
            )

            filter_dict = filters.to_orm_dict()

            if filter_dict:
                query = query.filter(**filter_dict)

            establishment_type_models = await query.offset(offset).limit(limit)

            total_count = (
                await TortoiseEstablishmentType.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseEstablishmentType.all().count()
            )

            entities = [
                await self._to_entity(model) for model in establishment_type_models
            ]

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
                f"Filtered {len(entities)} establishment types out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error filtering establishment types with criteria {filters}: {e}"
            )
            raise

    async def count(self, **kwargs) -> int:
        try:
            logger.debug(f"Counting establishment types with criteria: {kwargs}")
            if kwargs:
                count = await TortoiseEstablishmentType.filter(**kwargs).count()
            else:
                count = await TortoiseEstablishmentType.all().count()
            logger.debug(f"Establishment type count: {count}")
            return count
        except Exception as e:
            logger.error(
                f"Error counting establishment types with criteria {kwargs}: {e}"
            )
            raise

    async def get_by_name(self, name: str) -> Optional[EstablishmentTypeEntity]:
        try:
            logger.debug(f"Getting establishment type by name: {name}")
            establishment_type_model = await TortoiseEstablishmentType.get(
                name=name
            ).prefetch_related("created_by", "updated_by")
            result = await self._to_entity(establishment_type_model)
            logger.debug(f"Establishment type found by name: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"Establishment type with name '{name}' not found or error occurred: {e}"
            )
            return None
