from typing import Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.domain import DomainBaseSchema


class DomainSchema(DomainBaseSchema):
    pass


class CreateDomainSchema(BaseSchema):
    name: str = Field(..., max_length=100)


class UpdateDomainSchema(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
