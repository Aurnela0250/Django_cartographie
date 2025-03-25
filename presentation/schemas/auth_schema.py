from datetime import datetime
from typing import Optional

from ninja import Schema


class AccessToken(Schema):
    access_token: str
    expires_in: int


class RefreshToken(Schema):
    refresh_token: str
    expires_in: Optional[int] = None


class Token(Schema):
    access_token: AccessToken
    refresh_token: Optional[RefreshToken] = None
    token_type: str
    iat: datetime


class TokenPayload(Schema):
    user_id: str
    exp: int
    iat: int
    token_type: str


class TokenData(Schema):
    email: Optional[str] = None


class Login(Schema):
    email: str
    password: str
