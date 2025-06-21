from datetime import date, datetime
from typing import Optional

from presentation.schemas.bases.base import BaseSchema


class FormationAuthorizationBaseSchema(BaseSchema):
    """Base schema for formation authorization"""

    id: int
    date_debut: date
    date_fin: Optional[date] = None
    status: str
    decree: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
