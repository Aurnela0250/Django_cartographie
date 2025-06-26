import pytest
from httpx import AsyncClient

from core.entities.city import CityEntity
from core.entities.region import RegionEntity
from main import container
from presentation.constants import errors_code
from presentation.schemas.city import CreateCitySchema

# Mark all tests in this module as e2e
pytestmark = pytest.mark.e2e


class TestCreateCity:
    """
    E2E tests for city creation endpoint (/api/v1/cities/).
    """

    region_id: int

    @pytest.fixture(autouse=True)
    @pytest.mark.asyncio
    async def setup_method(self):
        """
        Setup test data before each test method.
        """
        # Create a region to be used by the tests and attach to the class
        region_use_case = container.region_use_case()
        region = await region_use_case.create(
            RegionEntity(name="Test Region For Create")
        )
        assert region.id is not None
        TestCreateCity.region_id = region.id

    @classmethod
    def teardown_class(cls):
        """
        Reset container after all tests in this class.
        """
        container.reset_override()

    class TestSuccess:
        """
        Tests for successful city creation scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_create_city_successfully(
            self,
            authenticated_async_client: AsyncClient,
        ):
            """
            Verify that a city can be created successfully with valid data.
            """
            # Given
            city_data = CreateCitySchema(
                name="New E2E City", region_id=TestCreateCity.region_id
            )

            # When
            response = await authenticated_async_client.post(
                "/api/v1/cities/",
                json=city_data.model_dump(),
            )

            # Then
            assert response.status_code == 201, response.text
            response_data = response.json()
            assert response_data["name"] == city_data.name
            assert response_data["regionId"] == city_data.region_id
            assert "id" in response_data

            # Verify in database
            city_use_case = container.city_use_case()
            created_city = await city_use_case.get(response_data["id"])
            assert created_city is not None
            assert created_city.name == city_data.name

    class TestFailures:
        """
        Tests for failed city creation scenarios.
        """

        @pytest.mark.asyncio
        async def test_should_return_409_when_city_already_exists(
            self,
            authenticated_async_client: AsyncClient,
        ):
            """
            Verify that creating a city with a name that already exists returns a 409 Conflict error.
            """
            # Given
            # 1. Create an existing city
            city_use_case = container.city_use_case()
            user_use_case = container.auth_use_case()
            user = await user_use_case.auth_repository.get_user_by_email(
                "test@example.com"
            )
            assert user is not None

            existing_city = await city_use_case.create(
                CityEntity(
                    name="Existing E2E City",
                    region_id=TestCreateCity.region_id,
                    created_by=user.id,
                )
            )

            # 2. Prepare data with the same name
            city_data = CreateCitySchema(
                name=existing_city.name,
                region_id=TestCreateCity.region_id,
            )

            # When
            response = await authenticated_async_client.post(
                "/api/v1/cities/",
                json=city_data.model_dump(),
            )

            # Then
            assert response.status_code == 409, response.text
            response_data = response.json()
            assert response_data["code"] == errors_code.CONFLICT
            assert "already exists" in response_data["message"]

        @pytest.mark.asyncio
        async def test_should_return_422_for_invalid_payload(
            self, authenticated_async_client: AsyncClient
        ):
            """
            Verify that an invalid payload returns a 422 Unprocessable Entity error.
            """
            # Given
            invalid_data = {"name": "Test"}  # Missing region_id

            # When
            response = await authenticated_async_client.post(
                "/api/v1/cities/",
                json=invalid_data,
            )

            # Then
            assert response.status_code == 422, response.text
            response_data = response.json()
            assert response_data["code"] == errors_code.UNPROCESSABLE_ENTITY
            assert any(
                "regionId" in detail["field"] for detail in response_data["details"]
            )

        @pytest.mark.asyncio
        async def test_should_return_401_for_unauthenticated_user(
            self, async_client: AsyncClient
        ):
            """
            Verify that an unauthenticated user cannot create a city.
            """
            # Given
            city_data = {"name": "Any City", "region_id": 999}

            # When
            response = await async_client.post("/api/v1/cities/", json=city_data)

            # Then
            assert response.status_code == 401, response.text
            assert response.json()["detail"] == "Not authenticated"
