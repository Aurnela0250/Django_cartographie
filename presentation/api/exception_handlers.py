import traceback
from typing import Any, TypeVar, Union

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import JsonResponse
from ninja.errors import HttpError
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from presentation.exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    UnprocessableEntityError,
    ValidationError,
)

ModelType = TypeVar("ModelType", bound=BaseModel)


def format_validation_errors(
    exc: Union[PydanticValidationError, DjangoValidationError, Exception]
) -> dict[str, Any]:
    if isinstance(exc, PydanticValidationError):
        errors = {}
        for error in exc.errors():
            field = (
                ".".join(str(loc) for loc in error["loc"])
                if error["loc"]
                else "general"
            )
            message = error["msg"]
            errors[field] = errors.get(field, []) + [message]
        return {"message": "Erreur de validation", "errors": errors}
    elif isinstance(exc, DjangoValidationError):
        return {"message": "Erreur de validation", "errors": exc.message_dict}
    return {"message": str(exc)}


def global_exception_handler(request, exc):
    if settings.DEBUG:
        print(f"Exception caught: {type(exc).__name__} - {str(exc)}")
        print("Traceback:")
        traceback.print_exc()

    if isinstance(exc, HttpError):
        return JsonResponse({"detail": str(exc)}, status=exc.status_code)
    elif isinstance(exc, ValidationError):
        return JsonResponse(exc.detail, status=422)
    elif isinstance(exc, PydanticValidationError):
        formatted_errors = format_validation_errors(exc)
        return JsonResponse(formatted_errors, status=422)
    elif isinstance(exc, DjangoValidationError):
        formatted_errors = format_validation_errors(exc)
        return JsonResponse(formatted_errors, status=400)
    elif isinstance(exc, BadRequestError):
        return JsonResponse({"detail": exc.detail}, status=400)
    elif isinstance(exc, UnauthorizedError):
        return JsonResponse({"detail": exc.detail}, status=401)
    elif isinstance(exc, ForbiddenError):
        return JsonResponse({"detail": exc.detail}, status=403)
    elif isinstance(exc, NotFoundError):
        return JsonResponse({"detail": exc.detail}, status=404)
    elif isinstance(exc, ConflictError):
        return JsonResponse({"detail": exc.detail}, status=409)
    elif isinstance(exc, UnprocessableEntityError):
        return JsonResponse({"detail": exc.detail}, status=422)
    elif isinstance(exc, InternalServerError):
        return JsonResponse({"detail": exc.detail}, status=500)
    else:
        # Pour toutes les autres exceptions non gérées
        return JsonResponse(
            {"detail": "Une erreur inattendue s'est produite"}, status=500
        )
