import logging
from uuid import UUID

from tortoise.exceptions import DoesNotExist, IntegrityError

from apps.tortoise.domain.models import Domain as TortoiseDomain
from core.entities.domain import DomainEntity
from core.entities.filters import DomainFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.domain_repository import IDomainRepository
from infrastructure.db.tortoise.model_to_entity import domain_to_entity
from presentation.exceptions import (
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
)

logger = logging.getLogger(__name__)


class DomainRepository(IDomainRepository):
    """
    Implémentation du repository pour les domaines utilisant Tortoise ORM
    """

    async def _to_entity(self, domain_model: TortoiseDomain) -> DomainEntity:
        """
        Méthode locale pour mapper un modèle Tortoise vers une entité Domain

        Args:
            domain_model: Le modèle Tortoise Domain à convertir

        Returns:
            DomainEntity: L'entité Domain convertie
        """
        try:
            logger.debug(
                f"Converting domain model to entity for domain ID: {domain_model.id}"
            )
            return await domain_to_entity(domain_model)
        except Exception as e:
            logger.error(f"Error converting domain model to entity: {e}")
            raise DatabaseException("Failed to convert domain model to entity", cause=e)

    async def create(self, data: DomainEntity) -> DomainEntity:
        """
        Crée un nouveau domaine dans la base de données

        Args:
            data: L'entité Domain à créer

        Returns:
            DomainEntity: L'entité Domain créée avec son ID
        """
        try:
            logger.info(f"Creating new domain: {data.name}")
            domain_model = await TortoiseDomain.create(
                name=data.name,
                created_by_id=data.created_by,
            )
            await domain_model.fetch_related("created_by", "updated_by")
            result = await self._to_entity(domain_model)
            logger.info(f"Domain created successfully with ID: {result.id}")
            return result
        except IntegrityError as e:
            logger.warning(
                f"Integrity error creating domain '{data.name}': {e}", exc_info=True
            )
            raise DatabaseIntegrityException(
                f"Domain with name '{data.name}' already exists.", cause=e
            )
        except Exception as e:
            logger.error(f"Error creating domain '{data.name}': {e}", exc_info=True)
            raise DatabaseException("Error creating domain", cause=e)

    async def get(self, id: UUID | int) -> DomainEntity:
        """
        Récupère un domaine par son ID

        Args:
            id: L'ID du domaine à récupérer

        Returns:
            Optional[DomainEntity]: L'entité Domain ou None si non trouvé
        """
        try:
            logger.debug(f"Getting domain by ID: {id}")
            domain_model = await TortoiseDomain.get(id=id).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(domain_model)
            logger.debug(f"Domain found: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Domain with ID {id} not found.")
            raise DatabaseDoesNotExistException(
                f"Domain with ID {id} not found.", cause=e
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while getting domain {id}: {e}",
                exc_info=True,
            )
            raise DatabaseException("Error getting domain by ID", cause=e)

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[DomainEntity]:
        """
        Récupère tous les domaines avec pagination

        Args:
            pagination_params: Paramètres de pagination

        Returns:
            PaginatedResult[DomainEntity]: Résultat paginé des domaines
        """
        try:
            logger.debug(
                f"Getting all domains - page: {pagination_params.page}, per_page: {pagination_params.per_page}"
            )
            offset = pagination_params.offset
            limit = pagination_params.limit

            domain_models = (
                await TortoiseDomain.all()
                .prefetch_related("created_by", "updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseDomain.all().count()

            entities = [await self._to_entity(model) for model in domain_models]

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

            logger.info(f"Retrieved {len(entities)} domains out of {total_count} total")
            return result
        except Exception as e:
            logger.error(f"Error getting all domains: {e}", exc_info=True)
            raise DatabaseException("Error getting all domains", cause=e)

    async def update(self, id: UUID | int, data: DomainEntity) -> DomainEntity:
        """
        Met à jour un domaine existant

        Args:
            id: L'ID du domaine à mettre à jour
            data: Les nouvelles données du domaine

        Returns:
            DomainEntity: L'entité Domain mise à jour
        Raises:
            DatabaseDoesNotExistException: Si le domaine n'existe pas
            DatabaseIntegrityException: Si une contrainte d'intégrité est violée
            DatabaseException: Pour toute autre erreur de base de données
        """
        try:
            logger.info(f"Updating domain with ID: {id}")
            domain_model = await TortoiseDomain.get(id=id)

            # Mise à jour des champs
            domain_model.name = data.name
            if data.updated_by is not None:
                domain_model.updated_by_id = data.updated_by

            await domain_model.save()
            await domain_model.fetch_related("created_by", "updated_by")

            result = await self._to_entity(domain_model)
            logger.info(f"Domain updated successfully: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Domain with ID {id} not found for update.")
            raise DatabaseDoesNotExistException(
                f"Domain with ID {id} not found.", cause=e
            )
        except IntegrityError as e:
            logger.warning(
                f"Integrity error updating domain {id} with name '{data.name}': {e}",
                exc_info=True,
            )
            raise DatabaseIntegrityException(
                f"A domain with name '{data.name}' may already exist.", cause=e
            )
        except Exception as e:
            logger.error(
                f"Error updating domain {id}: {e}",
                exc_info=True,
            )
            raise DatabaseException("Error updating domain", cause=e)

    async def delete(self, id: UUID | int) -> bool:
        """
        Supprime un domaine par son ID

        Args:
            id: L'ID du domaine à supprimer

        Returns:
            bool: True si supprimé avec succès, False sinon
        """
        try:
            logger.info(f"Deleting domain with ID: {id}")
            domain_model = await TortoiseDomain.get(id=id)
            domain_name = domain_model.name
            await domain_model.delete()
            logger.info(f"Domain '{domain_name}' deleted successfully")
            return True
        except DoesNotExist as e:
            logger.warning(f"Domain with ID {id} not found for deletion.")
            raise DatabaseDoesNotExistException(
                f"Domain with ID {id} not found.", cause=e
            )
        except Exception as e:
            logger.error(
                f"Error deleting domain {id}: {e}",
                exc_info=True,
            )
            raise DatabaseException("Error deleting domain", cause=e)

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: DomainFilters,
    ) -> PaginatedResult[DomainEntity]:
        """
        Filtre les domaines selon les critères fournis avec typage strict

        Args:
            pagination_params: Paramètres de pagination
            filters: Filtres typés avec validation Pydantic

        Returns:
            PaginatedResult[DomainEntity]: Résultat paginé des domaines filtrés
        """
        try:
            logger.debug(f"Filtering domains with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseDomain.all().prefetch_related("created_by", "updated_by")

            # Convertir les filtres Pydantic en dictionnaire pour Tortoise ORM
            filter_dict = filters.to_orm_dict()

            # Appliquer les filtres
            if filter_dict:
                query = query.filter(**filter_dict)

            domain_models = await query.offset(offset).limit(limit)

            # Compter le total avec les mêmes filtres
            total_count = (
                await TortoiseDomain.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseDomain.all().count()
            )

            entities = [await self._to_entity(model) for model in domain_models]

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
                f"Filtered {len(entities)} domains out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            logger.error(
                f"Error filtering domains with criteria {filters}: {e}", exc_info=True
            )
            raise DatabaseException("Error filtering domains", cause=e)

    async def count(self, **kwargs) -> int:
        """
        Compte le nombre de domaines selon les critères fournis

        Args:
            **kwargs: Critères de filtrage optionnels

        Returns:
            int: Le nombre de domaines correspondant aux critères
        """
        raise NotImplementedError

    async def get_by_name(self, name: str) -> DomainEntity:
        """
        Récupère un domaine par son nom

        Args:
            name: Le nom du domaine à récupérer

        Returns:
            DomainEntity: L'entité Domain ou Raise DoesNotExist si non trouvé
        """
        try:
            logger.debug(f"Getting domain by name: {name}")
            domain_model = await TortoiseDomain.get(name=name).prefetch_related(
                "created_by", "updated_by"
            )
            result = await self._to_entity(domain_model)
            logger.debug(f"Domain found by name: {result.name}")
            return result
        except DoesNotExist as e:
            logger.warning(f"Domain with name '{name}' not found.")
            raise DatabaseDoesNotExistException(
                f"Domain with name '{name}' not found.", cause=e
            )
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while getting domain by name '{name}': {e}",
                exc_info=True,
            )
            raise DatabaseException("Error getting domain by name", cause=e)
