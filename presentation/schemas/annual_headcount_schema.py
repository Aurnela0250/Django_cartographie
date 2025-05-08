import datetime as dt
from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import ConfigDict, Field, field_validator


class AnnualHeadcountBase(Schema):
    """Base schema for annual headcount"""

    academic_year: int = Field(
        ..., description="Année universitaire (ex: 2023 pour 2023-2024)"
    )
    students: int = Field(..., ge=0, description="Nombre d'étudiants inscrits")

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


class AnnualHeadcountCreate(AnnualHeadcountBase):
    """Schema for creating a new annual headcount"""

    pass


class AnnualHeadcountUpdate(Schema):
    """Schema for updating an annual headcount"""

    academic_year: Optional[int] = Field(
        None, description="Année universitaire (ex: 2023 pour 2023-2024)"
    )
    students: Optional[int] = Field(
        None, ge=0, description="Nombre d'étudiants inscrits"
    )

    @field_validator("academic_year")
    @classmethod
    def validate_year(cls, v):
        if v is None:
            return v

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


class AnnualHeadcountResponse(AnnualHeadcountBase):
    """Schema for annual headcount response"""

    id: int
    formation_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
