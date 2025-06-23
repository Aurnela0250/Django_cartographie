from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.container.container import Container
from core.entities.user import UserEntity
from infrastructure.db.tortoise.user_repository_impl import UserRepository
from infrastructure.external_services.jwt_service import JWTService
from presentation.constants import errors_code
from presentation.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    """Extrait le token depuis l'en-tête Authorization"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    return authorization.split(" ")[1]


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: JWTService = Depends(Provide[Container.jwt_service]),
    auth_use_case: UserRepository = Depends(Provide[Container.user_repository]),
) -> UserEntity:
    """Récupère l'utilisateur actuel depuis le token"""
    payload = await jwt_service.decode_access_token(token)

    user = await auth_use_case.get(payload.user_id)
    if user is None:
        raise UnauthorizedException(code=errors_code.INVALID_TOKEN)

    return user
