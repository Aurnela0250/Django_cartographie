from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DomainEntity(BaseModel):
    id: Optional[int] = None
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
