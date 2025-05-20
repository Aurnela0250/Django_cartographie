from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnnualHeadCountEntity(BaseModel):
    id: Optional[int] = None
    formation_id: int
    academic_year: int
    students: int
    success_rate: Optional[float] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
