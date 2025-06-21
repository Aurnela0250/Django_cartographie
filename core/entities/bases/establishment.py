from datetime import datetime
from typing import List, Optional

from core.entities.bases.base import BaseEntity


class EstablishmentBaseEntity(BaseEntity):
    """Base entity for establishment"""

    id: Optional[int] = None
    name: str
    acronym: Optional[str] = None
    address: str
    contacts: Optional[List[str]] = None
    website: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: float = 0
    establishment_type_id: int
    city_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
