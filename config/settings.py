"""
FastAPI settings for OrientationMada project.


"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv(os.path.join(Path(__file__).resolve().parent.parent, ".env"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Tortoise ORM Configuration
DB_USER = os.getenv("DB_USERNAME", "cartographie")
DB_PASS = os.getenv("DB_PASSWORD", "123456")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "cartographie_db")

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": DB_HOST,
                "port": DB_PORT,
                "user": DB_USER,
                "password": DB_PASS,
                "database": DB_NAME,
            },
        }
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "apps.tortoise.annual_headcount.models",
                "apps.tortoise.city.models",
                "apps.tortoise.domain.models",
                "apps.tortoise.establishment.models",
                "apps.tortoise.establishment_type.models",
                "apps.tortoise.formation.models",
                "apps.tortoise.formation_authorization.models",
                "apps.tortoise.level.models",
                "apps.tortoise.mention.models",
                "apps.tortoise.rate.models",
                "apps.tortoise.region.models",
                "apps.tortoise.user.models",
            ],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC",
}

db_url_test = (
    f"asyncpg://{DB_USER}:" f"{DB_PASS}@" f"{DB_HOST}:" f"{DB_PORT}/" f"{DB_NAME}_test"
)

TORTOISE_ORM_TEST = {
    "connections": {"default": db_url_test},
    "apps": {
        "models": {
            "models": TORTOISE_ORM["apps"]["models"]["models"],
            "default_connection": "default",
        },
    },
}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "fastapi-insecure-0b%4yfbe^i8=td=3hydac=5mepdh@$)d(j%wok36hfj%6tperv"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "*",
    "localhost",
    "127.0.0.1",
]

# OpenFGA Configuration
OPENFGA_API_SCHEME = "http"  # ou "https" en production
FGA_API_URL = "http://localhost:8080"  # Remplacez par l'URL de votre serveur OpenFGA
FGA_STORE_ID = "01JAHE1QQ9QF6B7D6GB9E3PCWQ"  # L'ID de votre store OpenFGA
FGA_MODEL_ID = "01JAJX1KK3YYGC4EXB0P0BZW4G"

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


# Application definition


# Database


# Password validation


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type

# Assurez-vous que le dossier logs existe
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_DIR, "debug.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "presentation": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "core": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


# JWT configuration
JWT_ISSUER = os.getenv("JWT_ISSUER", "lemon-app")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "lemon-users")
JWT_ALGORITHM = "RS256"

# Durée de vie des tokens
ACCESS_TOKEN_LIFETIME = timedelta(hours=2)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)

# Charger les clés depuis les fichiers
KEYS_DIR = BASE_DIR / "keys"

try:
    with open(KEYS_DIR / "jwt_access_private.pem", "r") as f:
        JWT_ACCESS_PRIVATE_KEY = f.read()

    with open(KEYS_DIR / "jwt_access_public.pem", "r") as f:
        JWT_ACCESS_PUBLIC_KEY = f.read()

    with open(KEYS_DIR / "jwt_refresh_private.pem", "r") as f:
        JWT_REFRESH_PRIVATE_KEY = f.read()

    with open(KEYS_DIR / "jwt_refresh_public.pem", "r") as f:
        JWT_REFRESH_PUBLIC_KEY = f.read()
except FileNotFoundError:
    # Messages d'erreur pour alerter que les clés sont manquantes
    print("ERREUR: Fichiers de clés JWT non trouvés dans le dossier 'keys/'")
    print("Veuillez exécuter les commandes suivantes pour générer les clés:")
    print("mkdir -p keys")
    print("openssl genrsa -out keys/jwt_access_private.pem 2048")
    print(
        "openssl rsa -in keys/jwt_access_private.pem -pubout -out keys/jwt_access_public.pem"
    )
    print("openssl genrsa -out keys/jwt_refresh_private.pem 2048")
    print(
        "openssl rsa -in keys/jwt_refresh_private.pem -pubout -out keys/jwt_refresh_public.pem"
    )

    # Valeurs fictives pour le développement - NE PAS UTILISER EN PRODUCTION
    JWT_ACCESS_PRIVATE_KEY = JWT_REFRESH_PRIVATE_KEY = JWT_ACCESS_PUBLIC_KEY = (
        JWT_REFRESH_PUBLIC_KEY
    ) = "invalid"


# Bcrypt configuration
BCRYPT_ROUNDS = int(
    os.getenv("BCRYPT_ROUNDS", "12")
)  # Nombre de rounds pour le hachage bcrypt
BCRYPT_LOG_ROUNDS = int(
    os.getenv("BCRYPT_LOG_ROUNDS", "12")
)  # Alternative pour la compatibilité


INCLUDE_STACK_TRACE_IN_RESPONSE = (
    os.getenv("INCLUDE_STACK_TRACE_IN_RESPONSE", "False") == "True"
)
LOG_CRITICAL_STACK_TRACE = os.getenv("LOG_CRITICAL_STACK_TRACE", "True") == "True"
