from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from tortoise import Tortoise

from core.entities.user import UserEntity


@pytest.fixture
def sample_user():
    """Utilisateur de test - fixture globale"""
    return UserEntity(
        id=1,
        email="test@example.com",
        password="hashed_password",
        created_at=datetime.now(ZoneInfo("UTC")),
        updated_at=datetime.now(ZoneInfo("UTC")),
    )


@pytest.fixture(scope="function", autouse=True)
async def initialize_db():
    """
    Initialise la base de données pour les tests.
    """
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={
            "models": [
                "apps.tortoise.user",
                "apps.tortoise.region",
                "apps.tortoise.city",
                "apps.tortoise.establishment_type",
                "apps.tortoise.establishment",
                "apps.tortoise.domain",
                "apps.tortoise.level",
                "apps.tortoise.mention",
                "apps.tortoise.rate",
                "apps.tortoise.formation_authorization",
                "apps.tortoise.formation",
                "apps.tortoise.annual_headcount",
            ]
        },
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
