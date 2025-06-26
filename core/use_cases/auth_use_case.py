import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from tortoise.transactions import atomic

from core.entities.token import TokenEntity
from core.entities.user import UserEntity
from core.interfaces.auth_repository import IAuthRepository
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from presentation.constants import errors_code
from presentation.exceptions import (
    BcryptHashPasswordException,
    BcryptVerifyPasswordException,
    ConflictException,
    DatabaseDoesNotExistException,
    DatabaseException,
    DatabaseIntegrityException,
    InternalServerErrorException,
    UnauthorizedException,
)


class AuthUseCase:
    def __init__(
        self,
        jwt_service: JWTService,
        bcrypt_service: BcryptService,
        auth_repository: IAuthRepository,
    ):
        self.jwt_service = jwt_service
        self.bcrypt_service = bcrypt_service
        self.auth_repository = auth_repository
        self.logger = logging.getLogger(__name__)

    @atomic()
    async def signup(
        self,
        email: str,
        password: str,
    ) -> UserEntity:
        try:
            # Hash the password before storing
            hashed_password = await self.bcrypt_service.hash_password(password)

            user_created = await self.auth_repository.signup(
                email=email,
                hashed_password=hashed_password,
            )

            return user_created
        except DatabaseIntegrityException as e:
            self.logger.warning(f"Signup failed for existing email {email}: {e}")
            raise ConflictException(cause=e)
        except BcryptHashPasswordException as e:
            self.logger.error(f"Error hashing password during signup: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during signup: {str(e)}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def login(self, login: str, password: str) -> TokenEntity:
        try:
            user = await self.auth_repository.get_user_by_email(login)

            # Verify the password first
            is_password_valid = await self.bcrypt_service.verify_password(
                password,
                user.password,
            )

            if not is_password_valid:
                raise UnauthorizedException(code=errors_code.INVALID_CREDENTIALS)

            # Then check if user ID is valid
            if not user.id:
                self.logger.error(
                    f"Unexpected error during login: User ID is None for user {login}"
                )
                raise InternalServerErrorException()

            token = await self.jwt_service.generate_tokens(int(user.id))

            return TokenEntity(
                user_id=token.user_id,
                exp=token.exp,
                iat=token.iat,
                jti=token.jti,
                token_type=token.token_type,
                iss=token.iss,
                aud=token.aud,
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                user=user,
            )
        except DatabaseDoesNotExistException as e:
            raise UnauthorizedException(cause=e, code=errors_code.INVALID_CREDENTIALS)
        except UnauthorizedException as e:
            self.logger.warning(f"Login failed for user {login}: {e}")
            raise e  # Preserve the original exception with its code
        except BcryptVerifyPasswordException as e:
            self.logger.error(f"Error verifying password during login: {str(e)}")
            raise InternalServerErrorException(cause=e)
        except DatabaseException as e:
            raise InternalServerErrorException(cause=e)
        except Exception as e:
            self.logger.warning(f"Unexpected error during login: {e}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def refresh_token(self, token: str) -> TokenEntity:
        try:
            # Décoder le refresh token
            payload = await self.jwt_service.decode_refresh_token(token)
            user_id = payload.user_id
            jti = payload.jti

            # Révoquer l'ancien refresh token
            current_time = int(datetime.now(ZoneInfo("UTC")).timestamp())
            exp_time = payload.exp - current_time
            if exp_time > 0:
                await self.jwt_service.revoke_token(jti, exp_time)

            # Vérifier que l'utilisateur existe avant de générer de nouveaux tokens
            user_found = await self.auth_repository.get_user_by_id(user_id)
            if not user_found.id:
                raise InternalServerErrorException()

            # Générer de nouveaux tokens seulement si l'utilisateur est valide
            new_token = await self.jwt_service.generate_tokens(user_id)

            return TokenEntity(
                user_id=new_token.user_id,
                exp=new_token.exp,
                iat=new_token.iat,
                jti=new_token.jti,
                token_type=new_token.token_type,
                iss=new_token.iss,
                aud=new_token.aud,
                access_token=new_token.access_token,
                refresh_token=new_token.refresh_token,
                user=user_found,
            )
        except DatabaseDoesNotExistException as e:
            raise UnauthorizedException(cause=e, code=errors_code.INVALID_TOKEN)
        except UnauthorizedException as e:
            self.logger.warning(f"Token refresh failed: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error during token refresh: {e}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def get_current_user(self, user_id: int) -> UserEntity:
        try:
            user = await self.auth_repository.get_user_by_id(user_id)

            if not user.id:
                raise InternalServerErrorException()

            return user
        except DatabaseDoesNotExistException as e:
            raise UnauthorizedException(code=errors_code.INVALID_TOKEN, cause=e)
        except Exception as e:
            print(f"Unexpected error during getting current user {e}")
            raise InternalServerErrorException(cause=e)

    @atomic()
    async def logout(
        self,
        access_token: str,
        refresh_token: str,
    ) -> None:
        try:
            current_time = int(datetime.now(ZoneInfo("UTC")).timestamp())
            tokens_to_revoke = []

            # Decode access token
            access_token_payload = await self.jwt_service.decode_access_token(
                access_token
            )
            access_jti = access_token_payload.jti
            access_exp_time = access_token_payload.exp - current_time

            if access_exp_time > 0:
                tokens_to_revoke.append((access_jti, access_exp_time))

            # Decode refresh token
            refresh_token_payload = await self.jwt_service.decode_refresh_token(
                refresh_token
            )
            refresh_jti = refresh_token_payload.jti
            refresh_exp_time = refresh_token_payload.exp - current_time

            if refresh_exp_time > 0:
                tokens_to_revoke.append((refresh_jti, refresh_exp_time))

            # Revoke all tokens at once
            for jti, exp_time in tokens_to_revoke:
                await self.jwt_service.revoke_token(jti, exp_time)

            return None
        except UnauthorizedException as e:
            self.logger.warning(f"Token logout failed: {e}")
            raise UnauthorizedException(cause=e)
        except Exception as e:
            self.logger.error(f"Unexpected error during logout {e}")
            raise InternalServerErrorException(cause=e)
