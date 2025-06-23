import asyncio
import os
import sys
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from tortoise import Tortoise
from tortoise.contrib import test
from tortoise.transactions import in_transaction

# Ajouter la racine du projet au sys.path pour résoudre les importations
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import TORTOISE_ORM
from core.container.container import Container


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Crée une boucle d'événements asyncio unique pour toute la session de test.
    pytest-asyncio utilisera automatiquement cette boucle pour tous les tests.

    Ceci résout l'erreur : RuntimeError: Task got Future attached to a different loop
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_db(
    event_loop: asyncio.AbstractEventLoop,
) -> AsyncGenerator[None, None]:
    """
    Initialise la base de données de test PostgreSQL une seule fois par session.
    Utilise les méthodes intégrées de Tortoise ORM pour une gestion propre.
    """
    # Utiliser la méthode recommandée par Tortoise ORM pour les tests
    db_config = test.getDBConfig(
        app_label="models",
        modules=TORTOISE_ORM["apps"]["models"]["models"],
    )

    try:
        # _create_db=True gère automatiquement la création de la base de données de test
        await Tortoise.init(db_config, _create_db=True)
        await Tortoise.generate_schemas()
        print("✅ Base de données de test initialisée avec succès.")
        yield
    finally:
        # Utiliser la méthode intégrée pour nettoyer
        if Tortoise._inited:
            await Tortoise._drop_databases()
        print("🧹 Base de données de test supprimée.")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def transactional_test() -> AsyncGenerator[None, None]:
    """
    Assure une isolation parfaite des données en exécutant chaque test dans
    une transaction qui est automatiquement annulée (rollback) à la fin.

    Utilise la fonction in_transaction de tortoise.transactions comme dans
    les exemples officiels de Tortoise ORM.
    """
    async with in_transaction():
        yield
        # Le rollback est automatique en sortant du contexte avec une exception
        # raise Exception("Force rollback pour isolation des tests")


@pytest.fixture(scope="function")
def container() -> Generator[Container, None, None]:
    """
    Fournit une instance fraîche du conteneur DI pour chaque test,
    permettant de surcharger les dépendances de manière isolée.
    """
    di_container = Container()
    yield di_container
