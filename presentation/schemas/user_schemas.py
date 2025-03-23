from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr


class UserBase(Schema):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: UUID
    email_verified: bool

    class Config:
        orm_mode = True


class UserOut(UserInDB):
    pass


class ClientOut(UserOut):
    client_type: str
