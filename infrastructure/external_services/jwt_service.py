from datetime import datetime
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from ninja.security import HttpBearer

from infrastructure.external_services.redis_service import RedisService
from presentation.exceptions import InternalServerError, InvalidTokenError

User = get_user_model()


class JWTService:
    @staticmethod
    def generate_tokens(user_id: int):
        """
        Génération des tokens d'accès et de rafraîchissement avec
        une durée d'expiration différenciée, des claims supplémentaires
        et la signature asymétrique (RS256).
        """
        current_time = datetime.now(ZoneInfo("UTC"))
        iat = int(current_time.timestamp())
        jti_access = str(uuid4())  # Identifiant unique pour le access token
        jti_refresh = str(uuid4())  # Identifiant unique pour le refresh token

        # Utilisation des paramètres de durée de vie depuis settings
        exp_access = int((current_time + settings.ACCESS_TOKEN_LIFETIME).timestamp())
        exp_refresh = int((current_time + settings.REFRESH_TOKEN_LIFETIME).timestamp())

        access_token_payload = {
            "user_id": int(user_id),
            "exp": exp_access,
            "iat": iat,
            "jti": jti_access,
            "token_type": "access",
            "iss": settings.JWT_ISSUER,  # Ajout d'un émetteur
            "aud": settings.JWT_AUDIENCE,  # Ajout d'une audience
        }

        refresh_token_payload = {
            "user_id": int(user_id),
            "exp": exp_refresh,
            "iat": iat,
            "jti": jti_refresh,
            "token_type": "refresh",
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
        }

        # Utilisation de clés différentes pour access et refresh tokens
        access_token = jwt.encode(
            access_token_payload,
            settings.JWT_ACCESS_PRIVATE_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        refresh_token = jwt.encode(
            refresh_token_payload,
            settings.JWT_REFRESH_PRIVATE_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        return (access_token, refresh_token, iat, exp_access)

    @staticmethod
    def decode_access_token(token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
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

            if not payload:
                raise InvalidTokenError()

            if payload["token_type"] != "access":
                raise InvalidTokenError("Token type not valid")

            # Vérifier si le token est révoqué
            if JWTService.is_token_revoked(payload.get("jti")):
                raise InvalidTokenError("Token has been revoked")

            return payload

        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Token expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")
        except InvalidTokenError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @staticmethod
    def decode_refresh_token(token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_REFRESH_PUBLIC_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_signature": True, "verify_exp": True},
                audience=settings.JWT_AUDIENCE,
                issuer=settings.JWT_ISSUER,
            )

            if not payload:
                raise InvalidTokenError()

            if payload["token_type"] != "refresh":
                raise InvalidTokenError("Token type not valid")

            # Vérifier si le token est révoqué
            if JWTService.is_token_revoked(payload.get("jti")):
                raise InvalidTokenError("Token has been revoked")

            return payload

        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Refresh token expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid refresh token")
        except InvalidTokenError as e:
            raise e
        except Exception as e:
            print(f"Erreur durant decode acces token : {e}")
            raise InternalServerError()

    @staticmethod
    def is_token_revoked(jti: str) -> bool:
        """
        Vérifie si un token a été révoqué en utilisant son identifiant unique (jti)
        en consultant Redis.
        """
        if not jti:
            return False
        return RedisService.exists(f"revoked_token:{jti}")

    @staticmethod
    def revoke_token(jti: str, exp_time: int) -> None:
        """
        Révoque un token en ajoutant son jti à la liste noire dans Redis
        avec une durée d'expiration correspondant à celle du token.
        """
        if jti and exp_time > 0:
            RedisService.set(f"revoked_token:{jti}", "1", exp=exp_time)


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token):
        payload = JWTService.decode_access_token(token)

        try:
            user = User.objects.get(id=payload["user_id"])
            request.user = user
        except User.DoesNotExist:
            raise InvalidTokenError("User not found")

        return payload


jwt_auth = JWTAuth()
