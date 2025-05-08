from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from core.domain.entities.establishment_type_entity import EstablishmentTypeEntity
from core.domain.entities.sector_entity import SectorEntity

if TYPE_CHECKING:
    from core.domain.entities.formation_entity import FormationEntity


class EstablishmentEntity(BaseModel):
    """Entity representing an establishment"""

    id: Optional[int] = None
    name: str
    acronyme: Optional[str] = None
    address: str
    code_postal: int
    ville: str
    contacts: Optional[List[str]] = None
    site_url: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: int
    establishment_type: Optional[EstablishmentTypeEntity] = None
    sector_id: int
    sector: Optional[SectorEntity] = None
    formations: Optional[List["FormationEntity"]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
