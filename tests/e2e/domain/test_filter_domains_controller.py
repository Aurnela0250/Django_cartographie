import uuid
from typing import Optional

import pytest
from fastapi import status
from httpx import AsyncClient

from core.entities.filters import DomainFilters
from tests.factories import CreateDomainSchemaFactory

pytestmark = pytest.mark.e2e


@pytest.fixture(autouse=True)
async def cleanup_domains(authenticated_async_client: AsyncClient):
    # Supprime tous les domaines avant chaque test pour éviter les conflits de nom
    resp = await authenticated_async_client.get("/api/v1/domains/")
    if resp.status_code == 200:
        data = resp.json()
        items = data["items"] if isinstance(data, dict) and "items" in data else data
        for domain in items:
            await authenticated_async_client.delete(f"/api/v1/domains/{domain['id']}/")


def unique_name(base: str) -> str:
    return f"{base}_{uuid.uuid4().hex[:8]}"


ENDPOINT = "/api/v1/domains/filter/"


async def create_domain(
    client: AsyncClient,
    name: str,
):
    data = CreateDomainSchemaFactory.build(name=name)
    response = await client.post(
        "/api/v1/domains/",
        json=data.model_dump(mode="json"),
    )
    if response.status_code == status.HTTP_201_CREATED:
        return response.json()
    elif response.status_code == status.HTTP_409_CONFLICT:
        # Domaine déjà existant, retourne None ou lève une erreur selon le besoin
        return None
    else:
        raise AssertionError(
            f"Erreur inattendue lors de la création du domaine: {response.status_code} {response.text}"
        )


async def get_filter(
    client: AsyncClient,
    filters: Optional[DomainFilters] = None,
    page: int = 1,
    per_page: int = 10,
):
    params = filters.model_dump(exclude_none=True) if filters else {}
    params.update({"page": page, "per_page": per_page})
    response = await client.get(
        ENDPOINT,
        params=params,
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()


async def test_filter_domains_empty_db(
    authenticated_async_client: AsyncClient,
):
    """
    Vérifie que l'endpoint retourne une liste vide si aucun domaine n'est présent.
    """
    data = await get_filter(
        authenticated_async_client,
    )
    assert data["items"] == []
    assert data["totalItems"] == 0
    assert data["page"] == 1
    assert data["perPage"] == 10
    assert data["totalPages"] == 0


async def test_filter_domains_by_name(
    authenticated_async_client: AsyncClient,
):
    """
    Crée plusieurs domaines et vérifie le filtrage partiel par nom.
    """
    await create_domain(
        authenticated_async_client,
        unique_name("Informatique"),
    )
    await create_domain(
        authenticated_async_client,
        unique_name("Electronique"),
    )
    await create_domain(
        authenticated_async_client,
        unique_name("Electromécanique"),
    )
    await create_domain(
        authenticated_async_client,
        unique_name("Gestion"),
    )
    # On filtre sur "Electro" pour attraper les deux domaines correspondants
    filters = DomainFilters(name="Electro")
    data = await get_filter(
        authenticated_async_client,
        filters,
    )
    names = [item["name"] for item in data["items"]]
    assert any("Electronique" in n for n in names)
    assert any("Electromécanique" in n for n in names)
    assert data["totalItems"] == 2


async def test_filter_domains_no_match(
    authenticated_async_client: AsyncClient,
):
    """
    Vérifie qu'un filtre qui ne correspond à aucun domaine retourne une liste vide.
    """
    await create_domain(
        authenticated_async_client,
        unique_name("Informatique"),
    )
    await create_domain(
        authenticated_async_client,
        unique_name("Electronique"),
    )
    filters = DomainFilters(name="Biologie")
    data = await get_filter(
        authenticated_async_client,
        filters,
    )
    assert data["items"] == []
    assert data["totalItems"] == 0


async def test_filter_domains_pagination(
    authenticated_async_client: AsyncClient,
):
    """
    Vérifie que la pagination fonctionne correctement avec un filtre.
    """
    noms = [
        unique_name("Electronique"),
        unique_name("Electromécanique"),
        unique_name("Electrostatique"),
        unique_name("Electrolyse"),
    ]
    for nom in noms:
        await create_domain(
            authenticated_async_client,
            nom,
        )
    filters = DomainFilters(name="Electro")
    # page 1, per_page 2
    data1 = await get_filter(
        authenticated_async_client,
        filters,
        page=1,
        per_page=2,
    )
    assert len(data1["items"]) == 2
    assert data1["totalItems"] == 4
    assert data1["page"] == 1
    assert data1["perPage"] == 2
    assert data1["totalPages"] == 2
    # page 2, per_page 2
    data2 = await get_filter(
        authenticated_async_client,
        filters,
        page=2,
        per_page=2,
    )
    assert len(data2["items"]) == 2
    assert data2["totalItems"] == 4
    assert data2["page"] == 2
    assert data2["perPage"] == 2
    assert data2["totalPages"] == 2
