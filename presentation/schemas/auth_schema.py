from pydantic import EmailStr

from presentation.schemas.base_schema import BaseSchema
from presentation.schemas.user_schema import UserAuthSchema


class Payload(BaseSchema):
    user_id: str
    exp: int
    iat: int
    jti: str
    token_type: str = "access"
    iss: str
    aud: str


class Token(Payload):
    access_token: str
    refresh_token: str


class TokenSchema(Token):
    user: UserAuthSchema


class Login(BaseSchema):
    email: EmailStr
    password: str


class SignUpSchema(BaseSchema):
    email: EmailStr
    password: str
