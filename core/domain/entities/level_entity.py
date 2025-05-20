from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LevelEntity(BaseModel):
    """Entity representing a level"""

    id: Optional[int] = None
    name: str
    acronyme: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
