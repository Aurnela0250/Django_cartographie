from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class MentionBaseEntity(BaseEntity):
    """Base entity for mentions"""

    id: Optional[int] = None
    name: str
    domain_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
