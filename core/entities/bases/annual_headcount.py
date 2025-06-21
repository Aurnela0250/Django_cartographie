from datetime import datetime
from typing import Optional

from core.entities.bases.base import BaseEntity


class AnnualHeadcountBaseEntity(BaseEntity):
    """Base entity for annual headcount"""

    id: Optional[int] = None
    formation_id: int
    academic_year: int
    students: int
    success_rate: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
