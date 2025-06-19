from datetime import datetime
from typing import Optional

from presentation.schemas.base_schema import BaseSchema


class CitySchema(BaseSchema):
    id: int
    name: str
    region_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class CreateCitySchemaRequest(BaseSchema):
    name: str
    region_id: int


class CreateCitySchemaResponse(CitySchema):
    pass


class UpdateCitySchema(BaseSchema):
    name: Optional[str] = None
    region_id: Optional[int] = None
