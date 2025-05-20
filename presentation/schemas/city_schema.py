from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import ConfigDict


class CitySchema(Schema):
    id: int
    name: str
    region_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CreateCitySchemaRequest(Schema):
    name: str
    region_id: int


class CreateCitySchemaResponse(CitySchema):
    pass


class UpdateCitySchema(Schema):
    name: Optional[str] = None
    region_id: Optional[int] = None
