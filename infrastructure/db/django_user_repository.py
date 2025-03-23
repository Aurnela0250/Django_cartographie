from typing import Optional
from uuid import UUID

from apps.users.models import Client, User
from core.domain.entities.user import ClientEntity, UserEntity
from core.interfaces.user_repository import UserRepository


class DjangoUserRepository(UserRepository):

    def create_user(self, user: UserEntity) -> UserEntity:
        django_user = User(
            email=user.email,
            username=user.username,
        )
        django_user.set_password(user.password)
        django_user.save()
        return self._to_entity(django_user)

    def create_client(self, client: ClientEntity) -> ClientEntity:
        django_user = User(
            email=client.email,
            username=client.username,
        )
        django_user.set_password(client.password)
        django_user.save()

        Client.objects.create(
            user=django_user,
            client_type=client.client_type,
        )

        return self._to_client_entity(django_user)

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(email=email)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def get_user_by_username(self, username: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(username=username)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def get_user_by_id(self, user_id: UUID) -> Optional[UserEntity]:
        try:
            user = User.objects.get(id=user_id)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        # Vérifier d'abord si le login correspond à un email
        user = User.objects.filter(email=login).first()
        if user is None:
            # Si ce n'est pas un email, vérifier si c'est un nom d'utilisateur
            user = User.objects.filter(username=login).first()
        if user and user.check_password(password):
            # Si l'utilisateur existe et le mot de passe est correct
            return self._to_entity(user)
        return None

    def _to_entity(self, django_user: User) -> UserEntity:
        return UserEntity(
            id=django_user.id,
            email=django_user.email,
            username=django_user.username,
            password="",  # We don't return the password
            active=django_user.active,
            email_verified=django_user.email_verified,
            is_two_factor_enabled=django_user.is_two_factor_enabled,
            image=django_user.image,
            created_by=(
                django_user.created_by.id if django_user.created_by else django_user.id
            ),
            updated_by=django_user.updated_by,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at,
        )

    def _to_client_entity(self, django_user: User) -> ClientEntity:
        client = Client.objects.get(user=django_user)
        return ClientEntity(
            id=django_user.id,
            email=django_user.email,
            username=django_user.username,
            password="",
            active=django_user.active,
            email_verified=django_user.email_verified,
            is_two_factor_enabled=django_user.is_two_factor_enabled,
            image=django_user.image,
            created_by=(
                django_user.created_by.id if django_user.created_by else django_user.id
            ),
            updated_by=django_user.updated_by,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at,
            client_type=client.client_type,
        )
