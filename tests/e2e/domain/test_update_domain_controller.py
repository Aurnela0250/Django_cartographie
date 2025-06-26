import pytest
from fastapi import status
from httpx import AsyncClient

from tests.factories import (
    CreateDomainSchemaFactory,
    UpdateDomainSchemaFactory,
)

pytestmark = pytest.mark.e2e


async def test_update_domain_success(
    authenticated_async_client: AsyncClient,
):
    """
    Test de mise à jour réussie d'un domaine.
    Vérifie que le statut est 200 et que les données sont mises à jour.
    """
    # Créer un domaine pour le test
    domain_data = CreateDomainSchemaFactory.build()
    create_response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain_data.model_dump(mode="json"),
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    domain_id = create_response.json()["id"]

    # Préparer les nouvelles données pour la mise à jour
    update_data = UpdateDomainSchemaFactory.build()

    # Effectuer la mise à jour
    response = await authenticated_async_client.put(
        f"/api/v1/domains/{domain_id}/",
        json=update_data.model_dump(mode="json"),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["name"] == update_data.name


async def test_update_domain_conflict(
    authenticated_async_client: AsyncClient,
):
    """
    Test de mise à jour d'un domaine avec un nom existant.
    Vérifie que le statut est 409 et que le code d'erreur est 'conflict'.
    """
    # Créer deux domaines
    domain1_data = CreateDomainSchemaFactory.build(name="Domain 1")
    domain2_data = CreateDomainSchemaFactory.build(name="Domain 2")

    create_response1 = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain1_data.model_dump(mode="json"),
    )
    assert create_response1.status_code == status.HTTP_201_CREATED
    domain1_id = create_response1.json()["id"]

    create_response2 = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain2_data.model_dump(mode="json"),
    )
    assert create_response2.status_code == status.HTTP_201_CREATED

    # Essayer de mettre à jour domain1 avec le nom de domain2
    update_data = UpdateDomainSchemaFactory.build(name="Domain 2")
    response = await authenticated_async_client.put(
        f"/api/v1/domains/{domain1_id}/",
        json=update_data.model_dump(mode="json"),
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    response_data = response.json()
    assert response_data["code"] == "conflict"


async def test_update_domain_not_found(
    authenticated_async_client: AsyncClient,
):
    """
    Test de mise à jour d'un domaine inexistant.
    Vérifie que le statut est 404 et que le code d'erreur est 'not_found'.
    """
    update_data = UpdateDomainSchemaFactory.build()
    response = await authenticated_async_client.put(
        "/api/v1/domains/99999/",
        json=update_data.model_dump(mode="json"),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data["code"] == "not_found"


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {"name": 123},
        {"name": "a" * 101},
    ],
)
async def test_update_domain_validation_error(
    authenticated_async_client: AsyncClient,
    invalid_payload: dict,
):
    """
    Test de mise à jour d'un domaine avec des données invalides.
    Vérifie que le statut est 422.
    """
    # Créer un domaine pour le test
    domain_data = CreateDomainSchemaFactory.build()
    create_response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json=domain_data.model_dump(mode="json"),
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    domain_id = create_response.json()["id"]

    # Essayer de mettre à jour avec des données invalides
    response = await authenticated_async_client.put(
        f"/api/v1/domains/{domain_id}/",
        json=invalid_payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
