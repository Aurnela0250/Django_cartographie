from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

from core.domain.entities.annual_headcount_entity import AnnualHeadCountEntity
from core.domain.entities.formation_authorization_entity import (
    FormationAuthorizationEntity,
)
from core.domain.entities.level_entity import LevelEntity
from core.domain.entities.mention_entity import MentionEntity

if TYPE_CHECKING:
    from core.domain.entities.establishment_entity import (
        EstablishmentEntity,
    )


class FormationEntity(BaseModel):
    id: Optional[int] = None
    intitule: str
    description: Optional[str] = None
    duration: int
    level_id: int
    mention_id: int
    establishment_id: int
    authorization_id: Optional[int] = None

    level: Optional[LevelEntity] = None
    mention: Optional[MentionEntity] = None
    establishment: Optional["EstablishmentEntity"] = None
    authorization: Optional[FormationAuthorizationEntity] = None
    annual_headcounts: List[AnnualHeadCountEntity] = []

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
