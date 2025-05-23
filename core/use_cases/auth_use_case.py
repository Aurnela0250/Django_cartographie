import logging
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from core.domain.entities.token_entity import TokenEntity
from core.domain.entities.user_entity import UserEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_user_repository import DjangoUserRepository
from infrastructure.external_services.jwt_service import JWTService
from presentation.exceptions import (
    AuthenticationError,
    ConflictError,
    InternalServerError,
    InvalidTokenError,
)


class AuthUseCase:
    def __init__(self, unit_of_work: UnitOfWork, jwt_service: JWTService):
        self.unit_of_work = unit_of_work
        self.jwt_service = jwt_service
        self.logger = logging.getLogger(__name__)

    def signup(self, email: str, password: str) -> UserEntity:
        with self.unit_of_work:
            user_repository = self.unit_of_work.get_repository(DjangoUserRepository)

            # Check if email already exists
            if user_repository.get_user_by_email(email):
                # Log without revealing the exact email in production logs
                self.logger.info("Signup attempt with existing account")
                raise ConflictError()

            user = UserEntity(
                id=None,
                email=email,
                password=password,
                created_at=None,
                updated_at=None,
            )

            user_created = user_repository.create_user(user)

            return user_created

    def login(self, login: str, password: str) -> TokenEntity:
        try:
            user_repository = self.unit_of_work.get_repository(DjangoUserRepository)
            user = user_repository.authenticate_user(login, password)

            if not user:
                raise AuthenticationError()
            if not user.active:
                raise AuthenticationError()
            if not user.id:
                raise AuthenticationError()

            (access_token, refresh_token, iat, exp) = self.jwt_service.generate_tokens(
                int(user.id)
            )

            return TokenEntity(
                access_token=access_token,
                refresh_token=refresh_token,
                iat=iat,
                exp=exp,
                user=user,
            )
        except AuthenticationError as e:
            raise e
        except Exception as e:
            print(f"Unexpected error during login {e}")
            raise InternalServerError()

    def refresh_token(self, token: str) -> TokenEntity:
        try:
            user_repository = self.unit_of_work.get_repository(DjangoUserRepository)
            # Décoder le refresh token
            payload = self.jwt_service.decode_refresh_token(token)
            user_id = payload["user_id"]
            jti = payload["jti"]

            # Révoquer l'ancien refresh token
            current_time = int(datetime.now(ZoneInfo("UTC")).timestamp())
            exp_time = payload["exp"] - current_time
            if exp_time > 0:
                self.jwt_service.revoke_token(jti, exp_time)

            # Générer de nouveaux tokens
            user_found = user_repository.get_user_by_id(user_id)
            (access_token, refresh_token, iat, exp) = self.jwt_service.generate_tokens(
                user_id
            )

            if not user_found:
                raise InvalidTokenError()
            if not user_found.active:
                raise InvalidTokenError()
            if not user_found.id:
                raise InvalidTokenError()

            return TokenEntity(
                access_token=access_token,
                refresh_token=refresh_token,
                iat=iat,
                exp=exp,
                user=user_found,
            )
        except InvalidTokenError as e:
            raise e
        except Exception as e:
            print(f"Unexpected error during token refresh {e}")
            raise InternalServerError()

    def get_current_user(self, user_id: int) -> UserEntity:
        try:
            user_repository = self.unit_of_work.get_repository(DjangoUserRepository)
            user = user_repository.get_user_by_id(user_id)

            if not user:
                raise AuthenticationError()
            if not user.active:
                raise AuthenticationError()
            if not user.id:
                raise AuthenticationError()

            return user
        except AuthenticationError as e:
            raise e
        except Exception as e:
            print(f"Unexpected error during getting current user {e}")
            raise InternalServerError()

    def logout(
        self,
        access_token: dict[str, Any],
        refresh_token: str,
    ) -> None:
        try:
            current_time = int(datetime.now(ZoneInfo("UTC")).timestamp())
            tokens_to_revoke = []

            # Prepare access token revocation
            access_jti = str(access_token.get("jti"))
            access_exp = access_token.get("exp", current_time)
            access_exp_time = access_exp - current_time

            if access_exp_time > 0:
                tokens_to_revoke.append((access_jti, access_exp_time))

            # Prepare refresh token revocation
            try:
                payload = self.jwt_service.decode_refresh_token(refresh_token)
                refresh_jti = payload["jti"]
                refresh_exp_time = payload["exp"] - current_time

                if refresh_exp_time > 0:
                    tokens_to_revoke.append((refresh_jti, refresh_exp_time))
            except Exception as e:
                self.logger.warning(f"Failed to decode refresh token: {str(e)}")

            # Revoke all tokens at once
            for jti, exp_time in tokens_to_revoke:
                self.jwt_service.revoke_token(jti, exp_time)

            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during logout {e}")
            raise InternalServerError()
