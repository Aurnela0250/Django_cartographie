from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from presentation.schemas.base_schema import BaseSchema
from presentation.schemas.city_schema import CitySchema
from presentation.schemas.establishment_type_schema import EstablishmentTypeSchema

if TYPE_CHECKING:
    from presentation.schemas.formation_schema import FormationSchema


class EstablishmentBaseSchema(BaseSchema):
    """Base schema for establishment data"""

    name: str
    acronym: Optional[str] = None
    address: str
    contacts: Optional[List[str]] = None
    website: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: int
    city_id: int


class CreateEstablishmentSchema(EstablishmentBaseSchema):
    """Schema for creating a new establishment"""

    pass


class UpdateEstablishmentSchema(EstablishmentBaseSchema):
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
    city_id: Optional[int] = None


class EstablishmentSchema(EstablishmentBaseSchema):
    """Schema for establishment responses"""

    id: int
    establishment_type: Optional[EstablishmentTypeSchema] = None
    city: Optional[CitySchema] = None
    formations: Optional[list["FormationSchema"]] = []
    rating: float = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class RateEstablishmentSchema(BaseSchema):
    """Schema pour noter un établissement"""

    rating: float = Field(..., ge=0, le=5)


class EstablishmentFilterParamsSchema(BaseSchema):
    """Schema for filtering establishments"""

    name: Optional[str] = None
    acronym: Optional[str] = None
    establishment_type_id: Optional[int] = None
    city_id: Optional[int] = None
    region_id: Optional[int] = None
    domain_id: Optional[int] = None  # Filtre par domaine
    level_id: Optional[int] = None  # Nouveau filtre par niveau
