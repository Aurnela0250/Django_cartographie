import logging

from ninja.errors import HttpError
from ninja_extra import api_controller, http_get, http_post

from core.use_cases.auth_use_cases import LoginUseCase, SignUpUseCase
from infrastructure.db.django_user_repository import DjangoUserRepository
from infrastructure.external_services.jwt_service import JWTService
from presentation.api.auth_utils import jwt_auth
from presentation.exceptions import AuthenticationError, ConflictError, ValidationError
from presentation.schemas.auth_schems import Login, Token
from presentation.schemas.user_schemas import UserCreate, UserOut


@api_controller("/auth", tags=["Authentication"])
class AuthController:
    def __init__(self):
        self.user_repository = DjangoUserRepository()
        self.jwt_service = JWTService()
        self.logger = logging.getLogger(__name__)

    @http_post("/signin", response={201: UserOut, 400: dict, 409: dict, 422: dict})
    def sign_up_client(self, user_data: UserCreate):
        try:
            use_case = SignUpUseCase(self.user_repository)
            client = use_case.execute(user_data.email, user_data.password)
            return 201, UserOut.from_orm(client)
        except ValidationError as e:
            self.logger.warning("Validation error during sign up")
            return 422, e.detail
        except ConflictError as e:
            self.logger.warning("User already exists during sign up")
            return 409, {"message": e.detail}
        except Exception:
            self.logger.error(
                "Unexpected error during sign up",
                exc_info=True,
            )
            raise HttpError(500, "Une erreur inattendue s'est produite")

    @http_post("/login", response={200: Token, 401: dict})
    def login(self, login_data: Login):
        try:
            use_case = LoginUseCase(self.user_repository)
            user = use_case.execute(login_data.email, login_data.password)
            if user:
                access_token, refresh_token = self.jwt_service.generate_tokens(
                    str(user.id)
                )
                return 200, Token(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_type="bearer",
                )
            raise AuthenticationError("Invalid credentials")
        except AuthenticationError as e:
            self.logger.warning("Authentication failed during login")
            return 401, {"message": str(e)}
        except Exception:
            self.logger.error(
                "Unexpected error during login",
                exc_info=True,
            )
            raise HttpError(500, "Une erreur inattendue s'est produite")

    @http_post("/refresh", response={200: Token, 401: dict}, auth=jwt_auth)
    def refresh_token(self, refresh_token: str):
        try:
            payload = self.jwt_service.decode_token(refresh_token)
            if payload and payload["token_type"] == "refresh":
                user_id = payload["user_id"]
                access_token, new_refresh_token = self.jwt_service.generate_tokens(
                    user_id
                )
                return 200, Token(
                    access_token=access_token,
                    refresh_token=new_refresh_token,
                    token_type="bearer",
                )
            self.logger.warning("Invalid refresh token attempt")
            return 401, {"message": "Invalid refresh token"}
        except Exception:
            self.logger.error(
                "Unexpected error during token refresh",
                exc_info=True,
            )
            raise HttpError(500, "Une erreur inattendue s'est produite")

    @http_get("/me", response=UserOut, auth=jwt_auth)
    def get_current_user(self, request):
        try:
            user_id = request.auth["user_id"]
            user = self.user_repository.get_user_by_id(user_id)
            return UserOut.from_orm(user)
        except ValidationError as e:
            self.logger.warning("Validation error during fetching current user")
            return 400, {"message": str(e)}
        except Exception:
            self.logger.error(
                "Unexpected error during fetching current user",
                exc_info=True,
            )
            raise HttpError(500, "Une erreur inattendue s'est produite")
