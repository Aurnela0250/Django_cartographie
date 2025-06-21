from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class CityBaseEntity(BaseEntity):
    """Base entity for city"""

    id: Optional[int] = None
    name: str
    region_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
