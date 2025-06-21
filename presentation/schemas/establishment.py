from typing import List, Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.city import CityBaseSchema
from presentation.schemas.bases.establishment import EstablishmentBaseSchema
from presentation.schemas.bases.establishment_type import EstablishmentTypeBaseSchema
from presentation.schemas.bases.formation import FormationBaseSchema


class EstablishmentSchema(EstablishmentBaseSchema):
    """Schema for establishment responses"""

    establishment_type: Optional[EstablishmentTypeBaseSchema] = None
    city: Optional[CityBaseSchema] = None
    formations: Optional[List[FormationBaseSchema]] = []


class CreateEstablishmentSchema(BaseSchema):
    """Schema for creating a new establishment"""

    name: str
    acronym: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[List[str]] = None
    website: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: int
    city_id: int


class UpdateEstablishmentSchema(BaseSchema):
    """Schema for updating an establishment"""

    name: str
    acronym: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[List[str]] = None
    website: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: int
    city_id: int


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
    domain_id: Optional[int] = None
