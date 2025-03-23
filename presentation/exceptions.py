from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from django.http import HttpResponse
from ninja.errors import HttpError
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

ModelType = TypeVar("ModelType", bound=BaseModel)


class SkyPulseApiError(Exception):
    """Base exception class for SkyPulse API"""

    def __init__(self, message: str = "Service is unavailable", name: str = "SkyPulse"):
        self.message = message
        self.name = name
        super().__init__(self.message)


class HTTPError(HttpError):
    """Base HTTP exception with customizable status code and detail"""

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code, detail)
        self.status_code = status_code
        self._detail = detail  # Stockez le détail dans un attribut privé
        self.headers = headers

    @property
    def detail(self):
        return self._detail

    def render(self, request) -> HttpResponse:
        response = HttpResponse(
            self.detail,
            status=self.status_code,
            content_type="application/json",
        )
        if self.headers:
            for name, value in self.headers.items():
                response[name] = value
        return response


class BadRequestError(HTTPError):
    """400 Bad Request"""

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=400, detail=detail, headers=headers)


class UnauthorizedError(HTTPError):
    """401 Unauthorized"""

    def __init__(
        self, detail: Any = "Unauthorized", headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=401, detail=detail, headers=headers)


class ForbiddenError(HTTPError):
    """403 Forbidden"""

    def __init__(
        self, detail: Any = "Forbidden", headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=403, detail=detail, headers=headers)


class NotFoundError(HTTPError):
    """404 Not Found"""

    def __init__(
        self, detail: Any = "Not found", headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=404, detail=detail, headers=headers)


class ConflictError(HTTPError):
    """409 Conflict"""

    def __init__(
        self, detail: Any = "Conflict", headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=409, detail=detail, headers=headers)


class UnprocessableEntityError(HTTPError):
    """422 Unprocessable Entity"""

    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=422, detail=detail, headers=headers)


class InternalServerError(HTTPError):
    """500 Internal Server Error"""

    def __init__(
        self,
        detail: Any = "Internal server error",
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=500, detail=detail, headers=headers)


class EntityError(Generic[ModelType]):
    """Base class for entity-related errors"""

    @classmethod
    def not_found(
        cls, model: Type[ModelType], identifier: Union[str, int, UUID, None] = None
    ) -> NotFoundError:
        detail = "Resource not found"
        return NotFoundError(detail=detail)

    @classmethod
    def already_exists(
        cls, model: Type[ModelType], identifier: Union[str, int, UUID, None] = None
    ) -> ConflictError:
        detail = "This resource already exists"
        return ConflictError(detail=detail)


# Specific exceptions
class ValidationError(UnprocessableEntityError):
    """Validation error"""

    def __init__(self, errors):
        self.error_details = errors
        super().__init__(detail={"message": "Erreur de validation", "errors": errors})

    def errors(self):
        return self.error_details

    @classmethod
    def formatted(cls, errors):
        formatted_errors = format_validation_errors(errors)
        return cls(formatted_errors)


class InvalidCredentialsError(UnauthorizedError):
    """Invalid credentials"""


class AuthenticationError(UnauthorizedError):
    """Authentication failed"""


class AuthorizationError(ForbiddenError):
    """Authorization failed"""


class InvalidTokenError(UnauthorizedError):
    """Invalid or expired token"""


class ServiceUnavailableError(InternalServerError):
    """Service unavailable"""


class DatabaseError(InternalServerError):
    """Database error"""


class ExternalServiceError(InternalServerError):
    """External service error"""


def format_validation_errors(
    exc: Union[PydanticValidationError, Exception],
) -> dict[str, Any]:
    if isinstance(exc, PydanticValidationError):
        errors = {}
        for error in exc.errors():
            field = error["loc"][0] if error["loc"] else "general"
            message = error["msg"]
            errors[field] = errors.get(field, []) + [message]
        return {"message": "Erreur de validation", "errors": errors}
    return {"message": str("exc")}
