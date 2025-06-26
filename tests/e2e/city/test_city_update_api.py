import pytest
from httpx import AsyncClient

from core.entities.city import CityEntity
from core.entities.region import RegionEntity
from main import container
from presentation.schemas.city import UpdateCitySchema

# Mark all tests in this module as e2e
pytestmark = pytest.mark.e2e


class TestUpdateCity:
    """
    E2E tests for the city update endpoint (/api/v1/cities/{city_id}/).
    """

    city_to_update: CityEntity
    existing_city: CityEntity

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
            RegionEntity(name="Test Region E2E Update")
        )
        assert region.id is not None

        # City for successful update test
        TestUpdateCity.city_to_update = await city_use_case.create(
            CityEntity(name="City to Update", region_id=region.id, created_by=user.id)
        )
        # City for conflict test
        TestUpdateCity.existing_city = await city_use_case.create(
            CityEntity(
                name="Existing City Name", region_id=region.id, created_by=user.id
            )
        )

    class TestSuccess:
        """
        Tests for successful city update scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_update_city_successfully(
            self,
            authenticated_async_client: AsyncClient,
        ):
            """
            Verify that a city can be updated successfully with valid data.
            """
            # Given
            update_data = UpdateCitySchema(name="Updated City Name")

            # When
            response = await authenticated_async_client.put(
                f"/api/v1/cities/{TestUpdateCity.city_to_update.id}/",
                json=update_data.model_dump(),
            )

            # Then
            assert response.status_code == 200, response.text
            response_data = response.json()
            assert response_data["id"] == TestUpdateCity.city_to_update.id
            assert response_data["name"] == update_data.name

            # Verify in database
            city_use_case = container.city_use_case()
            assert TestUpdateCity.city_to_update.id is not None
            updated_city = await city_use_case.get(TestUpdateCity.city_to_update.id)
            assert updated_city.name == update_data.name

    class TestFailures:
        """
        Tests for failed city update scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_return_409_when_name_already_exists(
            self,
            authenticated_async_client: AsyncClient,
        ):
            """
            Verify that updating a city with a name that already exists returns a 409 Conflict error.
            """
            # Given
            update_data = UpdateCitySchema(name=TestUpdateCity.existing_city.name)

            # When
            response = await authenticated_async_client.put(
                f"/api/v1/cities/{TestUpdateCity.city_to_update.id}/",
                json=update_data.model_dump(),
            )

            # Then
            assert response.status_code == 409, response.text
            response_data = response.json()
            assert response_data["code"] == "conflict"

        @pytest.mark.asyncio
        async def test_should_return_404_when_city_not_found(
            self, authenticated_async_client: AsyncClient
        ):
            """
            Verify that updating a non-existent city returns a 404 Not Found error.
            """
            # Given
            non_existent_city_id = 99999
            update_data = UpdateCitySchema(name="Any Name")

            # When
            response = await authenticated_async_client.put(
                f"/api/v1/cities/{non_existent_city_id}/",
                json=update_data.model_dump(),
            )

            # Then
            assert response.status_code == 404, response.text
            response_data = response.json()
            assert response_data["code"] == "not_found"

        @pytest.mark.asyncio
        async def test_should_return_401_for_unauthenticated_user(
            self, async_client: AsyncClient
        ):
            """
            Verify that an unauthenticated user cannot update a city.
            """
            # Given
            city_id = 1
            update_data = {"name": "Any Name"}

            # When
            response = await async_client.put(
                f"/api/v1/cities/{city_id}/", json=update_data
            )

            # Then
            assert response.status_code == 401, response.text
            assert response.json()["detail"] == "Not authenticated"
