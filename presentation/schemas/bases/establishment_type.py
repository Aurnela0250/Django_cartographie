from datetime import datetime
from typing import Optional

from presentation.schemas.bases.base import BaseSchema


class EstablishmentTypeBaseSchema(BaseSchema):
    """Base schema for establishment type"""

    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
