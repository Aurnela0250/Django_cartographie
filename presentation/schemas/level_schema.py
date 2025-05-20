from datetime import datetime
from typing import Optional

from pydantic import Field

from presentation.schemas.base_schema import BaseSchema


class LevelBase(BaseSchema):
    """Base schema for level data"""

    name: str = Field(..., description="Name of the level")
    acronyme: Optional[str] = Field(None, description="Acronym of the level")


class LevelCreate(LevelBase):
    """Schema for creating a level"""

    pass


class LevelUpdate(LevelBase):
    """Schema for updating a level"""

    name: Optional[str] = Field(None, description="Name of the level")
    acronyme: Optional[str] = Field(None, description="Acronym of the level")


class LevelOut(LevelBase):
    """Schema for displaying a level"""

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
