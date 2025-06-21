from datetime import datetime
from typing import Optional

from presentation.schemas.bases.base import BaseSchema


class FormationBaseSchema(BaseSchema):
    """Base schema for formation"""

    id: int
    name: str
    description: Optional[str] = None
    duration: int
    level_id: int
    mention_id: int
    establishment_id: int
    authorization_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
