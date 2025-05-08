from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from ninja import Schema
from pydantic import ConfigDict, Field

from presentation.schemas.annual_headcount_schema import AnnualHeadcountResponse
from presentation.schemas.base_schema import BaseSchema
from presentation.schemas.formation_authorization_schema import (
    FormationAuthorizationSchema,
)
from presentation.schemas.level_schema import LevelOut
from presentation.schemas.mention_schema import MentionSchema

if TYPE_CHECKING:
    from presentation.schemas.establishment_schema import EstablishmentSchema


class FormationBaseSchema(Schema):
    intitule: str = Field(..., max_length=255)
    description: Optional[str] = Field(None)
    duration: int = Field(..., gt=0, description="Durée en mois")
    level_id: int = Field(..., gt=0)
    mention_id: int = Field(..., gt=0)
    establishment_id: int = Field(..., gt=0)
    authorization_id: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(from_attributes=True)


class CreateFormationSchema(FormationBaseSchema):
    pass


class UpdateFormationSchema(Schema):
    intitule: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    duration: Optional[int] = Field(None, gt=0)
    level_id: Optional[int] = Field(None, gt=0)
    mention_id: Optional[int] = Field(None, gt=0)
    establishment_id: Optional[int] = Field(None, gt=0)
    authorization_id: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(from_attributes=True)


class FormationSchema(BaseSchema):
    id: int
    intitule: str
    description: Optional[str] = None
    duration: int
    level_id: int
    mention_id: int
    establishment_id: int
    authorization_id: Optional[int] = None
    level: Optional[LevelOut] = None
    mention: Optional[MentionSchema] = None
    establishment: Optional["EstablishmentSchema"] = None
    authorization: Optional[FormationAuthorizationSchema] = None
    annual_headcounts: List[AnnualHeadcountResponse] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
