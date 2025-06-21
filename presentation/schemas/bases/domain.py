from datetime import datetime
from typing import Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema


class DomainBaseSchema(BaseSchema):
    """Base schema for domain"""

    id: int
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
