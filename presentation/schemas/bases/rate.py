from presentation.schemas.bases.base import BaseSchema


class RateBaseSchema(BaseSchema):
    """Base schema for rating an establishment"""

    id: int
    establishment_id: int
    user_id: int
    rating: float
