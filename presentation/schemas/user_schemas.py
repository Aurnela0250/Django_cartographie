from typing import Optional

from ninja import Schema
from pydantic import EmailStr


class UserBase(Schema):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserOut(UserBase):
    pass
