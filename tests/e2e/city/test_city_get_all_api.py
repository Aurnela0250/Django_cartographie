import pytest
from fastapi.testclient import TestClient

from core.entities.city import CityEntity
from core.entities.region import RegionEntity
from main import container
from tests.e2e.conftest import get_authenticated_user_token

# Mark all tests in this module as e2e
pytestmark = pytest.mark.e2e


class TestGetAllCities:
    """
    E2E tests for the city listing endpoint (/api/v1/cities/).
    """

    @pytest.fixture(autouse=True)
    @pytest.mark.asyncio
    async def setup_method(self, client: TestClient):
        """
        Setup test data before each test method.
        """
        token = await get_authenticated_user_token(client)
        region_use_case = container.region_use_case()
        city_use_case = container.city_use_case()
        user_use_case = container.auth_use_case()
        user = await user_use_case.auth_repository.get_user_by_email("test@example.com")
        assert user is not None

        region = await region_use_case.create(
            RegionEntity(name="Test Region E2E GetAll")
        )
        assert region.id is not None
        for i in range(15):
            await city_use_case.create(
                CityEntity(name=f"City {i}", region_id=region.id, created_by=user.id)
            )

    def teardown_method(self):
        """
        Reset container after each test.
        """
        container.reset_override()

    class TestSuccess:
        """
        Tests for successful city listing scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_get_all_cities_paginated(
            self,
            client: TestClient,
        ):
            """
            Verify that cities can be listed with pagination.
            """
            # Given
            token = await get_authenticated_user_token(client)
            headers = {"Authorization": f"Bearer {token}"}
            params = {"page": 2, "per_page": 5}

            # When
            response = client.get("/api/v1/cities/", headers=headers, params=params)

            # Then
            assert response.status_code == 200, response.text
            response_data = response.json()

            assert response_data["page"] == 2
            assert response_data["per_page"] == 5
            assert response_data["total_items"] >= 15
            assert len(response_data["items"]) == 5
            assert response_data["items"][0]["name"] == "City 5"

    class TestFailures:
        """
        Tests for failed city listing scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_return_401_for_unauthenticated_user(
            self, client: TestClient
        ):
            """
            Verify that an unauthenticated user cannot list cities.
            """
            # When
            response = client.get("/api/v1/cities/")

            # Then
            assert response.status_code == 401, response.text
            assert response.json()["detail"] == "Not authenticated"
