from typing import List, Optional

from presentation.schemas.bases.base import BaseSchema


class EstablishmentBaseSchema(BaseSchema):
    """Base schema for establishment"""

    id: int
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
