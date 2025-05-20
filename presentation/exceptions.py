from typing import Any, Dict, List, Optional, TypeVar, Union

from ninja_extra.exceptions import APIException, AuthenticationFailed
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from presentation.constants.errors_message_constant import ErrorMessage
from presentation.schemas.error_schema import ErrorDetailSchema, ErrorResponseSchema

ModelType = TypeVar("ModelType", bound=BaseModel)


class HTTPError(APIException):
    """Base HTTP exception with fixed status code and detail message"""

    def __init__(
        self,
        error_message: ErrorMessage,
        headers: Optional[Dict[str, Any]] = None,
    ):
        error_message = error_message
        self.headers = headers
        super().__init__()
        self.status_code = error_message.status_code
        self.detail = self._build_error_detail(error_message)

    def _build_error_detail(self, error_message: ErrorMessage) -> Dict[str, Any]:
        """Construct standardized error detail structure"""
        error_response = ErrorResponseSchema(message=error_message.message)

        return error_response.model_dump(exclude_none=True)


# 4xx Client Errors
class BadRequestError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.BAD_REQUEST, headers)


class UnauthorizedError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.UNAUTHORIZED, headers)


class ForbiddenError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.FORBIDDEN, headers)


class NotFoundError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.NOT_FOUND, headers)


class ConflictError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.CONFLICT, headers)


class UnprocessableEntityError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.UNPROCESSABLE_ENTITY, headers)


# 5xx Server Errors
class InternalServerError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.INTERNAL_SERVER_ERROR, headers)


class ServiceUnavailableError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.SERVICE_UNAVAILABLE, headers)


# Custom Errors
class ValidationError(HTTPError):
    def __init__(
        self,
        error: Union[Dict[str, Any], PydanticValidationError, None] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(ErrorMessage.VALIDATION_ERROR, headers)
        self.detail = self._build_error_detail(error)

    def _build_error_detail(
        self, error: Union[Dict[str, Any], PydanticValidationError, None]
    ) -> Dict[str, Any]:
        """Construct standardized error detail structure"""
        error_response = ErrorResponseSchema(
            message=ErrorMessage.VALIDATION_ERROR.message
        )

        if isinstance(error, PydanticValidationError):
            error_response.details = self._format_pydantic_errors(error.errors())

        return error_response.model_dump(exclude_none=True)

    def _format_pydantic_errors(self, errors: List[Any]) -> List[ErrorDetailSchema]:
        """Standardize Pydantic error format for API responses"""
        return [
            ErrorDetailSchema(
                field=".".join(str(loc) for loc in error.get("loc", [])),
                message=error.get("msg", "Invalid value"),
                code=error.get("type", "validation_error"),
            )
            for error in errors
        ]


class InvalidCredentialsError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.INVALID_CREDENTIALS, headers)


class AuthenticationError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.AUTHENTICATION_ERROR, headers)


class InvalidTokenError(AuthenticationFailed):
    status_code = ErrorMessage.INVALID_TOKEN.status_code
    default_detail = ErrorMessage.INVALID_TOKEN.message

    def __init__(self, detail=None, headers=None):
        """
        Initialise l'exception InvalidTokenError avec un message personnalisé optionnel.

        Args:
            detail: Message d'erreur personnalisé (si None, utilise le message par défaut)
            headers: En-têtes HTTP optionnels à inclure dans la réponse
        """
        if detail is None:
            detail = self.default_detail

        super().__init__(detail=detail)


class DatabaseError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.DATABASE_ERROR, headers)


class ExternalServiceError(HTTPError):
    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorMessage.EXTERNAL_SERVICE_ERROR, headers)
