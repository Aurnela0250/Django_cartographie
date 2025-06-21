from pydantic import EmailStr

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.user import UserSchema


class Payload(BaseSchema):
    user_id: int
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
    user: UserSchema


class Login(BaseSchema):
    email: EmailStr
    password: str


class SignUpSchema(BaseSchema):
    email: EmailStr
    password: str
