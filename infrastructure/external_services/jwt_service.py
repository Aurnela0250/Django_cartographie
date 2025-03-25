from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt  # Import simple de jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from ninja.errors import HttpError
from ninja.security import HttpBearer

User = get_user_model()


class JWTService:
    @staticmethod
    def generate_tokens(user_id: str):
        current_time = datetime.now(ZoneInfo("UTC"))
        access_expire_time = current_time + timedelta(minutes=60)
        refresh_expire_time = current_time + timedelta(days=7)

        # Calculer la durée d'expiration en secondes
        access_expire_in = int((access_expire_time - current_time).total_seconds())
        refresh_expire_in = int((refresh_expire_time - current_time).total_seconds())

        access_token_payload = {
            "user_id": str(user_id),
            "exp": access_expire_time,
            "iat": current_time,
            "token_type": "access",
        }

        refresh_token_payload = {
            "user_id": str(user_id),
            "exp": refresh_expire_time,
            "iat": current_time,
            "token_type": "refresh",
        }

        access_token = jwt.encode(
            access_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )
        refresh_token = jwt.encode(
            refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
        )

        return (
            access_token,
            refresh_token,
            access_expire_in,
            refresh_expire_in,
            current_time,
        )

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token):
        payload = JWTService.decode_token(token)
        if not payload or payload["token_type"] != "access":
            raise HttpError(401, "Invalid token")

        try:
            user = User.objects.get(id=payload["user_id"])
            request.user = user  # Ajoutez l'utilisateur à la requête
        except User.DoesNotExist:
            raise HttpError(401, "User not found")

        return payload


jwt_auth = JWTAuth()
