from typing import List, Optional

from apps.tortoise.annual_headcount.models import (
    AnnualHeadcount as TortoiseAnnualHeadcount,
)
from apps.tortoise.city.models import City as TortoiseCity
from apps.tortoise.domain.models import Domain as TortoiseDomain
from apps.tortoise.establishment.models import Establishment as TortoiseEstablishment
from apps.tortoise.establishment_type.models import (
    EstablishmentType as TortoiseEstablishmentType,
)
from apps.tortoise.formation.models import Formation as TortoiseFormation
from apps.tortoise.formation_authorization.models import (
    FormationAuthorization as TortoiseFormationAuthorization,
)
from apps.tortoise.levels.models import Level as TortoiseLevel
from apps.tortoise.mentions.models import Mention as TortoiseMention
from apps.tortoise.rate.models import Rate as TortoiseRate
from apps.tortoise.region.models import Region as TortoiseRegion
from apps.tortoise.sector.models import Sector as TortoiseSector
from apps.tortoise.users.models import User as TortoiseUser
from core.entities.annual_headcount_entity import AnnualHeadCountEntity
from core.entities.city_entity import CityEntity
from core.entities.domain_entity import DomainEntity
from core.entities.establishment_entity import EstablishmentEntity
from core.entities.establishment_type_entity import EstablishmentTypeEntity
from core.entities.formation_authorization_entity import FormationAuthorizationEntity
from core.entities.formation_entity import FormationEntity
from core.entities.level_entity import LevelEntity
from core.entities.mention_entity import MentionEntity
from core.entities.rate_entity import RateEntity
from core.entities.region_entity import RegionEntity
from core.entities.sector_entity import SectorEntity
from core.entities.user_entity import UserEntity
from infrastructure.db.tortoise.metadata import (
    EstablishmentToEntityMetadata,
    FormationToEntityMetadata,
)


async def mention_to_entity(mention: TortoiseMention) -> MentionEntity:
    """
    Convertit un objet Mention (Tortoise ORM) en MentionEntity (Pydantic)
    """
    if not hasattr(mention, "domain") or mention.domain is None:
        raise ValueError(
            "Le champ domain (clé étrangère) est obligatoire pour MentionEntity mais est manquant sur l'objet Mention."
        )
    return MentionEntity(
        id=mention.id,
        name=mention.name,
        domain_id=mention.domain.id,
        created_at=mention.created_at,
        updated_at=mention.updated_at,
        created_by=mention.created_by.id if mention.created_by else None,
        updated_by=mention.updated_by.id if mention.updated_by else None,
    )


async def level_to_entity(level: TortoiseLevel) -> LevelEntity:
    """
    Convertit un objet Level (Tortoise ORM) en LevelEntity (Pydantic)
    """
    return LevelEntity(
        id=level.id,
        name=level.name,
        acronym=level.acronym,
        created_at=level.created_at,
        updated_at=level.updated_at,
        created_by=level.created_by.id if level.created_by else None,
        updated_by=level.updated_by.id if level.updated_by else None,
    )


async def formation_to_entity(
    formation: TortoiseFormation,
    metadata: Optional[FormationToEntityMetadata] = None,
) -> FormationEntity:
    """
    Convertit un objet Formation (Tortoise ORM) en FormationEntity (Pydantic)
    """
    level_entity = None
    mention_entity = None
    establishment_entity = None
    authorization_entity = None
    annual_headcount_list: List[AnnualHeadCountEntity] = []

    # Utiliser les valeurs par défaut de metadata si non fourni
    metadata = metadata if metadata is not None else FormationToEntityMetadata()

    if metadata.level and formation.level:
        level_entity = await level_to_entity(formation.level)
    if metadata.mention and formation.mention:
        mention_entity = await mention_to_entity(formation.mention)
    if metadata.establishment and formation.establishment:
        establishment_entity = EstablishmentEntity.model_validate(
            formation.establishment
        )
    if metadata.authorization and formation.authorization:
        authorization_entity = await formation_authorization_to_entity(
            formation.authorization
        )

    # Correction : requête asynchrone pour récupérer les AnnualHeadcount liés à la formation
    annual_headcount_models = await TortoiseAnnualHeadcount.filter(
        formation=formation
    ).all()
    for annual_headcount_model in annual_headcount_models:
        annual_headcount_list.append(
            await annual_headcount_to_entity(
                annual_headcount_model,
            ),
        )

    return FormationEntity(
        id=formation.id,
        name=formation.name,
        description=formation.description,
        duration=formation.duration,
        level_id=formation.level.id,
        mention_id=formation.mention.id,
        establishment_id=formation.establishment.id,
        authorization_id=(
            formation.authorization.id if formation.authorization else None
        ),
        level=level_entity,
        mention=mention_entity,
        establishment=establishment_entity,
        authorization=authorization_entity,
        annual_headcounts=annual_headcount_list,
        created_at=formation.created_at,
        updated_at=formation.updated_at,
        created_by=formation.created_by.id if formation.created_by else None,
        updated_by=formation.updated_by.id if formation.updated_by else None,
    )


