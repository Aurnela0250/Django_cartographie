from typing import Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.mention import MentionBaseSchema


class MentionSchema(MentionBaseSchema):
    pass


class CreateMentionSchema(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    domain_id: int = Field(..., gt=0)


class UpdateMentionSchema(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    domain_id: Optional[int] = Field(None, gt=0)
