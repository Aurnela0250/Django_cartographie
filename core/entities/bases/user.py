from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class UserBaseEntity(BaseEntity):
    """Base entity for user"""

    id: Optional[int] = None
    email: str
    password: str
    active: bool = True
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
