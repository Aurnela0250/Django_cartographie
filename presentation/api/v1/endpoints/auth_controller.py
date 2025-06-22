import logging
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.container.container import Container
from core.entities.user import UserEntity
from core.use_cases.auth_use_case import AuthUseCase
from presentation.constants.response_example import (
    current_user_responses,
    login_responses,
    logout_responses,
    refresh_token_responses,
    sign_up_responses,
)
from presentation.dependencies.auth_dependencies import get_current_user, oauth2_scheme
from presentation.exceptions import (
    ConflictException,
    InternalServerErrorException,
    UnauthorizedException,
)
from presentation.schemas.auth import Login, SignUpSchema, TokenSchema
from presentation.schemas.user import UserSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/signup",
    responses=sign_up_responses,
    status_code=201,
    response_model=UserSchema,
    summary="Sign up a new user",
    description="Endpoint to sign up a new user. Requires email and password. Returns user details",
    response_description="User details after successful sign up",
)
@inject
async def sign_up(
    user_data: SignUpSchema,
    auth_use_case: AuthUseCase = Depends(
        Provide[Container.auth_use_case],
    ),
) -> UserSchema:
    try:
        user_found = await auth_use_case.signup(
            user_data.email,
            user_data.password,
        )
        return UserSchema.model_validate(user_found)
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
    responses=login_responses,
)
@inject
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


# Endpoint pour Swagger/OAuth2
@router.post(
    "/token",
    responses=login_responses,
)
@inject
async def login_oauth2(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: AuthUseCase = Depends(
        Provide[Container.auth_use_case],
    ),
):
    try:
        token = await auth_use_case.login(
            form_data.username,
            form_data.password,
        )

        # OAuth2 attend ce format spécifique
        return {"access_token": token.access_token, "token_type": "bearer"}
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
    responses=refresh_token_responses,
)
@inject
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


@router.get(
    "/me",
    responses=current_user_responses,
)
def current_user(
    user: UserEntity = Depends(get_current_user),
):
    try:
        return UserSchema.model_validate(user)
    except UnauthorizedException as e:
        raise UnauthorizedException(cause=e)
    except Exception as e:
        print(f"Error getting current user: {e}")
        raise InternalServerErrorException(cause=e)


@router.post(
    "/logout",
    responses=logout_responses,
)
@inject
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
