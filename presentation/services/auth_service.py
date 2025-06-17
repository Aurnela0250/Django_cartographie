from typing import Optional

from fastapi import Depends, HTTPException, Header, status


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


async def get_current_user(token: str = Depends(get_token_from_header)) -> User:
    """Récupère l'utilisateur actuel depuis le token"""
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    user = get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return User(username=user.username, email=user.email, disabled=user.disabled)
