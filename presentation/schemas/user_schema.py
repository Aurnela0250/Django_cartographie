from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict, EmailStr

from presentation.schemas.base_schema import BaseSchema


class UserBase(Schema):
    email: EmailStr


class UserCreate(Schema):
    email: EmailStr
    password: str


class UserSignUp(Schema):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: UUID
    email_verified: bool


class UserOut(UserInDB):
    pass


class ClientOut(UserOut):
    client_type: str


class UserAuthSchema(BaseSchema):
    id: Optional[int] = None
    email: EmailStr
    active: bool = True
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
