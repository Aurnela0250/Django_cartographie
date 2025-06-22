from dependency_injector import containers, providers

from core.interfaces.auth_repository import IAuthRepository
from core.interfaces.city_repository import ICityRepository
from core.interfaces.domain_repository import IDomainRepository
from core.interfaces.establishment_repository import IEstablishmentRepository
from core.interfaces.establishment_type_repository import IEstablishmentTypeRepository
from core.interfaces.formation_repository import IFormationRepository
from core.interfaces.level_repository import ILevelRepository
from core.interfaces.mention_repository import IMentionRepository
from core.interfaces.rate_repository import IRateRepository
from core.interfaces.region_repository import IRegionRepository
from core.interfaces.user_repository import IUserRepository
from core.use_cases.auth_use_case import AuthUseCase
from core.use_cases.city_use_case import CityUseCase
from core.use_cases.domain_use_case import DomainUseCase
from core.use_cases.establishment_type_use_case import EstablishmentTypeUseCase
from core.use_cases.establishment_use_case import EstablishmentUseCase
from core.use_cases.formation_use_case import FormationUseCase
from core.use_cases.level_use_case import LevelUseCase
from core.use_cases.mention_use_case import MentionUseCase
from core.use_cases.region_use_case import RegionUseCase
from infrastructure.db.tortoise.auth_repository_impl import AuthRepository
from infrastructure.db.tortoise.city_repository_impl import CityRepository
from infrastructure.db.tortoise.domain_repository_impl import DomainRepository
from infrastructure.db.tortoise.establishment_repository_impl import (
    EstablishmentRepository,
)
from infrastructure.db.tortoise.establishment_type_repository_impl import (
    EstablishmentTypeRepository,
)
from infrastructure.db.tortoise.formation_repository_impl import FormationRepository
from infrastructure.db.tortoise.level_repository_impl import LevelRepository
from infrastructure.db.tortoise.mention_repository_impl import MentionRepository
from infrastructure.db.tortoise.rate_repository_impl import RateRepository
from infrastructure.db.tortoise.region_repository_impl import RegionRepository
from infrastructure.db.tortoise.user_repository_impl import UserRepository
from infrastructure.external_services.bcrypt_service import BcryptService
from infrastructure.external_services.jwt_service import JWTService
from infrastructure.external_services.redis_service import RedisService


class Container(containers.DeclarativeContainer):
    """
    Container de dépendances pour l'injection des repositories et services
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            # Endpoints
            "presentation.api.v1.endpoints.auth_controller",
            "presentation.api.v1.endpoints.city_controller",
            "presentation.api.v1.endpoints.domain_controller",
            "presentation.api.v1.endpoints.establishment_controller",
            "presentation.api.v1.endpoints.establishment_type_controller",
            "presentation.api.v1.endpoints.formation_controller",
            "presentation.api.v1.endpoints.level_controller",
            "presentation.api.v1.endpoints.mention_controller",
            "presentation.api.v1.endpoints.region_controller",
            # Dépendances
            "presentation.dependencies.auth_dependencies",
        ]
    )

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
    city_repository: providers.Provider[ICityRepository] = providers.Singleton(
        CityRepository
    )
    establishment_repository: providers.Provider[IEstablishmentRepository] = (
        providers.Singleton(EstablishmentRepository)
    )
    establishment_type_repository: providers.Provider[IEstablishmentTypeRepository] = (
        providers.Singleton(EstablishmentTypeRepository)
    )
    formation_repository: providers.Provider[IFormationRepository] = (
        providers.Singleton(FormationRepository)
    )
    level_repository: providers.Provider[ILevelRepository] = providers.Singleton(
        LevelRepository
    )
    mention_repository: providers.Provider[IMentionRepository] = providers.Singleton(
        MentionRepository
    )
    rate_repository: providers.Provider[IRateRepository] = providers.Singleton(
        RateRepository
    )
    region_repository: providers.Provider[IRegionRepository] = providers.Singleton(
        RegionRepository
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

    city_use_case: providers.Provider[CityUseCase] = providers.Factory(
        CityUseCase,
        city_repository,
    )
    domain_use_case: providers.Provider[DomainUseCase] = providers.Factory(
        DomainUseCase,
        domain_repository,
    )
    establishment_type_use_case: providers.Provider[EstablishmentTypeUseCase] = (
        providers.Factory(
            EstablishmentTypeUseCase,
            establishment_type_repository,
        )
    )
    establishment_use_case: providers.Provider[EstablishmentUseCase] = (
        providers.Factory(
            EstablishmentUseCase,
            establishment_repository,
            rate_repository,
        )
    )
    formation_use_case: providers.Provider[FormationUseCase] = providers.Factory(
        FormationUseCase,
        formation_repository,
    )
    level_use_case: providers.Provider[LevelUseCase] = providers.Factory(
        LevelUseCase,
        level_repository,
    )
    mention_use_case: providers.Provider[MentionUseCase] = providers.Factory(
        MentionUseCase,
        mention_repository,
    )
    region_use_case: providers.Provider[RegionUseCase] = providers.Factory(
        RegionUseCase,
        region_repository,
    )
