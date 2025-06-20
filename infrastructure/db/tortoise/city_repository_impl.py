import logging
from typing import Optional
from uuid import UUID

from apps.tortoise.city.models import City as TortoiseCity
from core.entities.city_entity import CityEntity
from core.entities.filters import CityFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.city_repository import ICityRepository
from infrastructure.db.tortoise.model_to_entity import city_to_entity

logger = logging.getLogger(__name__)


class CityRepository(ICityRepository):
    """
    Implémentation du repository pour les villes utilisant Tortoise ORM
    """

    async def _to_entity(self, city_model: TortoiseCity) -> CityEntity:
        """
        Méthode locale pour mapper un modèle Tortoise vers une entité City

        Args:
            city_model: Le modèle Tortoise City à convertir

        Returns:
            CityEntity: L'entité City convertie
        """
        try:
            logger.debug(
                f"Converting city model to entity for city ID: {city_model.id}"
            )
            return await city_to_entity(city_model)
        except Exception as e:
            logger.error(f"Error converting city model to entity: {e}")
            raise

    async def create(self, data: CityEntity) -> CityEntity:
        """
        Crée une nouvelle ville dans la base de données

        Args:
            data: L'entité City à créer

        Returns:
            CityEntity: L'entité City créée avec son ID
        """
        try:
            logger.info(f"Creating new city: {data.name}")
            city_model = await TortoiseCity.create(
                name=data.name,
                region_id=data.region_id,
                created_by_id=data.created_by,
            )
            result = await self._to_entity(city_model)
            logger.info(f"City created successfully with ID: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Error creating city '{data.name}': {e}")
            raise

    async def get(self, id: UUID | int) -> Optional[CityEntity]:
        """
        Récupère une ville par son ID

        Args:
            id: L'ID de la ville à récupérer

        Returns:
            Optional[CityEntity]: L'entité City ou None si non trouvée
        """
        try:
            logger.debug(f"Getting city by ID: {id}")
            city_model = await TortoiseCity.get(id=id).prefetch_related(
                "region", "created_by", "updated_by"
            )
            result = await self._to_entity(city_model)
            logger.debug(f"City found: {result.name}")
            return result
        except Exception as e:
            logger.warning(f"City with ID {id} not found or error occurred: {e}")
            return None

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[CityEntity]:
        """
        Récupère toutes les villes avec pagination

        Args:
            pagination_params: Paramètres de pagination

        Returns:
            PaginatedResult[CityEntity]: Résultat paginé des villes
        """
        try:
            logger.debug(
                f"Getting all cities - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            city_models = (
                await TortoiseCity.all()
                .prefetch_related("region", "created_by", "updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseCity.all().count()

            entities = [await self._to_entity(model) for model in city_models]

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

            logger.info(f"Retrieved {len(entities)} cities out of {total_count} total")
            return result
        except Exception as e:
            logger.error(f"Error getting all cities: {e}")
            raise

    async def update(self, id: UUID | int, data: CityEntity) -> CityEntity:
        """
        Met à jour une ville existante

        Args:
            id: L'ID de la ville à mettre à jour
            data: Les nouvelles données de la ville

        Returns:
            CityEntity: L'entité City mise à jour
        """
        try:
            logger.info(f"Updating city with ID: {id}")
            city_model = await TortoiseCity.get(id=id)

            # Mise à jour des champs
            city_model.name = data.name
            if data.region_id is not None:
                city_model.region_id = data.region_id
            if data.updated_by is not None:
                city_model.updated_by_id = data.updated_by

            await city_model.save()
            await city_model.refresh_from_db()

            result = await self._to_entity(city_model)
            logger.info(f"City updated successfully: {result.name}")
            return result
        except Exception as e:
            logger.warning(
                f"City with ID {id} not found or error occurred during update: {e}"
            )
            raise

    async def delete(self, id: UUID | int) -> bool:
        """
        Supprime une ville par son ID

        Args:
            id: L'ID de la ville à supprimer

        Returns:
            bool: True si supprimée avec succès, False sinon
        """
        try:
            logger.info(f"Deleting city with ID: {id}")
            city_model = await TortoiseCity.get(id=id)
            city_name = city_model.name
            await city_model.delete()
            logger.info(f"City '{city_name}' deleted successfully")
            return True
        except Exception as e:
            logger.warning(
                f"City with ID {id} not found or error occurred during deletion: {e}"
            )
            raise

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: CityFilters,
    ) -> PaginatedResult[CityEntity]:
        """
        Filtre les villes selon les critères fournis avec typage strict

        Args:
            pagination_params: Paramètres de pagination
            filters: Filtres typés avec validation Pydantic

        Returns:
            PaginatedResult[CityEntity]: Résultat paginé des villes filtrées
        """
        try:
            logger.debug(f"Filtering cities with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseCity.all().prefetch_related(
                "region", "created_by", "updated_by"
            )

            filter_dict = filters.to_orm_dict()

            if filter_dict:
                query = query.filter(**filter_dict)

            city_models = await query.offset(offset).limit(limit)

            total_count = (
                await TortoiseCity.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseCity.all().count()
            )

            entities = [await self._to_entity(model) for model in city_models]

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
                f"Filtered {len(entities)} cities out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            logger.error(f"Error filtering cities with criteria {filters}: {e}")
            raise

    async def count(self, **kwargs) -> int:
        """
        Compte le nombre de villes selon les critères fournis

        Args:
            **kwargs: Critères de filtrage optionnels

        Returns:
            int: Le nombre de villes correspondant aux critères
        """
        try:
            logger.debug(f"Counting cities with criteria: {kwargs}")
            if kwargs:
                count = await TortoiseCity.filter(**kwargs).count()
            else:
                count = await TortoiseCity.all().count()
            logger.debug(f"City count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting cities with criteria {kwargs}: {e}")
            raise

    async def get_by_name(self, name: str) -> Optional[CityEntity]:
        """
        Récupère une ville par son nom

        Args:
            name: Le nom de la ville à récupérer

        Returns:
            Optional[CityEntity]: L'entité City ou None si non trouvée
        """
        try:
            logger.debug(f"Getting city by name: {name}")
            city_model = await TortoiseCity.get(name=name).prefetch_related(
                "region", "created_by", "updated_by"
            )
            result = await self._to_entity(city_model)
            logger.debug(f"City found by name: {result.name}")
            return result
        except Exception as e:
            logger.warning(f"City with name '{name}' not found or error occurred: {e}")
            return None
