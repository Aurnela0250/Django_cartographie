from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class EstablishmentTypeBaseEntity(BaseEntity):
    """Base entity for establishment type"""

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
