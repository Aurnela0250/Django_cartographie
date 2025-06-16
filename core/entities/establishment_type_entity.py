from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EstablishmentTypeEntity(BaseModel):
    """Entity representing an establishment type"""

    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
