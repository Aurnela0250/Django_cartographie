from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema


class UserEntity(Schema):
    id: Optional[UUID] = None
    email: str
    password: str
    active: bool = True
    updated_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
