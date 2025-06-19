from datetime import datetime
from typing import Optional

from presentation.schemas.base_schema import BaseSchema


class EstablishmentTypeBaseSchema(BaseSchema):
    """Base schema for establishment type data"""

    name: str
    description: Optional[str] = None


class CreateEstablishmentTypeSchema(EstablishmentTypeBaseSchema):
    """Schema for creating a new establishment type"""

    pass


class UpdateEstablishmentTypeSchema(BaseSchema):
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
