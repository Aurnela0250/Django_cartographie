from typing import Optional

from ninja import Schema


class Token(Schema):
    access_token: str
    refresh_token: str
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
