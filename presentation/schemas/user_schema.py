from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from presentation.schemas.base_schema import BaseSchema


class UserBase(BaseSchema):
    email: EmailStr


class UserCreate(BaseSchema):
    email: EmailStr
    password: str


class UserSignUp(BaseSchema):
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
