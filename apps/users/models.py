from typing import Optional

import uuid6

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        username: str,
        password: Optional[str] = None,
        **extra_fields,
    ):

        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, username: str, password: Optional[str] = None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid6.uuid7,
        editable=False,
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    is_two_factor_enabled = models.BooleanField(default=False)
    image = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_users",
    )
    updated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_users",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)

    objects: models.Manager["User"] = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Client(models.Model):
    CLIENT_TYPE = [
        ("NURSERY", "Pépinière"),
        ("COLLEGIAN", "Collégien"),
        ("STUDENT", "Lycéen"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    client_type = models.CharField(
        max_length=20,
        choices=CLIENT_TYPE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.client_type}"
