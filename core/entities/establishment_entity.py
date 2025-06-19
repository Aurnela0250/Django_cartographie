from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from core.entities.city_entity import CityEntity
from core.entities.establishment_type_entity import EstablishmentTypeEntity

if TYPE_CHECKING:
    from core.entities.formation_entity import FormationEntity


class EstablishmentEntity(BaseModel):
    """Entity representing an establishment"""

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
    establishment_type: Optional[EstablishmentTypeEntity] = None
    city_id: int
    city: Optional[CityEntity] = None
    formations: Optional[List["FormationEntity"]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
