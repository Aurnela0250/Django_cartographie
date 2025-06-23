import logging
import traceback
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse  # Retrait de Depends

from config import settings
from config.settings import TORTOISE_ORM

# Importer les fonctions d'initialisation de Tortoise ORM et la configuration
from config.tortoise_init import close_tortoise, init_tortoise
from core.container.container import Container
from presentation.api.v1.router import v1_router
from presentation.constants import errors_code
from presentation.exceptions import (
    APIException,
    InternalServerErrorException,
    UnprocessableEntityException,
)
from presentation.schemas.error import (
    ErrorCategory,
    ErrorDetailSchema,
    ErrorResponseSchema,
)


class ErrorConfig:
    """Configuration centralisée pour la gestion d'erreurs."""

    INCLUDE_STACK_TRACE_IN_RESPONSE = settings.INCLUDE_STACK_TRACE_IN_RESPONSE
    LOG_CRITICAL_STACK_TRACE = settings.LOG_CRITICAL_STACK_TRACE


# Configuration du logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code exécuté au démarrage
    print("🚀 FastAPI starting - Initializing Tortoise ORM...")
    await init_tortoise(TORTOISE_ORM)  # Initialiser Tortoise ORM
    print("🐢 Tortoise ORM Initialized.")
    print("📋 Use Aerich for schema migrations for Tortoise ORM:")
    print("   - Check status: aerich status")
    print("   - Create migration: aerich migrate --name <migration_name>")
    print("   - Apply migrations: aerich upgrade")
    yield
    # Code exécuté à l'arrêt
    print("🐢 Closing Tortoise ORM connections...")
    await close_tortoise()  # Fermer les connexions Tortoise ORM
    print("⏹️  FastAPI shutting down")


app = FastAPI(
    title="Django Cartographie API",
    description="API FastAPI with SQLModel and Alembic migrations",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)

container = Container()

# =============================================
# GESTIONNAIRES D'EXCEPTIONS
# =============================================


@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """Middleware qui génère un ID de requête et attrape les exceptions pour les enrichir."""
    request_id = str(uuid.uuid4())
    try:
        response = await call_next(request)
    except Exception as exc:
        if isinstance(exc, APIException):
            exc.request_id = request_id
        elif not hasattr(exc, "request_id"):
            setattr(exc, "request_id", request_id)
        raise exc
    return response


@app.exception_handler(APIException)
async def handle_api_exception(request: Request, exc: APIException):
    """Gestionnaire principal pour toutes les erreurs APIException et ses dérivées."""
    try:
        log_level = logging.ERROR if exc.status_code >= 500 else logging.WARNING

        # Log de base avec les informations de l'exception
        logger.log(
            log_level,
            f"API Exception - Request ID: {exc.request_id} | "
            f"Status: {exc.status_code} | "
            f"Category: {exc.category.value} | "
            f"Code: {exc.code} | "
            f"Message: {exc.message}",
            extra={
                "request_id": exc.request_id,
                "status_code": exc.status_code,
                "category": exc.category.value,
                "code": exc.code,
                "details": [d.model_dump() for d in exc.details] if exc.details else [],
            },
        )

        # Log détaillé de la cause si elle existe
        if exc.__cause__:
            logger.error(
                f"Exception Cause - Request ID: {exc.request_id} | "
                f"Cause Type: {type(exc.__cause__).__name__} | "
                f"Cause Message: {str(exc.__cause__)}"
            )

            # Log de la stack trace de la cause pour les erreurs critiques
            if exc.status_code >= 500:
                cause_traceback = "".join(
                    traceback.format_exception(
                        type(exc.__cause__),
                        exc.__cause__,
                        exc.__cause__.__traceback__,
                    )
                )
                logger.error(
                    f"Cause Stack Trace - Request ID: {exc.request_id}:\n{cause_traceback}"
                )

        # Log des détails si disponibles
        if exc.details:
            details_str = " | ".join(
                [
                    f"Field: {detail.field}, Message: {detail.message}, Code: {detail.code}"
                    for detail in exc.details
                ]
            )
            logger.error(
                f"Exception Details - Request ID: {exc.request_id} | {details_str}"
            )

        if exc.status_code >= 500 and ErrorConfig.LOG_CRITICAL_STACK_TRACE:
            logger.error(
                f"Unhandled critical error occurred (RequestID: {exc.request_id}):",
                exc_info=exc.__cause__ or exc,
            )

        error_content = ErrorResponseSchema(
            message=exc.message,
            code=exc.code,
            category=exc.category,
            request_id=exc.request_id,
            timestamp=datetime.now(),
            details=exc.details or None,
            stack_trace=(
                get_stack_trace(exc)
                if ErrorConfig.INCLUDE_STACK_TRACE_IN_RESPONSE
                else None
            ),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_content.model_dump(mode="json", exclude_none=True),
        )
    except Exception as handler_error:
        logger.critical(
            f"Critical error in exception handler: {str(handler_error)} | "
            f"Original exception: {str(exc)}"
        )
        # Log de la stack trace du handler si configuré
        if ErrorConfig.LOG_CRITICAL_STACK_TRACE:
            handler_traceback = traceback.format_exc()
            logger.critical(f"Handler Stack Trace:\n{handler_traceback}")

        # Retourner une réponse d'erreur générique en cas d'échec du gestionnaire
        return JSONResponse(
            status_code=500,
            content={
                "message": "Erreur critique du serveur",
                "code": ErrorCategory.SERVER,
                "category": errors_code.INTERNAL_SERVER,
                "request_id": getattr(exc, "request_id", "unknown"),
                "timestamp": datetime.now().isoformat(),
            },
        )


def get_stack_trace(exc: Exception) -> Optional[str]:
    """
    Génère une stack trace lisible pour l'exception
    """
    try:
        if exc.__traceback__:
            return "".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)
            )
        return None
    except Exception:
        return "Stack trace unavailable"


@app.exception_handler(RequestValidationError)
async def handle_pydantic_validation_error(
    request: Request, exc: RequestValidationError
):
    """Gestionnaire pour les erreurs de validation de Pydantic."""
    details = [
        ErrorDetailSchema(
            field=" -> ".join(map(str, err["loc"])),
            message=err["msg"],
            code=err["type"],
            value=None,
        )
        for err in exc.errors()
    ]

    api_exc = UnprocessableEntityException(details=details)
    api_exc.request_id = getattr(exc, "request_id", str(uuid.uuid4()))
    return await handle_api_exception(request, api_exc)


@app.exception_handler(Exception)
async def handle_generic_exception(request: Request, exc: Exception):
    """Gestionnaire global pour toutes les exceptions non prévues."""
    if isinstance(exc, APIException) or isinstance(exc, RequestValidationError):
        raise exc  # Ne pas retraiter

    request_id = getattr(exc, "request_id", str(uuid.uuid4()))

    api_exc = InternalServerErrorException(
        message="Une erreur inattendue est survenue. L'équipe technique a été notifiée.",
        cause=exc,
    )
    api_exc.request_id = request_id
    return await handle_api_exception(request, api_exc)


@app.get("/")
async def read_root():
    return {
        "message": "Django Cartographie API",
        "status": "running",
        "migrations": "Use 'make help' to see all available Alembic commands",
    }


app.include_router(v1_router)
