# E2E Test Rules for the Project

## Introduction

This document defines the rules and conventions for writing end-to-end (E2E) tests in this project. These rules are intended to ensure that tests are consistent, readable, and maintainable, while verifying complete application workflows.

## Test Structure

### File Organization

1.  **Test Directories**:

    - E2E tests must be located in the `tests/e2e/` directory, with subdirectories for each resource or feature.
    - Example: `tests/e2e/city/` for E2E tests related to the city resource.

2.  **Test Files**:
    - Each test file must be dedicated to a single API endpoint (e.g., create, update, delete). This follows the same principle as unit tests, where each file targets a specific use case.
    - Example: `tests/e2e/city/test_city_create_api.py` for testing the creation endpoint, and `tests/e2e/city/test_city_update_api.py` for the update endpoint.

### Test Structure

1.  **Test Classes**:

    - Tests must be organized in test classes, with nested classes to separate success and failure scenarios.
    - Example (`tests/e2e/city/test_city_create_api.py`):
      ```python
      class TestCreateCity:
          class TestSuccess:
              # Success tests for city creation
          class TestFailures:
              # Failure tests for city creation
      ```

2.  **Test Methods**:
    - Each method must test a single, specific behavior.
    - Method names must be descriptive, following the `test_should_<behavior>` format.

## Fixtures and Test Environment

1.  **Test Client**:

    - Use FastAPI's `TestClient` to make HTTP requests to the application. The client should be provided via a `pytest` fixture.
    - Example:
      ```python
      @pytest.fixture(scope="module")
      def client():
          from fastapi.testclient import TestClient
          from main import app
          with TestClient(app) as c:
              yield c
      ```

2.  **Test Database**:

    - E2E tests must run against a dedicated test database to ensure isolation from the development and production environments.
    - Use fixtures to manage the test database lifecycle (creation, seeding, and teardown).
    - Tests should use real database connections and data, not mocks.

3.  **Dependency Injection with Container**:

    - Use the project's `core/container` to access use cases and repositories for test data setup and verification.
    - Example:
      ```python
      @pytest.fixture(scope="module")
      def container():
          from core.container.container import Container
          container = Container()
          container.wire(modules=["tests.e2e"])
          return container
      ```

4.  **Dependency Overrides**:
    - For external services that cannot be tested directly (e.g., payment gateways, email services), use FastAPI's dependency injection system to override them with mocks during tests.

## Test Scenarios

1.  **Success Scenarios**:

    - Verify that the API endpoints behave as expected with valid inputs. Check status codes, response bodies, and database state changes.
    - Example:

      ```python
      def test_should_create_city_successfully(client, container):
          # Given
          city_data = {"name": "New York", "region_id": 1}
          city_use_case = container.city_use_case()

          # When
          response = client.post("/api/v1/cities/", json=city_data)

          # Then
          assert response.status_code == 201
          data = response.json()
          assert data["name"] == "New York"

          # Verify in database using container
          created_city = await city_use_case.get_by_id(data["id"])
          assert created_city.name == "New York"
      ```

2.  **Failure Scenarios**:

    - Test how the system handles errors, such as invalid input, authentication failures, or business rule violations.
    - Example:

      ```python
      def test_should_return_409_when_city_already_exists(client, container):
          # Given
          city_use_case = container.city_use_case()
          # Create existing city using container
          existing_city = CityEntity(name="Paris", region_id=1)
          await city_use_case.create(existing_city)

          city_data = {"name": "Paris", "region_id": 1}

          # When
          response = client.post("/api/v1/cities/", json=city_data)

          # Then
          assert response.status_code == 409
      ```

## Best Practices

1.  **Readability**:

    - Write clear and expressive tests that document the application's behavior from a user's perspective.

2.  **Maintainability**:

    - Centralize common fixtures in `conftest.py`.
    - Avoid testing implementation details; focus on the public API contract.

3.  **Robustness**:
    - Ensure tests are independent and can be run in any order.
    - Clean up created resources after each test to maintain a consistent state.

## Recommended Packages

For E2E testing in this project, the following packages are recommended:

1.  **`TestClient`**: Provided by FastAPI for simulating HTTP requests.
2.  **`pytest`**: For structuring and running tests.
3.  **`pytest-mock`**: For mocking dependencies and external services.
4.  **Database-specific packages** (e.g., `pytest-postgresql`, `mongomock`): For creating isolated test databases.

## Test Workflow

After implementing a new E2E test file, follow these steps:

1.  **Update `Makefile`**:

    - Add a command to the `Makefile` to run the new test file individually.
    - Example:
      ```makefile
      test-e2e-city-create:
      	$(UV) run pytest $(TEST_PATH)e2e/city/test_city_create_api.py $(PYTEST_OPTS)
      ```

2.  **Execute the Specific Test**:

    - Run the new `make` command to verify that the new tests pass.
    - Example:
      ```bash
      make test-e2e-city-create
      ```

3.  **Run All E2E Tests**:
    - Run all E2E tests to ensure no regressions have been introduced.
    - Example:
      ```bash
      make test-e2e
      ```
