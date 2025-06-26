import pytest
from fastapi import status
from httpx import AsyncClient

from tests.factories import CreateDomainSchemaFactory


@pytest.mark.asyncio
async def test_get_all_domains_success(authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("/api/v1/domains/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)


@pytest.mark.asyncio
async def test_get_all_domains_pagination(authenticated_async_client: AsyncClient):
    # Create some domains for testing pagination
    for i in range(15):
        domain_data = CreateDomainSchemaFactory.build(name=f"domain-{i}")
        await authenticated_async_client.post(
            "/api/v1/domains/", json=domain_data.model_dump()
        )

    # Test first page
    response = await authenticated_async_client.get(
        "/api/v1/domains/?page=1&per_page=10"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 10

    # Test second page
    response = await authenticated_async_client.get(
        "/api/v1/domains/?page=2&per_page=10"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 5


@pytest.mark.asyncio
async def test_get_all_domains_empty(authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("/api/v1/domains/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["items"] == []
