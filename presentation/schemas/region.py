from typing import Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.region import RegionBaseSchema


class RegionSchema(RegionBaseSchema):
    """Schéma de base pour les données de région"""

    pass


class CreateRegionSchema(BaseSchema):
    """Schéma pour la création d'une région"""

    name: str = Field(..., description="Nom de la région")


class UpdateRegionSchema(BaseSchema):
    """Schéma pour la mise à jour d'une région"""

    name: Optional[str] = Field(None, description="Nom de la région")
