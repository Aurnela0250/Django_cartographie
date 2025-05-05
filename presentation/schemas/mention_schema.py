from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import ConfigDict, Field

from presentation.schemas.base_schema import BaseSchema


class MentionBase(Schema):
    name: str = Field(..., min_length=1, max_length=255)
    domain_id: int = Field(..., gt=0)


class CreateMentionSchema(MentionBase):
    pass


class UpdateMentionSchema(Schema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    domain_id: Optional[int] = Field(None, gt=0)


class MentionSchema(BaseSchema):
    id: int
    name: str
    domain_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
