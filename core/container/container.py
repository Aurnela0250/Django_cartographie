from dependency_injector import containers, providers

from core.interfaces.auth_repository import IAuthRepository
from core.interfaces.domain_repository import IDomainRepository
from core.interfaces.user_repository import IUserRepository
from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.db.tortoise.auth_repository_impl import AuthRepository
from infrastructure.db.tortoise.domain_repository_impl import DomainRepository
from infrastructure.db.tortoise.user_repository_impl import UserRepository
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from infrastructure.external_services.redis_service import RedisService


class Container(containers.DeclarativeContainer):
    """
    Container de dépendances pour l'injection des repositories et services
    """

    config = providers.Configuration()

    # Repository singletons
    auth_repository: providers.Provider[IAuthRepository] = providers.Singleton(
        AuthRepository
    )
    user_repository: providers.Provider[IUserRepository] = providers.Singleton(
        UserRepository
    )
    domain_repository: providers.Provider[IDomainRepository] = providers.Singleton(
        DomainRepository
    )

    # Service singletons
    redis_service: providers.Provider[RedisService] = providers.Singleton(RedisService)
    jwt_service: providers.Provider[JWTService] = providers.Singleton(
        JWTService,
        redis_service=redis_service,
    )
    bcrypt_service: providers.Provider[BcryptService] = providers.Singleton(
        BcryptService
    )

    # Use Case singletons
    auth_use_case: providers.Provider[AuthUseCase] = providers.Factory(
        AuthUseCase,
        jwt_service,
        bcrypt_service,
        auth_repository,
    )
