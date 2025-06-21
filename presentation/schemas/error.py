from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import Field

from presentation.schemas.bases.base import BaseSchema


class ErrorCategory(str, Enum):
    CLIENT = "client_error"
    SERVER = "server_error"
    BUSINESS = "business_error"
    EXTERNAL = "external_error"


class ErrorDetailSchema(BaseSchema):
    field: Optional[str] = Field(None, description="Champ spécifique lié à l'erreur.")
    message: str = Field(
        ..., description="Description lisible de l'erreur sur le champ."
    )
    code: Optional[str] = Field(None, description="Code d'erreur machine-lisible.")
    value: Optional[Any] = Field(
        None, description="Valeur qui a causé l'erreur (peut être masquée)."
    )


class ErrorResponseSchema(BaseSchema):
    message: str = Field(..., description="Message d'erreur général.")
    code: str = Field(..., description="Code d'erreur personnalisé.")
    category: ErrorCategory = Field(..., description="Catégorie de l'erreur.")
    request_id: Optional[str] = Field(
        None,
        description="ID unique de la requête pour le traçage.",
    )
    timestamp: datetime = Field(..., description="Horodatage de l'erreur.")
    details: Optional[List[ErrorDetailSchema]] = Field(
        None, description="Liste détaillée des erreurs."
    )
    stack_trace: Optional[str] = Field(
        None,
        description="Trace de la pile (uniquement en développement).",
    )
