import pytest
from django.test import TestCase
from ninja_extra.testing import TestClient

from apps.users.models import User
from presentation.api.v1.endpoints.auth_controller import AuthController


@pytest.mark.api
class TestAuthController(TestCase):
    def setUp(self):
        self.client = TestClient(AuthController)
        # Create a test user
        self.test_user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

    def test_sign_up_success(self):
        # Act
        response = self.client.post(
            "/signin", json={"email": "new@example.com", "password": "newpassword"}
        )

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], "new@example.com")

        # Verify user was created in the database
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_sign_up_existing_user(self):
        # Act
        response = self.client.post(
            "/signin", json={"email": "test@example.com", "password": "newpassword"}
        )

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertIn("message", response.json())

    def test_login_success(self):
        # Act
        response = self.client.post(
            "/login", json={"email": "test@example.com", "password": "testpassword"}
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("refresh_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")

    def test_login_invalid_credentials(self):
        # Act
        response = self.client.post(
            "/login", json={"email": "test@example.com", "password": "wrongpassword"}
        )

        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json())

    def test_get_current_user(self):
        # First login to get a token
        login_response = self.client.post(
            "/login", json={"email": "test@example.com", "password": "testpassword"}
        )

        access_token = login_response.json()["access_token"]

        # Act - Get current user with the token
        response = self.client.get(
            "/me", headers={"Authorization": f"Bearer {access_token}"}
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test@example.com")

    def test_refresh_token(self):
        # First login to get tokens
        login_response = self.client.post(
            "/login", json={"email": "test@example.com", "password": "testpassword"}
        )

        refresh_token = login_response.json()["refresh_token"]

        # Act - Refresh the token
        response = self.client.post(
            "/refresh",
            json={"refresh_token": refresh_token},
            headers={
                "Authorization": f"Bearer {login_response.json()['access_token']}"
            },
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("refresh_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")
