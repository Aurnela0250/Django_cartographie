from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserEntity(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    active: bool = True
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
