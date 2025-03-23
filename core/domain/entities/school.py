from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema


class SchoolEntity(Schema):
    id: UUID | None = None
    name: str
    # code: str
    status: str
    description: str
    address: str
    parcours: str
    cycle: str
    image_url: Optional[str] = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True
        orm_mode = True
