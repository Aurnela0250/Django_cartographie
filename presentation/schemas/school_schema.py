from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from ninja import Schema
from pydantic import Field

CYCLE_CHOICES = Literal["Primaire", "Secondaire", "Lycée"]
PARCOURS_CHOICES = Literal["GENERAL", "TECHNIQUE", "PROFESSIONEL"]
STATUS_CHOICES = Literal["PRIVE", "PUBLIC"]


class SchoolBaseSchema(Schema):
    name: str = Field(..., min_length=1, max_length=255)
    status: STATUS_CHOICES
    description: str
    address: str = Field(..., max_length=255)
    parcours: PARCOURS_CHOICES
    cycle: CYCLE_CHOICES
    image_url: Optional[str] = None


class SchoolSchema(SchoolBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None


class CreateSchoolSchema(SchoolBaseSchema):
    pass


class UpdateSchoolSchema(Schema):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
    )
    status: Optional[STATUS_CHOICES] = None
    description: Optional[str] = None
    address: Optional[str] = Field(
        None,
        max_length=255,
    )
    parcours: Optional[PARCOURS_CHOICES] = None
    cycle: Optional[CYCLE_CHOICES] = None
    image_url: Optional[str] = None


class DeleteSchoolSchema(Schema):
    id: UUID
