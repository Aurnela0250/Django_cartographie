# Entité représentant un secteur
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SectorEntity(BaseModel):
    """Entité représentant un secteur"""

    id: Optional[int] = None
    name: str
    region_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
