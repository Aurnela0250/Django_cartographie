from datetime import date, datetime
from typing import Literal, Optional

from ninja import Schema
from pydantic import Field, model_validator

from presentation.schemas.base_schema import BaseSchema

# MODIFIED: Define status choices directly as a Literal type
STATUS_CHOICES_LITERAL = Literal["REQUESTED", "VALIDATED", "REFUSED", "EXPIRED"]


class FormationAuthorizationBaseSchema(Schema):
    date_debut: date = Field(...)
    date_fin: Optional[date] = Field(None)
    status: STATUS_CHOICES_LITERAL = Field(...)  # MODIFIED: Use Literal for status
    arrete: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def check_dates(cls, values):
        # Ensure values is not None and contains the necessary fields
        if values is None:
            return values
        date_debut = getattr(values, "date_debut", None)
        date_fin = getattr(values, "date_fin", None)

        # Si date_debut et date_fin sont renseignés, vérifier l'ordre
        if date_debut is not None and date_fin is not None:
            if date_debut >= date_fin:
                raise ValueError("date_debut must be before date_fin")
        # Si uniquement date_fin est renseignée, vérifier la validité de l'année
        elif date_debut is None and date_fin is not None:
            if date_fin.year < 1900 or date_fin.year > 2100:
                raise ValueError(
                    "date_fin doit être une année valide (entre 1900 et 2100)"
                )
        return values


class CreateFormationAuthorizationSchema(FormationAuthorizationBaseSchema):
    pass


class UpdateFormationAuthorizationSchema(Schema):
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    status: Optional[STATUS_CHOICES_LITERAL] = Field(None)
    arrete: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def check_dates(cls, values):
        # Ensure values is not None and contains the necessary fields
        if values is None:
            return values
        date_debut = getattr(values, "date_debut", None)
        date_fin = getattr(values, "date_fin", None)

        # Si date_debut et date_fin sont renseignés, vérifier l'ordre
        if date_debut is not None and date_fin is not None:
            if date_debut >= date_fin:
                raise ValueError("date_debut must be before date_fin")
        # Si uniquement date_fin est renseignée, vérifier la validité de l'année
        elif date_debut is None and date_fin is not None:
            if date_fin.year < 1900 or date_fin.year > 2100:
                raise ValueError(
                    "date_fin doit être une année valide (entre 1900 et 2100)"
                )
        return values


class FormationAuthorizationSchema(BaseSchema):
    id: int
    date_debut: date
    date_fin: Optional[date] = None
    status: str
    arrete: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
