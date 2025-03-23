from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class SchoolYearEntity(BaseModel):
    id: Optional[int] = Field(default=None)
    start_year: int
    end_year: int
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    created_by: Optional[UUID] = Field(default=None)
    updated_by: Optional[UUID] = Field(default=None)

    class Config:
        from_attributes = True

    @field_validator("created_by", "updated_by", mode="before")
    @classmethod
    def parse_uuid(cls, value):
        if value is None:
            return None
        if isinstance(value, UUID):
            return value
        if isinstance(value, str):
            return UUID(value)
        if hasattr(value, "id"):
            return UUID(str(value.id))
        raise ValueError("Invalid UUID format")
