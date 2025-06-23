import pytest
from fastapi.testclient import TestClient

from core.entities.city import CityEntity
from core.entities.region import RegionEntity
from main import container
from tests.e2e.conftest import get_authenticated_user_token

# Mark all tests in this module as e2e
pytestmark = pytest.mark.e2e


class TestGetCity:
    """
    E2E tests for the city retrieval endpoint (/api/v1/cities/{city_id}/).
    """

    city_to_get: CityEntity

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

        region = await region_use_case.create(RegionEntity(name="Test Region E2E Get"))
        assert region.id is not None
        TestGetCity.city_to_get = await city_use_case.create(
            CityEntity(name="City To Get", region_id=region.id, created_by=user.id)
        )

    def teardown_method(self):
        """
        Reset container after each test.
        """
        container.reset_override()

    class TestSuccess:
        """
        Tests for successful city retrieval scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_get_city_successfully(
            self,
            client: TestClient,
        ):
            """
            Verify that a city can be retrieved successfully by its ID.
            """
            # Given
            token = await get_authenticated_user_token(client)
            headers = {"Authorization": f"Bearer {token}"}

            # When
            response = client.get(
                f"/api/v1/cities/{TestGetCity.city_to_get.id}/",
                headers=headers,
            )

            # Then
            assert response.status_code == 200, response.text
            response_data = response.json()
            assert response_data["id"] == TestGetCity.city_to_get.id
            assert response_data["name"] == TestGetCity.city_to_get.name
            assert response_data["region_id"] == TestGetCity.city_to_get.region_id

    class TestFailures:
        """
        Tests for failed city retrieval scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_return_404_when_city_not_found(self, client: TestClient):
            """
            Verify that a 404 Not Found error is returned for a non-existent city ID.
            """
            # Given
            token = await get_authenticated_user_token(client)
            non_existent_city_id = 99999
            headers = {"Authorization": f"Bearer {token}"}

            # When
            response = client.get(
                f"/api/v1/cities/{non_existent_city_id}/",
                headers=headers,
            )

            # Then
            assert response.status_code == 404, response.text
            response_data = response.json()
            assert response_data["code"] == "city:not_found"
            assert "not found" in response_data["message"]

        @pytest.mark.asyncio
        async def test_should_return_401_for_unauthenticated_user(
            self, client: TestClient
        ):
            """
            Verify that an unauthenticated user cannot retrieve a city.
            """
            # Given
            city_id = 1

            # When
            response = client.get(f"/api/v1/cities/{city_id}/")

            # Then
            assert response.status_code == 401, response.text
            assert response.json()["detail"] == "Not authenticated"
