from datetime import date
from typing import Literal, Optional

from pydantic import Field, model_validator

from presentation.schemas.bases.base import BaseSchema
from presentation.schemas.bases.formation_authorization import (
    FormationAuthorizationBaseSchema,
)

# MODIFIED: Define status choices directly as a Literal type
STATUS_CHOICES_LITERAL = Literal["REQUESTED", "VALIDATED", "REFUSED", "EXPIRED"]


class FormationAuthorizationSchema(FormationAuthorizationBaseSchema):
    pass


class CreateFormationAuthorizationSchema(BaseSchema):
    issued_date: date = Field(...)
    expiry_date: Optional[date] = Field(None)
    status: STATUS_CHOICES_LITERAL = Field(default="REQUESTED")
    decree: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def check_dates(cls, values):
        # Ensure values is not None and contains the necessary fields
        if values is None:
            return values
        issued_date = getattr(values, "issued_date", None)
        expiry_date = getattr(values, "expiry_date", None)

        # Si issued_date et expiry_date sont renseignés, vérifier l'ordre
        if issued_date is not None and expiry_date is not None:
            if issued_date >= expiry_date:
                raise ValueError("issued_date must be before expiry_date")
        # Si uniquement expiry_date est renseignée, vérifier la validité de l'année
        elif issued_date is None and expiry_date is not None:
            if expiry_date.year < 1900 or expiry_date.year > 2100:
                raise ValueError(
                    "expiry_date doit être une année valide (entre 1900 et 2100)"
                )
        return values


class UpdateFormationAuthorizationSchema(BaseSchema):
    issued_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: Optional[STATUS_CHOICES_LITERAL] = Field(None)
    decree: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def check_dates(cls, values):
        # Ensure values is not None and contains the necessary fields
        if values is None:
            return values
        issued_date = getattr(values, "issued_date", None)
        expiry_date = getattr(values, "expiry_date", None)

        # Si issued_date et expiry_date sont renseignés, vérifier l'ordre
        if issued_date is not None and expiry_date is not None:
            if issued_date >= expiry_date:
                raise ValueError("issued_date must be before expiry_date")
        # Si uniquement expiry_date est renseignée, vérifier la validité de l'année
        elif issued_date is None and expiry_date is not None:
            if expiry_date.year < 1900 or expiry_date.year > 2100:
                raise ValueError(
                    "expiry_date doit être une année valide (entre 1900 et 2100)"
                )
        return values
