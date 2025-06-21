from typing import Optional

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.city import CityBaseSchema


class CitySchema(CityBaseSchema):
    pass


class CreateCitySchema(BaseSchema):
    name: str
    region_id: int


class UpdateCitySchema(BaseSchema):
    name: Optional[str] = None
    region_id: Optional[int] = None
