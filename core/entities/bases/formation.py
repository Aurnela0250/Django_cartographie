from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class FormationBaseEntity(BaseEntity):
    """Base entity for formation"""

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    duration: int
    level_id: int
    mention_id: int
    establishment_id: int
    authorization_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
