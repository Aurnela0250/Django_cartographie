from typing import Optional
from uuid import UUID

from apps.users.models import User
from core.domain.entities.user_entity import UserEntity
from core.interfaces.user_repository import UserRepository


class DjangoUserRepository(UserRepository):

    def create_user(self, user: UserEntity) -> UserEntity:
        django_user = User(
            email=user.email,
        )
        django_user.set_password(user.password)
        django_user.save()
        return self._to_entity(django_user)

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(email=email)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        # Since our User model uses email as the username field,
        # we'll just call get_user_by_email
        return self.get_user_by_email(username)

    def get_user_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        try:
            user = User.objects.get(id=user_id)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        # In this implementation, we only use email as login
        user = User.objects.filter(email=login).first()
        if user and user.check_password(password):
            # If the user exists and the password is correct
            return self._to_entity(user)
        return None

    def _to_entity(self, django_user: User) -> UserEntity:
        return UserEntity(
            id=django_user.id,
            email=django_user.email,
            password="",  # We don't return the password
            active=django_user.active,
            updated_by=django_user.updated_by,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at,
        )
