from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RateEntity(BaseModel):
    """Entity representing a user vote for an establishment"""

    id: Optional[int] = None
    establishment_id: int
    user_id: int
    rating: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
