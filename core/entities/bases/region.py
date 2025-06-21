from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class RegionBaseEntity(BaseEntity):
    """Entity base for regions"""

    id: Optional[int] = None
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
