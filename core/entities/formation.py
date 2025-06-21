from typing import Optional, Sequence

from core.entities.bases.annual_headcount import AnnualHeadcountBaseEntity
from core.entities.bases.establishment import EstablishmentBaseEntity
from core.entities.bases.formation import FormationBaseEntity
from core.entities.bases.formation_authorization import FormationAuthorizationBaseEntity
from core.entities.bases.level import LevelBaseEntity
from core.entities.bases.mention import MentionBaseEntity


class FormationEntity(FormationBaseEntity):
    """Entity representing a formation"""

    level: Optional[LevelBaseEntity] = None
    mention: Optional[MentionBaseEntity] = None
    establishment: Optional[EstablishmentBaseEntity] = None
    authorization: Optional[FormationAuthorizationBaseEntity] = None
    annual_headcounts: Sequence[AnnualHeadcountBaseEntity] = []
