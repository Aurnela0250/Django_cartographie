from datetime import datetime

from pydantic import BaseModel, Field


class CreateRateSchema(BaseModel):
    rating: float = Field(
        ..., ge=0.0, le=5.0, description="Rating value between 0.0 and 5.0"
    )


class RateSchema(BaseModel):
    id: int
    establishment_id: int
    user_id: int
    rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
