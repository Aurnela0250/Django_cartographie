from pydantic import BaseModel, ConfigDict

from core.domain.entities.user_entity import UserEntity


class TokenEntity(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    exp: int
    iat: int
    user: UserEntity

    class Config:
        model_config = ConfigDict(from_attributes=True)
