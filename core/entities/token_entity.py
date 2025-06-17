from pydantic import BaseModel, ConfigDict

from core.entities.user_entity import UserEntity


class Payload(BaseModel):
    user_id: int
    exp: int
    iat: int
    jti: str
    token_type: str = "access"
    iss: str
    aud: str

    class Config:
        model_config = ConfigDict(from_attributes=True)


class Token(Payload):
    access_token: str
    refresh_token: str

    class Config:
        model_config = ConfigDict(from_attributes=True)


class TokenEntity(Token):
    user: UserEntity

    class Config:
        model_config = ConfigDict(from_attributes=True)
