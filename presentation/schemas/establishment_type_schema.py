from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic.config import ConfigDict


class EstablishmentTypeBaseSchema(Schema):
    """Base schema for establishment type data"""

    name: str
    description: Optional[str] = None


class CreateEstablishmentTypeSchema(EstablishmentTypeBaseSchema):
    """Schema for creating a new establishment type"""

    pass


class UpdateEstablishmentTypeSchema(Schema):
    """Schema for updating an establishment type"""

    name: Optional[str] = None
    description: Optional[str] = None


class EstablishmentTypeSchema(EstablishmentTypeBaseSchema):
    """Schema for establishment type responses"""

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)
