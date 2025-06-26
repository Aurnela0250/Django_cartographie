import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator
from unittest.mock import patch

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tortoise import Tortoise
from tortoise.contrib import test

# from tortoise.transactions import in_transaction

# Ajouter la racine du projet au sys.path pour résoudre les importations
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import TORTOISE_ORM
from core.container.container import Container
from main import container as main_container
from presentation.exceptions import ConflictException

# Configuration globale des logs pour les tests
logging.getLogger("tortoise").setLevel(logging.WARNING)
logging.getLogger("aiosqlite").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("  httpx:_client").setLevel(logging.WARNING)


# ====== FIXTURES DE BASE (PYTEST, LOOP, DB) ======
@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Crée une boucle d'événements asyncio pour chaque test."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def initialize_db(
    event_loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[None, None]:
    """Initialise la base de données de test pour chaque fonction de test."""
    db_config = test.getDBConfig(
        app_label="models",
        modules=TORTOISE_ORM["apps"]["models"]["models"],
    )
    try:
        await Tortoise.init(db_config, _create_db=True, use_tz=False)
        await Tortoise.generate_schemas()
        print("✅ Base de données de test initialisée.")
        yield
    finally:
        if Tortoise._inited:
            await Tortoise._drop_databases()
        print("\n🧹 Base de données de test supprimée.")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db() -> AsyncGenerator[None, None]:
    """Nettoie la base de données après chaque test en supprimant toutes les données de toutes les tables.
    Cela garantit un état propre pour chaque test et aide à prévenir les problèmes de boucle d'événements.
    """
    yield
    for app in Tortoise.apps.values():
        for model in app.values():
            await model.all().delete()
    await Tortoise.close_connections()


# ====== FIXTURES POUR L'INJECTION DE DÉPENDANCES ======
@pytest.fixture(scope="function")
def container() -> Generator[Container, None, None]:
    """Fournit une instance fraîche du conteneur DI pour chaque test."""
    yield main_container


# ====== FIXTURES POUR L'APPLICATION FASTAPI ET LES CLIENTS HTTP ======
@pytest.fixture(scope="function")
def app() -> FastAPI:
    """Crée une instance de l'application FastAPI avec un lifespan mocké."""
    with patch("main.lifespan") as mock_lifespan:

        @asynccontextmanager
        async def mock_lifespan_func(app: FastAPI):
            yield

        mock_lifespan.return_value = mock_lifespan_func
        from main import app as fastapi_app

        return fastapi_app


@pytest.fixture(scope="function")
def client(app: FastAPI) -> TestClient:
    """Crée un TestClient synchrone pour les tests rapides."""
    return TestClient(app)


@pytest_asyncio.fixture(scope="function")
async def async_client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Crée un client HTTP asynchrone pour les tests E2E en mode ASGI."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ====== FIXTURES POUR L'AUTHENTIFICATION ======
@pytest_asyncio.fixture(scope="function")
async def authenticated_user_token(client: TestClient, container: Container) -> str:
    """Crée un utilisateur et retourne un token d'authentification."""
    auth_use_case = container.auth_use_case()
    try:
        await auth_use_case.signup("test@example.com", "password123")
    except ConflictException:
        pass  # L'utilisateur existe déjà, c'est OK pour les tests

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    response.raise_for_status()
    return response.json()["accessToken"]


@pytest_asyncio.fixture(scope="function")
async def authenticated_async_client(
    app: FastAPI,
    authenticated_user_token: str,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Crée un client HTTP asynchrone authentifié."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"Authorization": f"Bearer {authenticated_user_token}"},
    ) as client:
        yield client
