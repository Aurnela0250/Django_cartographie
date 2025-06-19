import asyncio
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

import jwt

from config import settings
from core.entities.token_entity import Payload, Token
from infrastructure.external_services.redis_service import RedisService
from presentation.constants import errors_code
from presentation.exceptions import (
    InternalServerErrorException,
    UnauthorizedException,
)


class JWTService:
    def __init__(self, redis_service: RedisService):
        """
        Initialise le JWTService avec le RedisService injecté
        """
        self.redis_service = redis_service

    async def generate_tokens(self, user_id: int) -> Token:
        """
        Génération des tokens d'accès et de rafraîchissement avec
        une durée d'expiration différenciée, des claims supplémentaires
        et la signature asymétrique (RS256).
        """
        current_time = datetime.now(ZoneInfo("UTC"))
        iat = int(current_time.timestamp())
        jti_access = str(uuid4())
        jti_refresh = str(uuid4())

        # Utilisation des paramètres de durée de vie depuis settings
        exp_access = int((current_time + settings.ACCESS_TOKEN_LIFETIME).timestamp())
        exp_refresh = int((current_time + settings.REFRESH_TOKEN_LIFETIME).timestamp())

        access_token_payload = Payload(
            user_id=int(user_id),
            exp=exp_access,
            iat=iat,
            jti=jti_access,
            token_type="access",
            iss=settings.JWT_ISSUER,
            aud=settings.JWT_AUDIENCE,
        )

        refresh_token_payload = Payload(
            user_id=int(user_id),
            exp=exp_refresh,
            iat=iat,
            jti=jti_refresh,
            token_type="refresh",
            iss=settings.JWT_ISSUER,
            aud=settings.JWT_AUDIENCE,
        )

        # Utilisation de clés différentes pour access et refresh tokens avec asyncio.to_thread
        access_token = await asyncio.to_thread(
            jwt.encode,
            access_token_payload.model_dump(),
            settings.JWT_ACCESS_PRIVATE_KEY,
            settings.JWT_ALGORITHM,
        )
        refresh_token = await asyncio.to_thread(
            jwt.encode,
            refresh_token_payload.model_dump(),
            settings.JWT_REFRESH_PRIVATE_KEY,
            settings.JWT_ALGORITHM,
        )

        return Token(
            **access_token_payload.model_dump(),
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def decode_access_token(self, token: str) -> Payload:
        try:
            decoded_payload = await asyncio.to_thread(
                jwt.decode,
                token,
                settings.JWT_ACCESS_PUBLIC_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": True,
                },
                audience=settings.JWT_AUDIENCE,
                issuer=settings.JWT_ISSUER,
            )

            if not decoded_payload:
                raise UnauthorizedException(code=errors_code.INVALID_TOKEN)

            # Instancier le Payload directement après le décodage
            payload = Payload(**decoded_payload)

            if payload.token_type != "access":
                raise UnauthorizedException(code=errors_code.INVALID_TOKEN)

            # Vérifier si le token est révoqué
            if await self.is_token_revoked(payload.jti):
                raise UnauthorizedException(code=errors_code.TOKEN_REVOKED)

            return payload

        except jwt.ExpiredSignatureError as e:
            raise UnauthorizedException(code=errors_code.TOKEN_EXPIRED, cause=e)
        except jwt.InvalidTokenError as e:
            raise UnauthorizedException(code=errors_code.INVALID_TOKEN, cause=e)
        except UnauthorizedException as e:
            raise e
        except Exception as e:
            raise InternalServerErrorException(cause=e)

    async def decode_refresh_token(self, token: str) -> Payload:
        try:
            decoded_payload = await asyncio.to_thread(
                jwt.decode,
                token,
                settings.JWT_REFRESH_PUBLIC_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": True,
                },
                audience=settings.JWT_AUDIENCE,
                issuer=settings.JWT_ISSUER,
            )

            if not decoded_payload:
                raise UnauthorizedException(code=errors_code.INVALID_TOKEN)

            # Instancier le Payload directement après le décodage
            payload = Payload(**decoded_payload)

            if payload.token_type != "refresh":
                raise UnauthorizedException(code=errors_code.INVALID_TOKEN)

            # Vérifier si le token est révoqué
            if await self.is_token_revoked(payload.jti):
                raise UnauthorizedException(code=errors_code.TOKEN_REVOKED)

            return payload

        except jwt.ExpiredSignatureError as e:
            raise UnauthorizedException(code=errors_code.TOKEN_EXPIRED, cause=e)
        except jwt.InvalidTokenError as e:
            raise UnauthorizedException(code=errors_code.INVALID_TOKEN, cause=e)
        except Exception as e:
            raise InternalServerErrorException(cause=e)

    async def is_token_revoked(self, jti: str) -> bool:
        """
        Vérifie si un token a été révoqué en utilisant son identifiant unique (jti)
        en consultant Redis.
        """
        if not jti:
            return False
        return await self.redis_service.exists(f"revoked_token:{jti}")

    async def revoke_token(self, jti: str, exp_time: int) -> None:
        """
        Révoque un token en ajoutant son jti à la liste noire dans Redis
        avec une durée d'expiration correspondant à celle du token.
        """
        if jti and exp_time > 0:
            await self.redis_service.set(f"revoked_token:{jti}", "1", exp=exp_time)