async def user_to_entity(user: TortoiseUser) -> UserEntity:
    """
    Convertit un objet User (Tortoise ORM) en UserEntity (Pydantic)
    """
    return UserEntity(
        id=user.id,
        email=user.email,
        password=user.password,
        active=user.active,
        updated_by=user.updated_by.id if user.updated_by else None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


async def formation_authorization_to_entity(
    formation_authorization: TortoiseFormationAuthorization,
) -> FormationAuthorizationEntity:
    """
    Convertit un objet FormationAuthorization (Tortoise ORM) en FormationAuthorizationEntity (Pydantic)
    """
    return FormationAuthorizationEntity(
        id=formation_authorization.id,
        issued_date=formation_authorization.issued_date,
        expiry_date=formation_authorization.expiry_date,
        status=formation_authorization.status,
        decree=formation_authorization.decree,
        created_at=formation_authorization.created_at,
        updated_at=formation_authorization.updated_at,
        created_by=(
            formation_authorization.created_by.id
            if formation_authorization.created_by
            else None
        ),
        updated_by=(
            formation_authorization.updated_by.id
            if formation_authorization.updated_by
            else None
        ),
    )


async def establishment_type_to_entity(
    est_type: TortoiseEstablishmentType,
) -> EstablishmentTypeEntity:
    """
    Convertit un objet EstablishmentType (Tortoise ORM) en EstablishmentTypeEntity (Pydantic)
    """
    return EstablishmentTypeEntity(
        id=est_type.id,
        name=est_type.name,
        description=est_type.description,
        created_at=est_type.created_at,
        updated_at=est_type.updated_at,
        created_by=est_type.created_by.id if est_type.created_by else None,
        updated_by=est_type.updated_by.id if est_type.updated_by else None,
    )


async def establishment_to_entity(
    establishment: TortoiseEstablishment,
    metadata: Optional[EstablishmentToEntityMetadata] = None,
) -> EstablishmentEntity:
    """
    Convertit un objet Establishment (Tortoise ORM) en EstablishmentEntity (Pydantic)
    """
    establishment_type_entity = None
    sector_entity = None
    formations_list = []
    metadata = metadata if metadata is not None else EstablishmentToEntityMetadata()

    if metadata.establishment_type and establishment.establishment_type:
        establishment_type_entity = await establishment_type_to_entity(
            establishment.establishment_type
        )

    if metadata.sector and establishment.sector:  # Ajout de la conversion du secteur
        sector_entity = await sector_to_entity(establishment.sector)

    if metadata.formations:
        filtered_formations = await TortoiseFormation.filter(
            establishment=establishment
        ).all()
        for formation_model in filtered_formations:
            formations_list.append(
                formation_to_entity(
                    formation_model,
                    FormationToEntityMetadata(
                        level=True,
                        mention=True,
                        establishment=False,
                        authorization=True,
                    ),
                )
            )

    # Calcul de la moyenne des ratings pour l'établissement (Tortoise ORM async)
    rates = await TortoiseRate.filter(establishment_id=establishment.pk).all()
    avg_rating = 0  # Valeur par défaut si aucune évaluation
    if rates:
        total_ratings = len(rates)
        sum_ratings = sum(rate.rating for rate in rates)
        if total_ratings > 0:
            avg_rating = round(sum_ratings / total_ratings, 2)

    return EstablishmentEntity(
        id=establishment.id,
        name=establishment.name,
        acronym=establishment.acronym,
        address=establishment.address,
        contacts=establishment.contacts,
        website=establishment.website,
        description=establishment.description,
        latitude=establishment.latitude,
        longitude=establishment.longitude,
        rating=avg_rating,
        establishment_type_id=establishment.establishment_type.id,
        establishment_type=establishment_type_entity,
        sector_id=establishment.sector.id,
        sector=sector_entity,
        formations=formations_list,
        created_at=establishment.created_at,
        updated_at=establishment.updated_at,
        created_by=establishment.created_by.id if establishment.created_by else None,
        updated_by=establishment.updated_by.id if establishment.updated_by else None,
    )


async def domain_to_entity(domain: TortoiseDomain) -> DomainEntity:
    """
    Convertit un objet Domain (Tortoise ORM) en DomainEntity (Pydantic)
    """
    return DomainEntity(
        id=domain.id,
        name=domain.name,
        created_at=domain.created_at,
        updated_at=domain.updated_at,
        created_by=domain.created_by.id if domain.created_by else None,
        updated_by=domain.updated_by.id if domain.updated_by else None,
    )


async def city_to_entity(city: TortoiseCity) -> CityEntity:
    """
    Convertit un objet City (Tortoise ORM) en CityEntity (Pydantic)
    """
    return CityEntity(
        id=city.id,
        name=city.name,
        region_id=city.region.id,
        created_at=city.created_at,
        updated_at=city.updated_at,
        created_by=city.created_by.id if city.created_by else None,
        updated_by=city.updated_by.id if city.updated_by else None,
    )


async def annual_headcount_to_entity(
    headcount: TortoiseAnnualHeadcount,
) -> AnnualHeadCountEntity:
    """
    Convertit un objet AnnualHeadcount (Tortoise ORM) en AnnualHeadCountEntity (Pydantic)
    """
    if not hasattr(headcount, "formation") or headcount.formation is None:
        raise ValueError(
            "Le champ formation (clé étrangère) est obligatoire pour AnnualHeadCountEntity mais est manquant sur l'objet AnnualHeadcount."
        )
    return AnnualHeadCountEntity(
        id=headcount.id,
        formation_id=headcount.formation.id,
        academic_year=headcount.academic_year,
        students=headcount.students,
        success_rate=headcount.success_rate,
        created_at=headcount.created_at,
        updated_at=headcount.updated_at,
        created_by=headcount.created_by.id if headcount.created_by else None,
        updated_by=headcount.updated_by.id if headcount.updated_by else None,
    )


async def rate_to_entity(rate: TortoiseRate) -> RateEntity:
    """
    Convertit un objet Rate (Tortoise ORM) en RateEntity (Pydantic)
    """
    if not hasattr(rate, "establishment") or rate.establishment is None:
        raise ValueError(
            "Le champ establishment (clé étrangère) est obligatoire pour RateEntity mais est manquant sur l'objet Rate."
        )
    if not hasattr(rate, "user") or rate.user is None:
        raise ValueError(
            "Le champ user (clé étrangère) est obligatoire pour RateEntity mais est manquant sur l'objet Rate."
        )
    return RateEntity(
        id=rate.id,
        establishment_id=rate.establishment.id,
        user_id=rate.user.id,
        rating=rate.rating,
        created_at=rate.created_at,
        updated_at=rate.updated_at,
    )


async def region_to_entity(region: TortoiseRegion) -> RegionEntity:
    """
    Convertit un objet Region (Tortoise ORM) en RegionEntity (Pydantic)
    """
    return RegionEntity(
        id=region.id,
        name=region.name,
        code=region.code,
        created_at=region.created_at,
        updated_at=region.updated_at,
        created_by=region.created_by.id if region.created_by else None,
        updated_by=region.updated_by.id if region.updated_by else None,
    )


async def sector_to_entity(sector: TortoiseSector) -> SectorEntity:
    """
    Convertit un objet Sector (Tortoise ORM) en SectorEntity (Pydantic)
    """
    if not hasattr(sector, "city") or sector.city is None:
        raise ValueError(
            "Le champ city (clé étrangère) est obligatoire pour SectorEntity mais est manquant sur l'objet Sector."
        )
    return SectorEntity(
        id=sector.id,
        name=sector.name,
        city_id=sector.city.id,
        created_at=sector.created_at,
        updated_at=sector.updated_at,
        created_by=sector.created_by.id if sector.created_by else None,
        updated_by=sector.updated_by.id if sector.updated_by else None,
    )
