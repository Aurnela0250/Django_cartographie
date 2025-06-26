import pytest
from httpx import AsyncClient

from tests.factories import CreateDomainSchemaFactory

pytestmark = pytest.mark.e2e


async def test_create_domain_success(
    authenticated_async_client: AsyncClient,
):
    """
    Test de création réussie d'un domaine.
    Vérifie que le statut est 201 et que l'ID est un entier.
    """
    domain_data = CreateDomainSchemaFactory.build()
    response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain_data.model_dump(),
    )

    assert response.status_code == 201
    response_data = response.json()
    assert isinstance(response_data["id"], int)
    assert response_data["name"] == domain_data.name


async def test_create_domain_conflict(
    authenticated_async_client: AsyncClient,
):
    """
    Test de création d'un domaine avec un nom existant.
    Vérifie que le statut est 409 et que le code d'erreur est 'conflict'.
    """
    # 1. Créer un premier domaine
    domain_data = CreateDomainSchemaFactory.build()
    response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain_data.model_dump(),
    )
    assert response.status_code == 201

    # 2. Tenter de créer un domaine avec le même nom
    response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain_data.model_dump(),
    )

    assert response.status_code == 409
    response_data = response.json()
    assert response_data["code"] == "conflict"


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {"description": "sans nom"},
        {"name": 123},
        {"name": "a" * 101},
    ],
)
async def test_create_domain_validation_error(
    authenticated_async_client: AsyncClient,
    invalid_payload: dict,
):
    """
    Test de création d'un domaine avec des données invalides.
    Vérifie que le statut est 422.
    """
    response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=invalid_payload,
    )

    assert response.status_code == 422
