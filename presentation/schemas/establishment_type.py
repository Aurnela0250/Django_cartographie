from typing import Optional

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.establishment_type import EstablishmentTypeBaseSchema


class EstablishmentTypeSchema(EstablishmentTypeBaseSchema):
    """Schema for establishment type responses"""

    pass


class CreateEstablishmentTypeSchema(BaseSchema):
    """Schema for creating a new establishment type"""

    name: str
    description: Optional[str] = None


class UpdateEstablishmentTypeSchema(BaseSchema):
    """Schema for updating an establishment type"""

    name: Optional[str] = None
    description: Optional[str] = None
