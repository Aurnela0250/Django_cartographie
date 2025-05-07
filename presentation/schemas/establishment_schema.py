from datetime import datetime
from typing import List, Optional

from ninja import Schema
from pydantic.config import ConfigDict


class EstablishmentBaseSchema(Schema):
    """Base schema for establishment data"""

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


class CreateEstablishmentSchema(EstablishmentBaseSchema):
    """Schema for creating a new establishment"""

    pass


class UpdateEstablishmentSchema(Schema):
    """Schema for updating an establishment"""

    name: Optional[str] = None
    acronyme: Optional[str] = None
    address: Optional[str] = None
    code_postal: Optional[int] = None
    ville: Optional[str] = None
    contacts: Optional[List[str]] = None
    site_url: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: Optional[int] = None


class EstablishmentSchema(EstablishmentBaseSchema):
    """Schema for establishment responses"""

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
