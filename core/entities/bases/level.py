from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class LevelBaseEntity(BaseEntity):
    """Base entity for level"""

    id: Optional[int] = None
    name: str
    acronym: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
