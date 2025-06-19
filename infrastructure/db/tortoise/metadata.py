from typing import Optional

from pydantic import BaseModel


class EstablishmentToEntityMetadata(BaseModel):
    establishment_type: Optional[bool] = False
    city: Optional[bool] = False
    formations: Optional[bool] = False


class FormationToEntityMetadata(BaseModel):
    level: Optional[bool] = False
    mention: Optional[bool] = False
    establishment: Optional[bool] = False
    authorization: Optional[bool] = False
