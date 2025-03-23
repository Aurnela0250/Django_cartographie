from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema


class UserEntity(Schema):
    id: Optional[UUID] = None
    email: str
    username: str
    password: str
    active: bool = True
    email_verified: bool = False
    is_two_factor_enabled: bool = False
    image: Optional[str] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ClientEntity(UserEntity):
    client_type: str

    class Config:
        orm_mode = True
