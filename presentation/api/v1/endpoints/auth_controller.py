import logging

from ninja_extra import api_controller, http_get, http_post, route
from pydantic import ValidationError as PydanticValidationError

from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import JWTService, jwt_auth
from presentation.exceptions import (
    AuthenticationError,
    ConflictError,
    InternalServerError,
    InvalidTokenError,
    ValidationError,
)
from presentation.schemas.auth_schema import Login, TokenSchema
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.user_schema import UserAuthSchema, UserSignUp


@api_controller("/auth", tags=["Authentication"])
class AuthController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.jwt_service = JWTService()
        self.auth_use_case = AuthUseCase(
            self.unit_of_work,
            self.jwt_service,
        )
        self.logger = logging.getLogger(__name__)

    @route.post(
        "/signup",
        response={
            201: UserAuthSchema,
            422: ErrorResponseSchema,
            409: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def sign_up(self, user_data: UserSignUp):
        try:
            user_found = self.auth_use_case.signup(
                user_data.email,
                user_data.password,
            )
            return 201, UserAuthSchema.from_orm(user_found)
        except PydanticValidationError as e:
            self.logger.warning("Validation error during sign up")
            raise ValidationError(e)
        except ConflictError as e:
            self.logger.warning("User already exists during sign up")
            raise e
        except Exception:
            self.logger.error(
                "Unexpected error during sign up",
                exc_info=True,
            )
            raise InternalServerError()

    @route.post(
        "/login",
        response={
            200: TokenSchema,
            401: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def login(self, data: Login):
        try:
            use_case = self.auth_use_case
            token = use_case.login(data.email, data.password)

            response = TokenSchema.from_orm(token)

            return 200, response
        except PydanticValidationError as e:
            self.logger.warning("Validation error during login")
            raise ValidationError(e)
        except AuthenticationError:
            self.logger.warning("Authentication error during login")
            raise AuthenticationError()
        except Exception as e:
            self.logger.error(
                f"Unexpected error during login {e}",
                exc_info=True,
            )
            print(f"Unexpected error during login {e}")
            raise InternalServerError()

    @route.post(
        "/refresh",
        response={
            200: TokenSchema,
            401: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def refresh_token(self, refresh_token: str):
        self.logger.info("Refreshing token")
        try:
            new_token = self.auth_use_case.refresh_token(refresh_token)
            token = TokenSchema.from_orm(new_token)

            return (
                200,
                token,
            )
        except InvalidTokenError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error refreshing token: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_get("/me", response=UserAuthSchema, auth=jwt_auth)
    def get_current_user(self, request):
        try:
            user_id = request.auth["user_id"]
            user = self.auth_use_case.get_current_user(user_id)
            return UserAuthSchema.from_orm(user)
        except InvalidTokenError as e:
            raise e
        except Exception as e:
            print(f"Error getting current user: {e}")
            raise InternalServerError()

    @http_post(
        "/logout",
        response={
            200: dict,
            401: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
    )
    def logout(self, request, refresh_token: str):
        try:
            access_token = request.auth

            self.auth_use_case.logout(
                access_token,
                refresh_token,
            )

            return {"message": "Successfully logged out"}
        except InvalidTokenError as e:
            raise e
        except Exception as e:
            print(f"Unexpected error during logout {e}")
            self.logger.error("Error during logout", exc_info=True)
            raise InternalServerError()
