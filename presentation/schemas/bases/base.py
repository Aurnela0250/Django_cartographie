from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        loc_by_alias=True,
        alias_generator=to_camel,
        json_encoders={datetime: lambda v: v.isoformat() if v is not None else None},
    )
