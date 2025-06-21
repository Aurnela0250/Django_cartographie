from datetime import datetime
from typing import Optional

from presentation.schemas.bases.base import BaseSchema


class MentionBaseSchema(BaseSchema):
    """Base schema for mentions"""

    id: int
    name: str
    domain_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
