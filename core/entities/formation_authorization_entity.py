from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FormationAuthorizationEntity(BaseModel):
    id: Optional[int] = None
    issued_date: date
    expiry_date: Optional[date] = None
    status: str
    decree: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
