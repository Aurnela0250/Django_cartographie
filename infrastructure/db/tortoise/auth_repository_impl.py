import logging
from uuid import UUID

from tortoise.exceptions import DoesNotExist

from apps.tortoise.user.models import User as TortoiseUser
from core.entities.pagination import PaginatedResult, PaginationParams
from core.entities.user import UserEntity
from core.interfaces.auth_repository import IAuthRepository
from infrastructure.db.tortoise.model_to_entity import user_to_entity

logger = logging.getLogger(__name__)


class AuthRepository(IAuthRepository):
    """
    Implémentation de l'interface IAuthRepository pour Tortoise ORM
    """

    async def _to_entity(self, user: TortoiseUser) -> UserEntity:
        """
        Méthode locale pour mapper un modèle Tortoise User vers UserEntity
        """
        try:
            return await user_to_entity(user)
        except Exception as e:
            logger.error(
                f"Erreur lors de la conversion du modèle vers l'entité: {str(e)}"
            )
            raise ValueError(
                f"Erreur lors de la conversion du modèle vers l'entité: {str(e)}"
            )

    async def signup(self, email: str, hashed_password: str) -> UserEntity:
        """
        Créer un nouvel utilisateur avec email et mot de passe hashé
        """
        try:
            logger.info(f"Tentative de création d'utilisateur avec email: {email}")
            user = await TortoiseUser.create(
                email=email,
                password=hashed_password,
                active=True,
            )
            logger.info(f"Utilisateur créé avec succès, ID: {user.id}")
            return await self._to_entity(user)
        except Exception as e:
            logger.error(
                f"Erreur lors de la création de l'utilisateur avec email {email}: {str(e)}"
            )
            raise RuntimeError(f"Erreur lors de la création de l'utilisateur: {str(e)}")

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        """
        Récupérer un utilisateur par son email
        """
        try:
            logger.debug(f"Recherche d'utilisateur par email: {email}")
            user = await TortoiseUser.filter(email=email).first()
            if not user:
                logger.debug(f"Aucun utilisateur trouvé pour l'email: {email}")
                return None
            logger.debug(f"Utilisateur trouvé avec ID: {user.id}")
            return await self._to_entity(user)
        except Exception as e:
            logger.error(
                f"Erreur lors de la récupération de l'utilisateur par email {email}: {str(e)}"
            )
            raise RuntimeError(
                f"Erreur lors de la récupération de l'utilisateur par email: {str(e)}"
            )

    async def get_user_by_id(self, user_id: int) -> UserEntity | None:
        """
        Récupérer un utilisateur par son ID
        """
        try:
            logger.debug(f"Recherche d'utilisateur par ID: {user_id}")
            user = await TortoiseUser.get(pk=user_id)
            logger.debug(f"Utilisateur trouvé avec email: {user.email}")
            return await self._to_entity(user)
        except DoesNotExist:
            logger.debug(f"Aucun utilisateur trouvé pour l'ID: {user_id}")
            return None
        except Exception as e:
            logger.error(
                f"Erreur lors de la récupération de l'utilisateur par ID {user_id}: {str(e)}"
            )
            raise RuntimeError(
                f"Erreur lors de la récupération de l'utilisateur par ID: {str(e)}"
            )

    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """
        Mettre à jour le mot de passe d'un utilisateur
        """
        try:
            logger.info(
                f"Tentative de mise à jour du mot de passe pour l'utilisateur ID: {user_id}"
            )
            user = await TortoiseUser.filter(id=user_id).first()
            if user:
                user.password = hashed_password
                await user.save()
                logger.info(
                    f"Mot de passe mis à jour avec succès pour l'utilisateur ID: {user_id}"
                )
                return True
            logger.warning(
                f"Utilisateur non trouvé pour la mise à jour du mot de passe, ID: {user_id}"
            )
            return False
        except Exception as e:
            logger.error(
                f"Erreur lors de la mise à jour du mot de passe pour l'utilisateur ID {user_id}: {str(e)}"
            )
            raise RuntimeError(
                f"Erreur lors de la mise à jour du mot de passe: {str(e)}"
            )

    async def delete_user_by_id(self, user_id: int) -> bool:
        """
        Supprimer un utilisateur par son ID
        """
        try:
            logger.info(f"Tentative de suppression de l'utilisateur ID: {user_id}")
            user = await TortoiseUser.filter(id=user_id).first()
            if user:
                await user.delete()
                logger.info(f"Utilisateur supprimé avec succès, ID: {user_id}")
                return True
            logger.warning(f"Utilisateur non trouvé pour la suppression, ID: {user_id}")
            return False
        except Exception as e:
            logger.error(
                f"Erreur lors de la suppression de l'utilisateur ID {user_id}: {str(e)}"
            )
            raise RuntimeError(
                f"Erreur lors de la suppression de l'utilisateur: {str(e)}"
            )

    async def create(self, data: UserEntity) -> UserEntity:
        raise NotImplementedError

    async def get(self, id: UUID | int) -> UserEntity | None:
        raise NotImplementedError

    async def get_all(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[UserEntity]:
        raise NotImplementedError

    async def update(self, id: UUID | int, data: UserEntity) -> UserEntity:
        raise NotImplementedError

    async def delete(self, id: UUID | int) -> bool:
        raise NotImplementedError

    async def filter(
        self, pagination_params: PaginationParams, **kwargs
    ) -> PaginatedResult[UserEntity]:
        raise NotImplementedError

    async def count(self, **kwargs) -> int:
        raise NotImplementedError
