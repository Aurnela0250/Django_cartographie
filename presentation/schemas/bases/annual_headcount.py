import datetime as dt
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AnnualHeadcountBaseSchema(BaseModel):
    """Base schema for annual headcount"""

    id: int
    formation_id: int
    academic_year: int = Field(
        ...,
        description="Année universitaire (ex: 2023 pour 2023-2024)",
    )
    students: int = Field(
        ...,
        ge=0,
        description="Nombre d'étudiants inscrits",
    )
    success_rate: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Taux de réussite en pourcentage (ex: 85.5 pour 85,5%)",
    )
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    @field_validator("academic_year")
    @classmethod
    def validate_year(cls, v):
        # Vérifier que c'est une année valide (4 chiffres)
        if not 1000 <= v <= 9999:
            raise ValueError("L'année universitaire doit être un nombre à 4 chiffres")

        # Vérifier que l'année n'est pas trop dans le futur
        current_year = dt.datetime.now().year
        if v > current_year + 5:
            raise ValueError(
                f"L'année universitaire ne peut pas dépasser {current_year + 5}"
            )

        return v
