from enum import Enum
from http import HTTPStatus


class ErrorMessage(Enum):
    # 4xx Client Errors
    BAD_REQUEST = (
        "The request could not be understood or was missing required parameters.",
        HTTPStatus.BAD_REQUEST,
    )
    UNAUTHORIZED = (
        "You are not authorized to access this resource. Please log in.",
        HTTPStatus.UNAUTHORIZED,
    )
    FORBIDDEN = (
        "You do not have permission to access this resource.",
        HTTPStatus.FORBIDDEN,
    )
    NOT_FOUND = ("The requested resource could not be found.", HTTPStatus.NOT_FOUND)
    CONFLICT = (
        "A conflict occurred. The resource already exists.",
        HTTPStatus.CONFLICT,
    )
    UNPROCESSABLE_ENTITY = (
        "The request could not be processed due to validation errors.",
        HTTPStatus.UNPROCESSABLE_ENTITY,
    )

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = (
        "An unexpected error occurred on the server. Please try again later.",
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    SERVICE_UNAVAILABLE = (
        "The service is temporarily unavailable. Please try again later.",
        HTTPStatus.SERVICE_UNAVAILABLE,
    )

    # Custom Errors
    VALIDATION_ERROR = (
        "Validation failed. Please check the provided data and try again.",
        HTTPStatus.UNPROCESSABLE_ENTITY,
    )
    INVALID_CREDENTIALS = (
        "The provided credentials are invalid. Please try again.",
        HTTPStatus.UNAUTHORIZED,
    )
    AUTHENTICATION_ERROR = (
        "Authentication failed. Please verify your credentials.",
        HTTPStatus.UNAUTHORIZED,
    )
    INVALID_TOKEN = (
        "The token is invalid or has expired or revoked. Please log in again.",
        HTTPStatus.UNAUTHORIZED,
    )
    DATABASE_ERROR = (
        "A database error occurred. Please contact support if the issue persists.",
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    EXTERNAL_SERVICE_ERROR = (
        "An error occurred while communicating with an external service. Please try again later.",
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    @property
    def message(self):
        return self.value[0]

    @property
    def status_code(self):
        return self.value[1].value

    def __str__(self) -> str:
        return self.message
