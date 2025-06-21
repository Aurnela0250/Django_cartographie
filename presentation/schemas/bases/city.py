from datetime import datetime
from typing import Optional

from presentation.schemas.bases.base import BaseSchema


class CityBaseSchema(BaseSchema):
    """Base schema for city"""

    id: int
    name: str
    region_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
