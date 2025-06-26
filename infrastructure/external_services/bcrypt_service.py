import asyncio

from passlib.context import CryptContext

from presentation.exceptions import (
    BcryptHashPasswordException,
    BcryptVerifyPasswordException,
)


class BcryptService:
    """
    Service pour le hachage et la vérification des mots de passe avec bcrypt.
    """

    def __init__(self):
        """
        Initialise le service bcrypt avec la configuration depuis settings.
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def hash_password(self, password: str) -> str:
        """
        Hache un mot de passe avec bcrypt de manière asynchrone.

        Args:
            password: Le mot de passe en clair à hacher

        Returns:
            Le mot de passe haché en format string

        Raises:
            ValueError: Si le mot de passe est vide
            Exception: Pour toute autre erreur de hachage
        """
        try:

            # Exécuter le hachage de manière asynchrone avec asyncio.to_thread
            hashed = await asyncio.to_thread(lambda: self.pwd_context.hash(password))

            # Retourner le hash en string
            return hashed

        except Exception as e:
            raise BcryptHashPasswordException(
                f"Erreur lors du hachage du mot de passe: {str(e)}"
            )

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Vérifie si un mot de passe correspond à son hash de manière asynchrone.

        Args:
            password: Le mot de passe en clair à vérifier
            hashed_password: Le mot de passe haché stocké

        Returns:
            True si le mot de passe correspond, False sinon

        Raises:
            Exception: Pour toute erreur de vérification
        """
        try:

            # Exécuter la vérification de manière asynchrone avec asyncio.to_thread
            return await asyncio.to_thread(
                self.pwd_context.verify,
                password,
                hashed_password,
            )

        except Exception as e:
            raise BcryptVerifyPasswordException(
                f"Erreur lors de la vérification du mot de passe: {str(e)}"
            )
