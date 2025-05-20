import redis
from django.conf import settings


class RedisService:
    """
    Service pour interagir avec Redis - implémente un pattern Singleton.
    """

    _instance = None
    _redis_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisService, cls).__new__(cls)
            # Connexion à Redis en utilisant les paramètres depuis settings
            cls._redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True,
            )
        return cls._instance

    @classmethod
    def get_client(cls):
        """
        Retourne le client Redis.
        """
        if cls._redis_client is None:
            cls()
        return cls._redis_client

    @classmethod
    def set(cls, key: str, value: str, exp: int = None) -> bool:
        """
        Définit une valeur dans Redis avec une expiration optionnelle.
        """
        return cls.get_client().set(key, value, ex=exp)

    @classmethod
    def get(cls, key: str) -> str:
        """
        Récupère une valeur depuis Redis.
        """
        return cls.get_client().get(key)

    @classmethod
    def exists(cls, key: str) -> bool:
        """
        Vérifie si une clé existe dans Redis.
        """
        return bool(cls.get_client().exists(key))

    @classmethod
    def delete(cls, key: str) -> int:
        """
        Supprime une clé de Redis.
        """
        return cls.get_client().delete(key)
