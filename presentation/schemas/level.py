from typing import Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.level import LevelBaseSchema


class LevelSchema(LevelBaseSchema):
    """Base schema for level data"""

    pass


class CreateLevelSchema(BaseSchema):
    """Schema for creating a level"""

    name: str = Field(..., description="Name of the level")
    acronym: Optional[str] = Field(None, description="Acronym of the level")


class UpdateLevelSchema(BaseSchema):
    """Schema for updating a level"""

    name: Optional[str] = Field(None, description="Name of the level")
    acronym: Optional[str] = Field(None, description="Acronym of the level")
