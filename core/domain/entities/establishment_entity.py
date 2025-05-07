from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class EstablishmentEntity(BaseModel):
    """Entity representing an establishment"""

    id: Optional[int] = None
    name: str
    acronyme: Optional[str] = None
    address: str
    code_postal: int
    ville: str
    contacts: Optional[List[str]] = None
    site_url: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    establishment_type_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
