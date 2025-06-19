from pydantic import Field

from presentation.schemas.base_schema import BaseSchema


class RateSchema(BaseSchema):
    id: int
    establishment_id: int
    user_id: int
    rating: float


class CreateRateSchema(BaseSchema):
    rating: float = Field(..., ge=0, le=5, description="Note entre 0 et 5")
