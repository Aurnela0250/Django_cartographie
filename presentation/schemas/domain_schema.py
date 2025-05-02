from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DomainBase(BaseModel):
    name: str = Field(..., max_length=100)  # Added max_length
    description: Optional[str] = None


class DomainCreate(DomainBase):
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class DomainUpdate(DomainBase):
    name: Optional[str] = Field(None, max_length=100)  # Added max_length
    updated_by: Optional[int] = None


class DomainOut(DomainBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
