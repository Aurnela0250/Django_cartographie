import logging

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from core.container.container import Container
from core.entities.user_entity import UserEntity
from core.use_cases.auth_use_case import AuthUseCase
from presentation.dependencies.auth_dependencies import (
    get_current_user,
    oauth2_scheme,
)
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    UnauthorizedException,
)
from presentation.schemas.auth_schema import Login, SignUpSchema, TokenSchema
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.user_schema import UserAuthSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth", "Authentication", "authentication", "auth"],
)


@router.post(
    "/signup",
    responses={
        201: {
            "model": UserAuthSchema,
            "description": "User created successfully",
            "content": {
                "application/json": {
                    # "schema": UserAuthSchema,
                },
            },
        },
    },
    status_code=201,
    response_model=UserAuthSchema,
    summary="Sign up a new user",
    description="Endpoint to sign up a new user. Requires email and password. Returns user details",
    response_description="User details after successful sign up",
)
async def sign_up(
    user_data: SignUpSchema,
    auth_use_case: AuthUseCase = Depends(
        Provide[Container.auth_use_case],
    ),
) -> UserAuthSchema:
    try:
        user_found = await auth_use_case.signup(
            user_data.email,
            user_data.password,
        )
        return UserAuthSchema.model_validate(user_found)
    # except PydanticValidationError as e:
    #     logger.warning("Validation error during sign up")
    #     raise ValidationError(e)
    except ConflictException as e:
        logger.warning("User already exists during sign up")
        raise ConflictException(cause=e)
    except Exception as e:
        logger.error(
            "Unexpected error during sign up",
            exc_info=True,
        )
        raise InternalServerErrorException(cause=e)


@router.post(
    "/login",
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "schema": TokenSchema,
                },
            },
        },
        401: {
            "description": "Authentication error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
    },
)
async def login(
    data: Login,
    auth_use_case: AuthUseCase = Depends(
        Provide[Container.auth_use_case],
    ),
):
    try:
        token = await auth_use_case.login(
            data.email,
            data.password,
        )

        response = TokenSchema.model_validate(token)

        return response
    except UnauthorizedException as e:
        logger.warning("Authentication error during login")
        raise UnauthorizedException(cause=e)
    except Exception as e:
        logger.error(
            f"Unexpected error during login {e}",
            exc_info=True,
        )
        print(f"Unexpected error during login {e}")
        raise InternalServerErrorException(cause=e)


@router.post(
    "/refresh",
    responses={
        200: {
            "description": "Refresh successful",
            "content": {
                "application/json": {
                    "schema": TokenSchema,
                },
            },
        },
        401: {
            "description": "Authentication error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
    },
)
async def refresh_token(
    refresh_token: str,
    auth_use_case: AuthUseCase = Depends(
        Provide[Container.auth_use_case],
    ),
):
    logger.info("Refreshing token")
    try:
        new_token = await auth_use_case.refresh_token(refresh_token)
        token = TokenSchema.model_validate(new_token)

        return token
    except UnauthorizedException as e:
        raise UnauthorizedException(cause=e)
    except Exception as e:
        logger.error(
            f"Error refreshing token: {str(e)}",
            exc_info=True,
        )
        raise InternalServerErrorException(cause=e)


@router.get("/me")
def current_user(
    user: UserEntity = Depends(get_current_user),
):
    try:
        return UserAuthSchema.model_validate(user)
    except UnauthorizedException as e:
        raise UnauthorizedException(cause=e)
    except Exception as e:
        print(f"Error getting current user: {e}")
        raise InternalServerErrorException(cause=e)


@router.post(
    "/logout",
    responses={
        200: {
            "description": "Logout successful",
            "content": {
                "application/json": {
                    "schema": dict,
                },
            },
        },
        401: {
            "description": "Authentication error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "schema": ErrorResponseSchema,
                },
            },
        },
    },
)
async def logout(
    refresh_token: str,
    auth_use_case: AuthUseCase = Depends(
        Provide[Container.auth_use_case],
    ),
    access_token: str = Depends(oauth2_scheme),
):
    try:

        await auth_use_case.logout(
            access_token,
            refresh_token,
        )

        return {"message": "Successfully logged out"}
    except InternalServerErrorException as e:
        raise InternalServerErrorException(cause=e)
    except Exception as e:
        print(f"Unexpected error during logout {e}")
        logger.error("Error during logout", exc_info=True)
        raise InternalServerErrorException(cause=e)
