# Active Context

## Current Focus

- Refactoring unit tests for the City module to align with Clean Architecture principles.
- Centralizing common fixtures in `tests/unit/city/conftest.py`.
- Using `spec` for mocks to ensure strict adherence to repository interfaces.
- Introducing a `city_factory` for flexible and concise test data generation.
- Organizing tests in nested classes for better readability and separation of success and failure scenarios.

## Recent Changes

- Refactored `test_city_create_use_case.py`, `test_city_delete_use_case.py`, `test_city_get_use_case.py`, `test_city_update_use_case.py`, `test_city_filter_use_case.py`, and `test_city_get_all_use_case.py`.
- Updated `conftest.py` to include common fixtures and the `city_factory`.
- Updated the testing guidelines in `.clinerules/07-quality-assurance/7-test-unit.md` to include the `Makefile` update workflow.

## Next Steps

- Review and update other test modules to apply the same refactoring principles.
- Ensure all tests follow the new structure and use the centralized fixtures.
- Ensure the documented test workflow is followed for all new tests.

## Important Patterns and Preferences

- Use of `pytest` for testing.
- Strict adherence to Clean Architecture principles.
- Centralization of common test setup and teardown logic.
- Use of factories for test data generation.
- Organizing tests in nested classes for clarity.

## Learnings

- Refactoring tests to align with Clean Architecture improves maintainability and readability.
- Centralizing fixtures reduces code duplication and ensures consistency.
- Using `spec` for mocks helps catch interface violations early.
- Factories provide a flexible way to generate test data.
- Documenting the full test workflow, including `Makefile` updates, is crucial for maintaining a consistent and reliable testing process.

## Known Issues

- None at the moment.

## Evolution of Decisions

- Decided to centralize fixtures to avoid duplication and ensure consistency.
- Chose to use `spec` for mocks to enforce strict interface adherence.
- Opted for nested test classes to improve test organization and readability.
- Introduced a factory pattern for test data generation to enhance flexibility and conciseness.

## Testing Structure

### Common Fixtures

```python
# tests/unit/city/conftest.py

from unittest.mock import AsyncMock
import pytest
from core.entities.city import CityEntity
from core.interfaces.city_repository import ICityRepository
from core.use_cases.city_use_case import CityUseCase

@pytest.fixture
def mock_city_repository():
    """Mock du repository de ville avec spec strict"""
    return AsyncMock(spec=ICityRepository)

@pytest.fixture
def city_use_case(mock_city_repository):
    """Fixture pour créer une instance de CityUseCase avec des mocks"""
    return CityUseCase(city_repository=mock_city_repository)

@pytest.fixture
def city_factory():
    """Factory pour créer des entités CityEntity avec des valeurs par défaut"""
    def _factory(**overrides):
        defaults = {
            "id": None,
            "name": "Default City",
            "region_id": 1,
            "created_at": None,
            "updated_at": None,
        }
        return CityEntity(**{**defaults, **overrides})
    return _factory
```

### Test Structure

```python
# tests/unit/city/test_city_create_use_case.py

import pytest
from presentation.exceptions import ConflictException, InternalServerErrorException

class TestCityCreateUseCase:
    """Tests unitaires pour la méthode create de CityUseCase"""

    class TestSuccess:
        """Tests des cas de succès"""

        @pytest.mark.asyncio
        async def test_should_create_city_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de création de ville réussie"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            created_city = city_factory(id=1, name="Paris", region_id=1)
            mock_city_repository.get_by_name.return_value = None
            mock_city_repository.create.return_value = created_city

            # When
            result = await city_use_case.create(new_city)

            # Then
            assert result == created_city
            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_called_once_with(new_city)

    class TestFailures:
        """Tests des cas d'échec"""

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_city_already_exists(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de création de ville avec nom déjà existant"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            existing_city = city_factory(id=1, name="Paris", region_id=1)
            mock_city_repository.get_by_name.return_value = existing_city

            # When & Then
            with pytest.raises(ConflictException):
                await city_use_case.create(new_city)

            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_get_by_name_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la vérification d'existence"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            mock_city_repository.get_by_name.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.create(new_city)

            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_not_called()

        @pytest.mark.asyncio
        async def test_should_raise_internal_error_on_create_failure(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test de gestion d'erreur lors de la création en base"""
            # Given
            new_city = city_factory(name="Paris", region_id=1)
            mock_city_repository.get_by_name.return_value = None
            mock_city_repository.create.side_effect = Exception("Database error")

            # When & Then
            with pytest.raises(InternalServerErrorException):
                await city_use_case.create(new_city)

            mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
            mock_city_repository.create.assert_called_once_with(new_city)
```

### Applying the Structure to Other Tests

- Follow the same structure for other test files (`test_city_delete_use_case.py`, `test_city_get_use_case.py`, `test_city_update_use_case.py`, `test_city_filter_use_case.py`, and `test_city_get_all_use_case.py`).
- Ensure all tests use the centralized fixtures and follow the nested class structure for clarity.

### Test Workflow

After implementing a new test file, the following steps must be followed:

1.  **Update `Makefile`**:

    - Add a new command in the `Makefile` to run the newly created test file specifically. This allows for isolated testing and easier debugging.
    - For example, for a new test file `tests/unit/new_module/test_new_feature.py`, you would add:
      ```makefile
      test-unit-new-module-new-feature:
      	$(UV) run pytest $(TEST_PATH)unit/new_module/test_new_feature.py $(PYTEST_OPTS)
      ```

2.  **Execute the Specific Test**:

    - Run the newly created `make` command to ensure that your new tests pass without errors.
    - Example:
      ```bash
      make test-unit-new-module-new-feature
      ```

3.  **Run All Unit Tests**:
    - Finally, run all unit tests to verify that your changes have not introduced any regressions in other parts of the application.
    - Example:
      ```bash
      make test-unit
      ```
