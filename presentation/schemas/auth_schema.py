from typing import Optional

from ninja import Schema

from presentation.schemas.base_schema import BaseSchema
from presentation.schemas.user_schema import UserAuthSchema


class TokenSchema(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    exp: int
    iat: int
    user: UserAuthSchema


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
