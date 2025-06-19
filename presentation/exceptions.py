import logging
from typing import List, Optional, Union

from fastapi import status

from config import settings
from presentation.constants import errors_code, errors_message
from presentation.schemas.error_schema import ErrorCategory, ErrorDetailSchema

# =============================================
# CONFIGURATION ET LOGGING
# =============================================


class ErrorConfig:
    """Configuration centralisée pour la gestion d'erreurs."""

    INCLUDE_STACK_TRACE_IN_RESPONSE = settings.INCLUDE_STACK_TRACE_IN_RESPONSE
    LOG_CRITICAL_STACK_TRACE = settings.LOG_CRITICAL_STACK_TRACE


# Configuration du logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# =============================================
# EXCEPTIONS PERSONNALISÉES (HIÉRARCHIE D'HÉRITAGE)
# =============================================


class APIException(Exception):
    """Exception de base pour toutes les erreurs de l'API."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    category: ErrorCategory = ErrorCategory.SERVER
    message: str = errors_message.INTERNAL_SERVER_ERROR
    code: str = errors_code.INTERNAL_SERVER

    def __init__(
        self,
        message: Optional[str] = None,
        category: Optional[ErrorCategory] = None,
        code: Optional[str] = None,
        details: Optional[Union[List[ErrorDetailSchema], ErrorDetailSchema]] = None,
        cause: Optional[Exception] = None,
    ):
        self.message = message or self.message
        self.category = category or self.category
        self.code = code or self.code

        if details is None:
            self.details = []
        elif isinstance(details, list):
            self.details = details
        else:
            self.details = [details]

        self.request_id: Optional[str] = None  # Assigné par le middleware
        self.__cause__ = cause
        super().__init__(self.message)


# --- Classes de base pour les catégories ---


class ClientException(APIException):
    """Exception de base pour les erreurs 4xx (côté client)."""

    category = ErrorCategory.CLIENT


class ServerException(APIException):
    """Exception de base pour les erreurs 5xx (côté serveur)."""

    category = ErrorCategory.SERVER


# --- Erreurs Client (4xx) ---


class BadRequestException(ClientException):
    status_code = status.HTTP_400_BAD_REQUEST
    message: str = errors_message.BAD_REQUEST
    code: str = errors_code.BAD_REQUEST


class UnprocessableEntityException(ClientException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message: str = errors_message.UNPROCESSABLE_ENTITY
    code: str = errors_code.UNPROCESSABLE_ENTITY


class UnauthorizedException(ClientException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message: str = errors_message.UNAUTHORIZED
    code: str = errors_code.UNAUTHORIZED


class ForbiddenException(ClientException):
    status_code = status.HTTP_403_FORBIDDEN
    message = errors_message.FORBIDDEN
    code = errors_code.FORBIDDEN


class NotFoundException(ClientException):
    status_code = status.HTTP_404_NOT_FOUND
    message = errors_message.NOT_FOUND
    code = errors_code.NOT_FOUND


class ConflictException(ClientException):
    status_code = status.HTTP_409_CONFLICT
    message = errors_message.CONFLICT
    code = errors_code.CONFLICT


# --- Erreurs Serveur (5xx) ---


class InternalServerErrorException(ServerException):
    pass


class ServiceUnavailableException(ServerException):
    message = errors_message.SERVICE_UNAVAILABLE
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = errors_code.SERVICE_UNAVAILABLE
