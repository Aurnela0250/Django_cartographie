from pydantic import Field

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.rate import RateBaseSchema


class RateSchema(RateBaseSchema):
    id: int
    establishment_id: int
    user_id: int
    rating: float


class CreateRateSchema(BaseSchema):
    rating: float = Field(
        default=0,
        ge=0,
        le=5,
        description="Note entre 0 et 5",
    )
