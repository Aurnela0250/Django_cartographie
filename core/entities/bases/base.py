from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        loc_by_alias=True,
        json_encoders={datetime: lambda v: v.isoformat() if v is not None else None},
    )
