from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from ninja import Field, Schema
from pydantic.config import ConfigDict
from pydantic.main import BaseModel

from presentation.schemas.establishment_type_schema import EstablishmentTypeSchema
from presentation.schemas.sector_schema import SectorOut

if TYPE_CHECKING:
    from presentation.schemas.formation_schema import FormationSchema


class EstablishmentBaseSchema(Schema):
    """Base schema for establishment data"""

    name: str
    acronyme: Optional[str] = None
    address: str
    contacts: Optional[List[str]] = None
    site_url: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: int
    sector_id: int

    model_config = ConfigDict(from_attributes=True)


class CreateEstablishmentSchema(EstablishmentBaseSchema):
    """Schema for creating a new establishment"""

    pass


class UpdateEstablishmentSchema(Schema):
    """Schema for updating an establishment"""

    name: Optional[str] = None
    acronyme: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[List[str]] = None
    site_url: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: Optional[int] = None
    sector_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class EstablishmentSchema(EstablishmentBaseSchema):
    """Schema for establishment responses"""

    id: int
    establishment_type: Optional[EstablishmentTypeSchema] = None
    sector: Optional[SectorOut] = None
    formations: Optional[list["FormationSchema"]] = []
    rating: float = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class RateEstablishmentSchema(Schema):
    """Schema pour noter un établissement"""

    rating: float = Field(..., ge=0, le=5)

    model_config = ConfigDict(from_attributes=True)


class EstablishmentFilterParamsSchema(BaseModel):
    """Schema for filtering establishments"""

    name: Optional[str] = None
    acronyme: Optional[str] = None
    establishment_type_id: Optional[int] = None
    city_id: Optional[int] = None
    region_id: Optional[int] = None
    domain_id: Optional[int] = None  # Filtre par domaine
    level_id: Optional[int] = None  # Nouveau filtre par niveau
