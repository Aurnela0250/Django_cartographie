import pytest
from httpx import AsyncClient

from core.entities.city import CityEntity
from core.entities.region import RegionEntity
from main import container
from presentation.exceptions import NotFoundException

# Mark all tests in this module as e2e
pytestmark = pytest.mark.e2e


class TestDeleteCity:
    """
    E2E tests for the city deletion endpoint (/api/v1/cities/{city_id}/).
    """

    city_to_delete: CityEntity

    @pytest.fixture(autouse=True)
    @pytest.mark.asyncio
    async def setup_method(self, authenticated_async_client: AsyncClient):
        """
        Setup test data before each test method.
        """
        region_use_case = container.region_use_case()
        city_use_case = container.city_use_case()
        user_use_case = container.auth_use_case()
        user = await user_use_case.auth_repository.get_user_by_email("test@example.com")
        assert user is not None

        region = await region_use_case.create(
            RegionEntity(name="Test Region E2E Delete")
        )
        assert region.id is not None
        TestDeleteCity.city_to_delete = await city_use_case.create(
            CityEntity(name="City to Delete", region_id=region.id, created_by=user.id)
        )

    def teardown_method(self):
        """
        Reset container after each test.
        """
        container.reset_override()

    class TestSuccess:
        """
        Tests for successful city deletion scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_delete_city_successfully(
            self,
            authenticated_async_client: AsyncClient,
        ):
            """
            Verify that a city can be deleted successfully.
            """
            # When
            response = await authenticated_async_client.delete(
                f"/api/v1/cities/{TestDeleteCity.city_to_delete.id}/",
            )

            # Then
            assert response.status_code == 204, response.text

            # Verify in database
            city_use_case = container.city_use_case()
            with pytest.raises(NotFoundException):
                assert TestDeleteCity.city_to_delete.id is not None
                await city_use_case.get(TestDeleteCity.city_to_delete.id)

    class TestFailures:
        """
        Tests for failed city deletion scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_return_404_when_city_not_found(
            self, authenticated_async_client: AsyncClient
        ):
            """
            Verify that deleting a non-existent city returns a 404 Not Found error.
            """
            # Given
            non_existent_city_id = 99999

            # When
            response = await authenticated_async_client.delete(
                f"/api/v1/cities/{non_existent_city_id}/",
            )

            # Then
            assert response.status_code == 404, response.text
            response_data = response.json()
            assert response_data["code"] == "city:not_found"

        @pytest.mark.asyncio
        async def test_should_return_401_for_unauthenticated_user(
            self, async_client: AsyncClient
        ):
            """
            Verify that an unauthenticated user cannot delete a city.
            """
            # Given
            city_id = 1

            # When
            response = await async_client.delete(f"/api/v1/cities/{city_id}/")

            # Then
            assert response.status_code == 401, response.text
            assert response.json()["detail"] == "Not authenticated"
