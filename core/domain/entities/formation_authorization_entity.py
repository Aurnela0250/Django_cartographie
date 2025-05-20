from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FormationAuthorizationEntity(BaseModel):
    id: Optional[int] = None
    date_debut: date
    date_fin: Optional[date] = None
    status: str
    arrete: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
