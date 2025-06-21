from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from presentation.schemas.bases.base import BaseSchema


class UserBaseSchema(BaseSchema):
    """Base schema for user"""

    id: int
    email: EmailStr
    active: bool = True
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
