# presentation/api/auth_utils.py


from django.http.request import HttpRequest
from ninja.errors import HttpError
from ninja.security import HttpBearer

from infrastructure.external_services.jwt_service import JWTService

# presentation/api/auth_utils.py


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token):
        payload = JWTService.decode_token(token)
        if not payload or payload["token_type"] != "access":
            raise HttpError(401, "Invalid token")
        return payload


jwt_auth = JWTAuth()
