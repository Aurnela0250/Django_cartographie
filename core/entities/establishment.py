from typing import List, Optional

from core.entities.bases.city import CityBaseEntity
from core.entities.bases.establishment import EstablishmentBaseEntity
from core.entities.bases.establishment_type import EstablishmentTypeBaseEntity
from core.entities.bases.formation import FormationBaseEntity


class EstablishmentEntity(EstablishmentBaseEntity):
    """Entity representing an establishment"""

    establishment_type: Optional[EstablishmentTypeBaseEntity] = None
    city: Optional[CityBaseEntity] = None
    formations: Optional[List[FormationBaseEntity]] = []
