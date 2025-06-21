from typing import List, Optional

from pydantic import Field

from presentation.schemas.bases.annual_headcount import AnnualHeadcountBaseSchema
from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.establishment import EstablishmentBaseSchema
from presentation.schemas.bases.formation import FormationBaseSchema
from presentation.schemas.bases.formation_authorization import (
    FormationAuthorizationBaseSchema,
)
from presentation.schemas.bases.level import LevelBaseSchema
from presentation.schemas.bases.mention import MentionBaseSchema


class FormationSchema(FormationBaseSchema):
    """Schema for formation responses"""

    level: Optional[LevelBaseSchema] = None
    mention: Optional[MentionBaseSchema] = None
    establishment: Optional[EstablishmentBaseSchema] = None
    authorization: Optional[FormationAuthorizationBaseSchema] = None
    annual_headcounts: List[AnnualHeadcountBaseSchema] = []


class CreateFormationSchema(BaseSchema):
    """Schema for creating a new formation"""

    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    duration: int = Field(..., gt=0)
    level_id: int = Field(..., gt=0)
    mention_id: int = Field(..., gt=0)
    establishment_id: int = Field(..., gt=0)
    authorization_id: Optional[int] = Field(None, gt=0)


class UpdateFormationSchema(BaseSchema):
    """Schema for updating a formation"""

    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    duration: Optional[int] = Field(None, gt=0)
    level_id: Optional[int] = Field(None, gt=0)
    mention_id: Optional[int] = Field(None, gt=0)
    establishment_id: Optional[int] = Field(None, gt=0)
    authorization_id: Optional[int] = Field(None, gt=0)
