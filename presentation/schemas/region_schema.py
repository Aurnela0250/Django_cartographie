from datetime import datetime
from typing import Optional
from pydantic import Field

from presentation.schemas.base_schema import BaseSchema


class RegionBase(BaseSchema):
    """Schéma de base pour les données de région"""

    name: str = Field(..., description="Nom de la région")
    code: Optional[str] = Field(None, description="Code de la région (ex: code INSEE)")


class RegionCreate(RegionBase):
    """Schéma pour la création d'une région"""

    pass


class RegionUpdate(RegionBase):
    """Schéma pour la mise à jour d'une région"""

    name: Optional[str] = Field(None, description="Nom de la région")


class RegionOut(RegionBase):
    """Schéma pour l'affichage d'une région"""

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
