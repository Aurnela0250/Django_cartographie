from typing import Optional

from ninja import Schema


class Token(Schema):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


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


class RefreshToken(Schema):
    refresh_token: str
