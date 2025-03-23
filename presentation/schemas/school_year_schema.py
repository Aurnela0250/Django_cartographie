from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import Field


class SchoolYearBaseSchema(Schema):
    start_year: int = Field(..., ge=1900, le=2100)
    end_year: int = Field(..., ge=1900, le=2100)


class SchoolYearSchema(SchoolYearBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None


class CreateSchoolYearSchema(SchoolYearBaseSchema):
    pass


class UpdateSchoolYearSchema(Schema):
    start_year: Optional[int] = Field(None, ge=1900, le=2100)
    end_year: Optional[int] = Field(None, ge=1900, le=2100)


class DeleteSchoolYearSchema(Schema):
    id: int
