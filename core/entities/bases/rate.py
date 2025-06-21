from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class RateBaseEntity(BaseEntity):
    """Base entity for rating an establishment"""

    id: Optional[int] = None
    establishment_id: int
    user_id: int
    rating: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
