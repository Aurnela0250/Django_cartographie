import pytest
from fastapi.testclient import TestClient

from core.entities.city import CityEntity
from core.entities.region import RegionEntity
from main import container
from tests.e2e.conftest import get_authenticated_user_token

# Mark all tests in this module as e2e
pytestmark = pytest.mark.e2e


class TestFilterCities:
    """
    E2E tests for the city filtering endpoint (/api/v1/cities/filter/).
    """

    region1_id: int
    region2_id: int

    @pytest.fixture(autouse=True)
    @pytest.mark.asyncio
    async def setup_and_teardown(self, client: TestClient):
        """
        Set up data for tests and reset container afterwards.
        """
        # Setup: Create the user first to ensure it exists.
        await get_authenticated_user_token(client)

        auth_use_case = container.auth_use_case()
        user = await auth_use_case.auth_repository.get_user_by_email("test@example.com")
        assert user is not None

        # Create other necessary entities
        region_use_case = container.region_use_case()
        city_use_case = container.city_use_case()

        region1 = await region_use_case.create(RegionEntity(name="Filter Region A"))
        assert region1.id is not None
        TestFilterCities.region1_id = region1.id

        region2 = await region_use_case.create(RegionEntity(name="Filter Region B"))
        assert region2.id is not None
        TestFilterCities.region2_id = region2.id

        await city_use_case.create(
            CityEntity(name="Paris", region_id=region1.id, created_by=user.id)
        )
        await city_use_case.create(
            CityEntity(name="Lyon", region_id=region1.id, created_by=user.id)
        )
        await city_use_case.create(
            CityEntity(name="Marseille", region_id=region2.id, created_by=user.id)
        )
        await city_use_case.create(
            CityEntity(name="Lille", region_id=region2.id, created_by=user.id)
        )

        yield  # This is where the test runs

        # Teardown: Reset container to a clean state
        container.reset_override()

    class TestSuccess:
        """
        Tests for successful city filtering scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_filter_by_name(self, client: TestClient):
            """
            Verify that cities can be filtered by name.
            """
            # Given
            token = await get_authenticated_user_token(client)
            headers = {"Authorization": f"Bearer {token}"}
            params = {"name": "Pa"}  # Partial name search

            # When
            response = client.get(
                "/api/v1/cities/filter/?name=Pa", headers=headers, params=params
            )

            # Then
            assert response.status_code == 200, response.text
            response_data = response.json()
            print("Response data :", response_data)
            assert response_data["totalItems"] == 0
            assert response_data["items"][0]["name"] == "Paris"
            assert "nextPage" in response_data
            assert "previousPage" in response_data

        @pytest.mark.asyncio
        async def test_should_filter_by_region_id(self, client: TestClient):
            """
            Verify that cities can be filtered by region ID.
            """
            # Given
            token = await get_authenticated_user_token(client)
            headers = {"Authorization": f"Bearer {token}"}
            params = {"region_id": TestFilterCities.region2_id}

            # When
            response = client.get(
                "/api/v1/cities/filter/", headers=headers, params=params
            )

            # Then
            assert response.status_code == 200, response.text
            response_data = response.json()
            assert response_data["totalItems"] == 2
            item_names = {item["name"] for item in response_data["items"]}
            assert item_names == {"Marseille", "Lille"}
            assert "nextPage" in response_data
            assert "previousPage" in response_data

        @pytest.mark.asyncio
        async def test_should_filter_by_name_and_region(self, client: TestClient):
            """
            Verify that cities can be filtered by both name and region ID.
            """
            # Given
            token = await get_authenticated_user_token(client)
            headers = {"Authorization": f"Bearer {token}"}
            params = {"name": "L", "region_id": TestFilterCities.region1_id}

            # When
            response = client.get(
                "/api/v1/cities/filter/", headers=headers, params=params
            )

            # Then
            assert response.status_code == 200, response.text
            response_data = response.json()
            assert response_data["totalItems"] == 1
            assert response_data["items"][0]["name"] == "Lyon"
            assert "nextPage" in response_data
            assert "previousPage" in response_data

    class TestFailures:
        """
        Tests for failed city filtering scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_return_401_for_unauthenticated_user(
            self, client: TestClient
        ):
            """
            Verify that an unauthenticated user cannot filter cities.
            """
            # When
            response = client.get("/api/v1/cities/filter/")

            # Then
            assert response.status_code == 401, response.text
            response_data = response.json()
            assert response_data["code"] == "unauthorized"
            assert response_data["message"] == "Not authenticated"
