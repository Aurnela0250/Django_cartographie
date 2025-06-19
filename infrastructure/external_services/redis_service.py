import asyncio
from contextlib import asynccontextmanager
from typing import Any, Optional

import redis.asyncio as redis

from config import settings


class RedisService:
    """
    Service pour interagir avec Redis - géré par l'injecteur de dépendances.
    """

    def __init__(self):
        # Connexion à Redis en utilisant les paramètres depuis settings
        self._redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
        )

    async def set(self, key: str, value: Any, exp: Optional[int] = None) -> bool:
        """
        Définit une valeur dans Redis avec une expiration optionnelle.

        Args:
            key: La clé Redis
            value: La valeur à stocker (sera sérialisée automatiquement)
            exp: Temps d'expiration en secondes

        Returns:
            bool: True si l'opération a réussi
        """
        result = await self._redis_client.set(key, value, ex=exp)
        return bool(result)

    async def get(self, key: str) -> Optional[str]:
        """
        Récupère une valeur depuis Redis.

        Args:
            key: La clé Redis

        Returns:
            Optional[str]: La valeur ou None si la clé n'existe pas
        """
        return await self._redis_client.get(key)

    async def exists(self, key: str) -> bool:
        """
        Vérifie si une clé existe dans Redis.

        Args:
            key: La clé à vérifier

        Returns:
            bool: True si la clé existe
        """
        return bool(await self._redis_client.exists(key))

    async def delete(self, key: str) -> int:
        """
        Supprime une clé de Redis.

        Args:
            key: La clé à supprimer

        Returns:
            int: Nombre de clés supprimées
        """
        return await self._redis_client.delete(key)

    async def expire(self, key: str, seconds: int) -> bool:
        """
        Définit un délai d'expiration pour une clé existante.

        Args:
            key: La clé Redis
            seconds: Temps d'expiration en secondes

        Returns:
            bool: True si l'expiration a été définie
        """
        return bool(await self._redis_client.expire(key, seconds))

    async def ttl(self, key: str) -> int:
        """
        Récupère le temps de vie restant d'une clé.

        Args:
            key: La clé Redis

        Returns:
            int: TTL en secondes (-1 si pas d'expiration, -2 si clé inexistante)
        """
        return await self._redis_client.ttl(key)

    async def increment(self, key: str, amount: int = 1) -> int:
        """
        Incrémente une valeur numérique dans Redis.

        Args:
            key: La clé Redis
            amount: Montant de l'incrémentation

        Returns:
            int: Nouvelle valeur après incrémentation
        """
        return await self._redis_client.incrby(key, amount)

    async def set_hash(self, key: str, mapping: dict) -> bool:
        """
        Stocke un hash dans Redis.

        Args:
            key: La clé du hash
            mapping: Dictionnaire à stocker

        Returns:
            bool: True si l'opération a réussi
        """
        result = await asyncio.to_thread(self._redis_client.hset, key, mapping=mapping)
        return bool(result)

    async def get_hash(self, key: str) -> dict:
        """
        Récupère un hash depuis Redis.

        Args:
            key: La clé du hash

        Returns:
            dict: Le hash ou un dictionnaire vide
        """
        result = await asyncio.to_thread(self._redis_client.hgetall, key)
        # Type ignore pour éviter l'erreur de typage avec l'union Awaitable[dict] | dict
        return result  # type: ignore

    async def close(self):
        """
        Ferme la connexion Redis proprement.
        """
        await self._redis_client.aclose()

    async def ping(self) -> bool:
        """
        Teste la connexion Redis.

        Returns:
            bool: True si Redis répond
        """
        try:
            return await self._redis_client.ping()
        except Exception:
            return False

    @asynccontextmanager
    async def pipeline(self):
        """
        Context manager pour les opérations en batch.

        Usage:
            async with redis_service.pipeline() as pipe:
                await pipe.set("key1", "value1")
                await pipe.set("key2", "value2")
                await pipe.execute()
        """
        pipe = self._redis_client.pipeline()
        try:
            yield pipe
        finally:
            await pipe.reset()
