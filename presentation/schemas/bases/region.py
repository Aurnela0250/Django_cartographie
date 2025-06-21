from datetime import datetime
from typing import Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema


class RegionBaseSchema(BaseSchema):
    """Schema base for regions"""

    id: int
    name: str = Field(..., description="Name of the region")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
