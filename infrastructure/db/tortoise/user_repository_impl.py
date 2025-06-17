import logging
from typing import Optional
from uuid import UUID

from apps.tortoise.users.models import User as TortoiseUser
from core.entities.filters import UserFilters
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.user_entity import UserEntity
from core.interfaces.user_repository import IUserRepository
from infrastructure.db.tortoise.model_to_entity import user_to_entity


class UserRepository(IUserRepository):
    """
    Implémentation du repository User utilisant Tortoise ORM
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def _to_entity(self, user_model: TortoiseUser) -> UserEntity:
        """
        Convertit un modèle Tortoise User vers une UserEntity

        Args:
            user_model: L'objet User de Tortoise ORM

        Returns:
            UserEntity: L'entité User correspondante
        """
        self.logger.debug(
            f"Conversion du modèle User (ID: {user_model.id}) vers UserEntity"
        )
        try:
            result = await user_to_entity(user_model)
            self.logger.debug(
                f"Conversion réussie pour l'utilisateur ID: {user_model.id}"
            )
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la conversion du modèle User (ID: {user_model.id}): {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la conversion du modèle vers l'entité: {str(e)}"
            )

    async def create(self, data: UserEntity) -> UserEntity:
        """
        Crée un nouvel utilisateur dans la base de données

        Args:
            data: L'entité utilisateur à créer

        Returns:
            UserEntity: L'utilisateur créé avec son ID
        """
        self.logger.info(f"Création d'un nouvel utilisateur avec l'email: {data.email}")
        try:
            user_model = await TortoiseUser.create(
                email=data.email,
                password=data.password,
                active=data.active,
                updated_by_id=data.updated_by,
            )
            result = await self._to_entity(user_model)
            self.logger.info(
                f"Utilisateur créé avec succès - ID: {user_model.id}, Email: {data.email}"
            )
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la création de l'utilisateur avec l'email {data.email}: {str(e)}"
            )
            raise ValueError(f"Erreur lors de la création de l'utilisateur: {str(e)}")

    async def get(self, id: UUID | int) -> Optional[UserEntity]:
        """
        Récupère un utilisateur par son ID

        Args:
            id: L'ID de l'utilisateur

        Returns:
            Optional[UserEntity]: L'utilisateur trouvé ou None
        """
        self.logger.debug(f"Récupération de l'utilisateur avec l'ID: {id}")
        try:
            user_model = await TortoiseUser.get(id=id).prefetch_related("updated_by")
            result = await self._to_entity(user_model)
            self.logger.debug(f"Utilisateur trouvé avec l'ID: {id}")
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la récupération de l'utilisateur avec l'ID: {id} - {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la récupération de l'utilisateur avec l'ID {id}: {str(e)}"
            )

    async def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[UserEntity]:
        """
        Récupère tous les utilisateurs avec pagination

        Args:
            pagination_params: Paramètres de pagination

        Returns:
            PaginatedResult[UserEntity]: Résultat paginé des utilisateurs
        """
        self.logger.info(
            f"Récupération de tous les utilisateurs - Page: {pagination_params.page}, Per page: {pagination_params.per_page}"
        )
        try:
            offset = pagination_params.offset
            limit = pagination_params.limit

            user_models = (
                await TortoiseUser.all()
                .prefetch_related("updated_by")
                .offset(offset)
                .limit(limit)
            )

            total_count = await TortoiseUser.all().count()
            users = [await self._to_entity(user_model) for user_model in user_models]

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
                items=users,
                total_items=total_count,
                page=pagination_params.page,
                per_page=pagination_params.per_page,
                total_pages=total_pages,
                next_page=next_page,
                previous_page=previous_page,
            )
            self.logger.info(
                f"Récupération réussie - {len(users)} utilisateurs trouvés sur {total_count} au total"
            )
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la récupération de tous les utilisateurs: {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la récupération de tous les utilisateurs: {str(e)}"
            )

    async def update(self, id: UUID | int, data: UserEntity) -> Optional[UserEntity]:
        """
        Met à jour un utilisateur existant

        Args:
            id: L'ID de l'utilisateur à mettre à jour
            data: Les nouvelles données de l'utilisateur

        Returns:
            Optional[UserEntity]: L'utilisateur mis à jour ou None si introuvable
        """
        self.logger.info(f"Mise à jour de l'utilisateur avec l'ID: {id}")
        try:
            user_model = await TortoiseUser.get(id=id)

            # Mise à jour des champs
            user_model.email = data.email
            user_model.updated_by_id = data.updated_by

            await user_model.save()
            await user_model.refresh_from_db(fields=["updated_by"])

            result = await self._to_entity(user_model)
            self.logger.info(
                f"Utilisateur mis à jour avec succès - ID: {id}, Email: {data.email}"
            )
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la mise à jour de l'utilisateur avec l'ID: {id} - {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la mise à jour de l'utilisateur avec l'ID {id}: {str(e)}"
            )

    async def delete(self, id: UUID | int) -> bool:
        """
        Supprime un utilisateur

        Args:
            id: L'ID de l'utilisateur à supprimer

        Returns:
            bool: True si supprimé avec succès, False sinon
        """
        self.logger.info(f"Suppression de l'utilisateur avec l'ID: {id}")
        try:
            user_model = await TortoiseUser.get(id=id)
            await user_model.delete()
            self.logger.info(f"Utilisateur supprimé avec succès - ID: {id}")
            return True
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la suppression de l'utilisateur avec l'ID: {id} - {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la suppression de l'utilisateur avec l'ID {id}: {str(e)}"
            )

    async def filter(
        self,
        pagination_params: PaginationParams,
        filters: UserFilters,
    ) -> PaginatedResult[UserEntity]:
        """
        Filtre les utilisateurs selon les critères fournis avec typage strict

        Args:
            pagination_params: Paramètres de pagination
            filters: Filtres typés avec validation Pydantic

        Returns:
            PaginatedResult[UserEntity]: Résultat paginé des utilisateurs filtrés
        """
        try:
            self.logger.debug(f"Filtering users with criteria: {filters}")
            offset = pagination_params.offset
            limit = pagination_params.limit

            query = TortoiseUser.all().prefetch_related("updated_by")

            # Convertir les filtres Pydantic en dictionnaire pour Tortoise ORM
            filter_dict = filters.to_orm_dict()

            # Appliquer les filtres
            if filter_dict:
                query = query.filter(**filter_dict)

            user_models = await query.offset(offset).limit(limit)

            # Compter le total avec les mêmes filtres
            total_count = (
                await TortoiseUser.filter(**filter_dict).count()
                if filter_dict
                else await TortoiseUser.all().count()
            )

            users = [await self._to_entity(user_model) for user_model in user_models]

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
                items=users,
                total_items=total_count,
                page=pagination_params.page,
                per_page=pagination_params.per_page,
                total_pages=total_pages,
                next_page=next_page,
                previous_page=previous_page,
            )

            self.logger.info(
                f"Filtered {len(users)} users out of {total_count} matching criteria"
            )
            return result
        except Exception as e:
            self.logger.error(f"Error filtering users with criteria {filters}: {e}")
            raise

    async def count(self, **kwargs) -> int:
        """
        Compte le nombre d'utilisateurs correspondant aux critères

        Args:
            **kwargs: Critères de filtrage

        Returns:
            int: Nombre d'utilisateurs
        """
        self.logger.debug(f"Comptage des utilisateurs avec les critères: {kwargs}")
        try:
            result = await TortoiseUser.filter(**kwargs).count()
            self.logger.debug(
                f"Comptage réussi - {result} utilisateurs trouvés avec les critères: {kwargs}"
            )
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur lors du comptage des utilisateurs avec les critères {kwargs}: {str(e)}"
            )
            raise ValueError(f"Erreur lors du comptage des utilisateurs: {str(e)}")

    async def create_user(self, user: UserEntity) -> UserEntity:
        """
        Crée un nouvel utilisateur (méthode spécifique à IUserRepository)

        Args:
            user: L'entité utilisateur à créer

        Returns:
            UserEntity: L'utilisateur créé
        """
        self.logger.info(f"Appel de create_user pour l'email: {user.email}")
        try:
            result = await self.create(user)
            self.logger.info(f"create_user réussi pour l'email: {user.email}")
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur dans create_user pour l'email {user.email}: {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la création de l'utilisateur (create_user): {str(e)}"
            )

    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Récupère un utilisateur par son email

        Args:
            email: L'email de l'utilisateur

        Returns:
            Optional[UserEntity]: L'utilisateur trouvé ou None
        """
        self.logger.debug(f"Recherche de l'utilisateur avec l'email: {email}")
        try:
            user_model = await TortoiseUser.get(email=email).prefetch_related(
                "updated_by"
            )
            result = await self._to_entity(user_model)
            self.logger.debug(f"Utilisateur trouvé avec l'email: {email}")
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur lors de la recherche de l'utilisateur avec l'email: {email} - {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la récupération de l'utilisateur avec l'email {email}: {str(e)}"
            )

    async def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        """
        Récupère un utilisateur par son ID

        Args:
            user_id: L'ID de l'utilisateur

        Returns:
            Optional[UserEntity]: L'utilisateur trouvé ou None
        """
        self.logger.debug(f"Appel de get_user_by_id pour l'ID: {user_id}")
        try:
            result = await self.get(user_id)
            self.logger.debug(f"get_user_by_id réussi pour l'ID: {user_id}")
            return result
        except Exception as e:
            self.logger.error(
                f"Erreur dans get_user_by_id pour l'ID {user_id}: {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la récupération de l'utilisateur par ID: {str(e)}"
            )
