from datetime import datetime
from typing import Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema


class LevelBaseSchema(BaseSchema):
    """Base schema for level"""

    id: int
    name: str = Field(..., description="Name of the level")
    acronym: Optional[str] = Field(None, description="Acronym of the level")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
