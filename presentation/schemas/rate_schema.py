from pydantic import BaseModel, ConfigDict, Field


class RateSchema(BaseModel):
    id: int
    establishment_id: int
    user_id: int
    rating: float

    model_config = ConfigDict(from_attributes=True)


class CreateRateSchema(BaseModel):
    rating: float = Field(..., ge=0, le=5, description="Note entre 0 et 5")
    model_config = ConfigDict(from_attributes=True)
