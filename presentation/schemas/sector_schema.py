from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field

from presentation.schemas.base_schema import BaseSchema


class SectorBase(BaseSchema):
    """Schéma de base pour les données de secteur"""

    name: str = Field(..., description="Nom du secteur")
    region_id: int = Field(..., description="ID de la région associée")


class SectorCreate(SectorBase):
    """Schéma pour la création d'un secteur"""

    pass


class SectorUpdate(BaseSchema):
    """Schéma pour la mise à jour d'un secteur"""

    name: Optional[str] = Field(None, description="Nom du secteur")
    region_id: Optional[int] = Field(None, description="ID de la région associée")


class SectorOut(SectorBase):
    """Schéma pour l'affichage d'un secteur"""

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
