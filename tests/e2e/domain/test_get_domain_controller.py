import pytest
from httpx import AsyncClient

from tests.factories import DomainEntityFactory


@pytest.mark.asyncio
async def test_get_domain_success(
    authenticated_async_client: AsyncClient,
):
    # Create a domain for testing
    domain_data = DomainEntityFactory.build()
    response = await authenticated_async_client.post(
        "/api/v1/domains/",
        json={"name": domain_data.name},
    )
    domain_id = response.json()["id"]

    # Test the GET endpoint
    response = await authenticated_async_client.get(
        f"/api/v1/domains/{domain_id}/",
    )
    assert response.status_code == 200
    assert response.json()["name"] == domain_data.name


@pytest.mark.asyncio
async def test_get_domain_not_found(
    authenticated_async_client: AsyncClient,
):
    # Test with a non-existent domain ID
    response = await authenticated_async_client.get(
        "/api/v1/domains/99999/",
    )
    assert response.status_code == 404
    assert response.json()["code"] == "not_found"


@pytest.mark.asyncio
async def test_get_domain_invalid_id(
    authenticated_async_client: AsyncClient,
):
    # Test with an invalid domain ID (e.g., string instead of integer)
    response = await authenticated_async_client.get(
        "/api/v1/domains/invalid_id/",
    )
    assert response.status_code == 422
