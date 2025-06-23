import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from tortoise import Tortoise

from config.settings import TORTOISE_ORM_TEST
from config.tortoise_init import close_tortoise, init_tortoise
from main import app, container
from presentation.exceptions import ConflictException


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_tests():
    """
    Initialise la base de données de test avant de lancer les tests
    et la nettoie après.
    """
    await init_tortoise(TORTOISE_ORM_TEST)
    await Tortoise.generate_schemas()
    yield
    await close_tortoise()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db(initialize_tests):
    """
    Nettoie la base de données après chaque test.
    """
    yield
    models = Tortoise.apps.get("models")
    if models:
        for model in models.values():
            await model.all().delete()


@pytest.fixture(scope="function")
def client():
    """
    Test client for the E2E tests.
    We don't use `with TestClient(app) as c:` to avoid running the app's
    lifespan manager, which conflicts with our test DB setup.
    """
    yield TestClient(app)


async def get_authenticated_user_token(client: TestClient) -> str:
    """
    Create a user and return an authentication token.
    """
    auth_use_case = container.auth_use_case()
    try:
        await auth_use_case.signup("test@example.com", "password123")
    except ConflictException:
        # User already exists, which is fine for our test setup.
        pass
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    return response.json()["accessToken"]
