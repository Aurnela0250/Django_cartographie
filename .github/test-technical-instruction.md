Here is the English translation:

# Tests with Django Ninja Extra

Django Ninja Extra is a powerful extension for Django Ninja that introduces class-based views and advanced features while maintaining the high performance and simplicity of Django Ninja. The test structure remains similar to that used for standard Django, but with some specifics for testing APIs.

## Recommended structure for tests

```
tests/
├── unit/                      # Isolated unit tests
│   ├── core/                  # Core business tests
│   │   ├── domain/
│   │   │   └── entities/      # Entity tests
│   │   ├── use_cases/         # Use case tests
│   │   └── interfaces/        # Abstract interface tests
│   ├── infrastructure/        # Concrete implementation tests
│   │   ├── db/                # Repository tests
│   │   └── external_services/ # External service tests
│   └── presentation/          # Controller and schema tests
│       ├── api/
│       └── schemas/
├── integration/               # Integration tests
│   ├── repositories/          # Tests with real DB
│   └── services/              # Tests with external services
└── api/                       # Complete endpoint tests
    └── v1/                    # Tests by API version

```

## Specific tests for Django Ninja Extra

With Django Ninja Extra, you can use standard Django test classes as well as specialized test clients provided by the framework.

### Testing API controllers

To test your class-based API controllers with Django Ninja Extra, use `ninja_extra.testing.TestClient`:

```python
from django.test import TestCase
from ninja_extra.testing import TestClient
from myapp.api import UserController

class UserControllerTest(TestCase):
    def setUp(self):
        self.client = TestClient(UserController)

    def test_user_list(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
```

### Testing APIs with JWT authentication

If you're using ninja_jwt for authentication:

```python
from django.test import TestCase
from ninja_extra.testing import TestClient
from ninja_jwt.controller import NinjaJWTDefaultController
from myapp.api import SecuredController

class SecuredAPITest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Get a JWT token
        token_client = TestClient(NinjaJWTDefaultController)
        response = token_client.post("/token/pair", data={
            "username": "testuser",
            "password": "testpassword"
        })
        self.token = response.data["access"]

        # Initialize the client with the controller to test
        self.client = TestClient(SecuredController)

    def test_protected_endpoint(self):
        # Call the endpoint with the JWT token
        response = self.client.get(
            "/protected-resource",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)
```

## Test examples by type

### 1. Unit test of an entity

```python
import pytest
from pydantic import ValidationError
from core.domain.entities.user_entity import User

class TestUserEntity:
    def test_valid_user_creation(self) -> None:
        """Test that a valid user can be created."""
        user = User(
            id="1",
            email="test@example.com",
            username="testuser",
            hashed_password="hashedpassword123"
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"

    def test_invalid_email_format(self) -> None:
        """Test that an error is raised with an invalid email."""
        with pytest.raises(ValidationError):
            User(
                id="1",
                email="invalid-email",
                username="testuser",
                hashed_password="hashedpassword123"
            )
```

### 2. Unit test of a use case

```python
import pytest
from unittest.mock import Mock, patch
from core.use_cases.auth_use_case import LoginUseCase
from core.domain.entities.user_entity import User
from presentation.exceptions import AuthenticationError

class TestLoginUseCase:
    def setup_method(self) -> None:
        self.user_repository = Mock()
        self.jwt_service = Mock()
        self.login_use_case = LoginUseCase(
            user_repository=self.user_repository,
            jwt_service=self.jwt_service
        )

    def test_successful_login(self) -> None:
        """Test that a login succeeds with valid credentials."""
        # Arrange
        email = "test@example.com"
        password = "password123"
        user = User(id="1", email=email, username="testuser", hashed_password="hashed_password")

        self.user_repository.get_user_by_email.return_value = user
        self.jwt_service.create_access_token.return_value = "access_token"
        self.jwt_service.create_refresh_token.return_value = "refresh_token"

        with patch('core.use_cases.auth_use_case.verify_password', return_value=True):
            # Act
            result = self.login_use_case.execute(email=email, password=password)

            # Assert
            assert result["access_token"] == "access_token"
            assert result["refresh_token"] == "refresh_token"
            self.user_repository.get_user_by_email.assert_called_once_with(email)
```

### 3. Integration test of a repository

```python
from django.test import TestCase
from infrastructure.db.django_user_repository import DjangoUserRepository
from apps.users.models import User as UserModel

class TestDjangoUserRepository(TestCase):
    def setUp(self) -> None:
        self.repository = DjangoUserRepository()
        # Create a test user in the database
        self.user_model = UserModel.objects.create(
            email="test@example.com",
            username="testuser",
            password="hashedpassword123"
        )

    def test_get_user_by_email(self) -> None:
        """Test that the repository can retrieve a user by email."""
        # Act
        user = self.repository.get_user_by_email("test@example.com")

        # Assert
        assert user is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
```

### 4. API test of a controller with Django Ninja Extra

```python
from django.test import TestCase
from ninja_extra.testing import TestClient
from apps.api.controllers import AuthController
from apps.users.models import User

class TestAuthController(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(AuthController)
        # Create a test user
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="password123"
        )

    def test_login_success(self) -> None:
        """Test that a user can log in with valid credentials."""
        # Act
        response = self.client.post(
            "/login",
            data={
                "email": "test@example.com",
                "password": "password123"
            }
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
```

## Recommended tools

Add these dependencies to your `requirements.txt`:

```
pytest==7.4.0
pytest-django==4.5.2
pytest-cov==4.1.0
factory-boy==3.2.1
```

## Test configuration and execution

Create a `pytest.ini` file at the root of the project:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

Commands to run the tests:

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Tests with code coverage
pytest --cov=.

# Generate an HTML coverage report
pytest --cov=. --cov-report=html
```
