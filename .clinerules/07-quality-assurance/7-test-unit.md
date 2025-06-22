# Test Rules for the Project

## Introduction

This document defines the rules and conventions to follow for writing unit tests in this project. These rules aim to ensure consistency, readability, and maintainability of tests.

## Test Structure

### File Organization

1. **Test Directories**:

   - Tests must be organized in directories specific to each module or entity.
   - Example: `tests/unit/city/` for unit tests of the `City` module.

2. **Test Files**:
   - Each test file must correspond to a single entity or use case.
   - Example: `test_city_create_use_case.py` for tests of the `create` method of `CityUseCase`.

### Test Structure

1. **Test Classes**:

   - Tests must be organized in test classes, with nested classes to separate success and failure scenarios.
   - Example:

     ```python
     class TestCityCreateUseCase:
         class TestSuccess:
             # Success tests

         class TestFailures:
             # Failure tests
     ```

2. **Test Methods**:
   - Each test method must test a single behavior or scenario.
   - Test methods must be named descriptively, following the format `test_should_<behavior>`.

### Fixtures

1. **Centralization of Fixtures**:

   - Common fixtures must be centralized in a `conftest.py` file at the root of the module's test directory.
   - Example: `tests/unit/city/conftest.py`.

2. **Using `spec` for Mocks**:

   - Mocks must use `spec` to ensure they strictly respect the repository interface.
   - Example:
     ```python
     @pytest.fixture
     def mock_city_repository():
         return AsyncMock(spec=ICityRepository)
     ```

3. **Factories for Test Data**:
   - Use factories to generate test entities in a flexible and concise manner.
   - Example:
     ```python
     @pytest.fixture
     def city_factory():
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

### Test Scenarios

1. **Success Scenarios**:

   - Success tests must verify that the expected behavior is correctly implemented.
   - Example:

     ```python
     @pytest.mark.asyncio
     async def test_should_create_city_successfully(
         self, city_use_case, mock_city_repository, city_factory
     ):
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
     ```

2. **Failure Scenarios**:

   - Failure tests must verify that errors or exceptions are correctly handled.
   - Example:

     ```python
     @pytest.mark.asyncio
     async def test_should_raise_conflict_when_city_already_exists(
         self, city_use_case, mock_city_repository, city_factory
     ):
         # Given
         new_city = city_factory(name="Paris", region_id=1)
         existing_city = city_factory(id=1, name="Paris", region_id=1)
         mock_city_repository.get_by_name.return_value = existing_city

         # When & Then
         with pytest.raises(ConflictException):
             await city_use_case.create(new_city)

         mock_city_repository.get_by_name.assert_called_once_with(new_city.name)
         mock_city_repository.create.assert_not_called()
     ```

### Best Practices

1. **Readability and Intention**:

   - Tests must be clear and express business behavior.
   - Use descriptive names for fixtures, classes, and test methods.

2. **Maintainability**:

   - Avoid code duplication by centralizing fixtures and using factories.
   - Organize tests in nested classes for better readability.

3. **Robustness**:
   - Use strict mocks (`spec`) to ensure that tests fail if contracts (interfaces) are not respected.
   - Test error cases to ensure that exceptions are correctly handled.

## Test Workflow

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

## Complete Example

Here is a complete example of a test file following these rules:

```python
# tests/unit/city/test_city_create_use_case.py

import pytest
from presentation.exceptions import ConflictException, InternalServerErrorException

class TestCityCreateUseCase:
    """Unit tests for the create method of CityUseCase"""

    class TestSuccess:
        """Tests for success cases"""

        @pytest.mark.asyncio
        async def test_should_create_city_successfully(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test for successful city creation"""
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
        """Tests for failure cases"""

        @pytest.mark.asyncio
        async def test_should_raise_conflict_when_city_already_exists(
            self, city_use_case, mock_city_repository, city_factory
        ):
            """Test for city creation with already existing name"""
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
            """Test for error handling during existence check"""
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
            """Test for error handling during database creation"""
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

By following these rules, we ensure that all tests are consistent, readable, and maintainable, while respecting Clean Architecture principles.
