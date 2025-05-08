from typing import List, Optional

from pydantic import BaseModel

from apps.city.models import City
from apps.establishment.models import Establishment, EstablishmentType
from apps.formation.models import AnnualHeadcount, Formation
from apps.formation_authorization.models import FormationAuthorization
from apps.levels.models import Level
from apps.mentions.models import Mention
from apps.rate.models import Rate
from apps.sector.models import Sector
from core.domain.entities.city_entity import CityEntity
from core.domain.entities.establishment_entity import EstablishmentEntity
from core.domain.entities.formation_authorization_entity import (
    FormationAuthorizationEntity,
)
from core.domain.entities.formation_entity import AnnualHeadCountEntity, FormationEntity
from core.domain.entities.level_entity import LevelEntity
from core.domain.entities.mention_entity import MentionEntity
from core.domain.entities.rate_entity import RateEntity
from core.domain.entities.sector_entity import SectorEntity
from core.interfaces.establishment_type_repository import EstablishmentTypeEntity


def level_to_entity(level: Level) -> LevelEntity:
    """Convertit un objet Level Django en LevelEntity"""
    return LevelEntity(
        id=level.pk,
        name=level.name,
        acronyme=level.acronyme,
        created_at=level.created_at,
        updated_at=level.updated_at,
        created_by=level.created_by.id if level.created_by else None,
        updated_by=level.updated_by.id if level.updated_by else None,
    )


def mention_to_entity(mention: Mention) -> MentionEntity:
    """Convertit un objet Mention Django en MentionEntity"""
    return MentionEntity(
        id=mention.pk,
        name=mention.name,
        domain_id=mention.domain.pk,
        created_at=mention.created_at,
        updated_at=mention.updated_at,
        created_by=mention.created_by.id if mention.created_by else None,
        updated_by=mention.updated_by.id if mention.updated_by else None,
    )


class FormationToEntityMetadata(BaseModel):
    level: Optional[bool] = False
    mention: Optional[bool] = False
    establishment: Optional[bool] = False
    authorization: Optional[bool] = False


def formation_authorization_to_entity(
    authorization: FormationAuthorization,
) -> FormationAuthorizationEntity:
    return FormationAuthorizationEntity(
        id=authorization.pk,
        date_debut=authorization.date_debut,
        date_fin=authorization.date_fin,
        status=authorization.status,
        arrete=authorization.arrete,
        created_at=authorization.created_at,
        updated_at=authorization.updated_at,
        created_by=authorization.created_by.id if authorization.created_by else None,
        updated_by=authorization.updated_by.id if authorization.updated_by else None,
    )


def formation_to_entity(
    formation: Formation,
    metadata: Optional[FormationToEntityMetadata] = None,
) -> FormationEntity:
    level_entity = None
    mention_entity = None
    establishment_entity = None
    authorization_entity = None
    annual_headcount_list: List[AnnualHeadCountEntity] = []

    # Utiliser les valeurs par défaut de metadata si non fourni
    effective_metadata = (
        metadata if metadata is not None else FormationToEntityMetadata()
    )

    if effective_metadata.level and formation.level:
        level_entity = level_to_entity(formation.level)
    if effective_metadata.mention and formation.mention:
        mention_entity = mention_to_entity(formation.mention)
    if effective_metadata.establishment and formation.establishment:
        establishment_entity = EstablishmentEntity.model_validate(
            formation.establishment
        )
    if effective_metadata.authorization and formation.authorization:
        authorization_entity = formation_authorization_to_entity(
            formation.authorization
        )

    for annual_headcount_model in AnnualHeadcount.objects.filter(formation=formation):
        annual_headcount_list.append(
            annual_headcount_to_entity(
                annual_headcount_model,
            ),
        )

    return FormationEntity(
        id=formation.pk,
        intitule=formation.intitule,
        description=formation.description,
        duration=formation.duration,
        level_id=formation.level.pk,
        mention_id=formation.mention.pk,
        establishment_id=formation.establishment.pk,
        authorization_id=(
            formation.authorization.pk if formation.authorization else None
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


def annual_headcount_to_entity(
    headcount: AnnualHeadcount,
) -> AnnualHeadCountEntity:
    """Convertit un objet EffectifAnnuelFormation Django en EffectifAnnuelFormationEntity"""
    return AnnualHeadCountEntity(
        id=headcount.pk,
        formation_id=headcount.formation.pk,
        academic_year=headcount.academic_year,
        students=headcount.students,
        created_at=headcount.created_at,
        updated_at=headcount.updated_at,
        created_by=headcount.created_by.id if headcount.created_by else None,
        updated_by=headcount.updated_by.id if headcount.updated_by else None,
    )


def sector_to_entity(sector: Sector) -> SectorEntity:
    """Convertit un objet Sector Django en SectorEntity"""
    return SectorEntity(
        id=sector.pk,
        name=sector.name,
        region_id=sector.region.pk,
        created_at=sector.created_at,
        updated_at=sector.updated_at,
        created_by=sector.created_by.id if sector.created_by else None,
        updated_by=sector.updated_by.id if sector.updated_by else None,
    )


class EstablishmentToEntityMetadata(BaseModel):
    establishment_type: Optional[bool] = False
    sector: Optional[bool] = False
    formations: Optional[bool] = False


def establishment_to_entity(
    establishment: Establishment,
    metadata: Optional[EstablishmentToEntityMetadata] = None,
) -> EstablishmentEntity:

    effective_metadata = (
        metadata if metadata is not None else EstablishmentToEntityMetadata()
    )

    establishment_type_entity = None
    if effective_metadata.establishment_type and establishment.establishment_type:
        establishment_type_entity = establishment_type_to_entity(
            establishment.establishment_type
        )

    sector_entity = None
    if (
        effective_metadata.sector and establishment.sector
    ):  # Ajout de la conversion du secteur
        sector_entity = sector_to_entity(establishment.sector)

    formations_list = []
    if effective_metadata.formations:
        for formation_model in Formation.objects.filter(establishment=establishment):
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

    # Calcul de la moyenne des ratings pour l'établissement
    rates = Rate.objects.filter(establishment_id=establishment.pk)
    avg_rating = 0  # Valeur par défaut si aucune évaluation
    if rates.exists():
        total_ratings = rates.count()
        sum_ratings = sum(rate.rating for rate in rates)
        if total_ratings > 0:
            avg_rating = round(sum_ratings / total_ratings, 2)

    return EstablishmentEntity(
        id=establishment.pk,
        name=establishment.name,
        acronyme=establishment.acronyme,
        address=establishment.address,
        code_postal=establishment.code_postal,
        ville=establishment.ville,
        contacts=establishment.contacts,
        site_url=establishment.site_url,
        description=establishment.description,
        latitude=establishment.latitude,
        longitude=establishment.longitude,
        rating=avg_rating,
        establishment_type_id=establishment.establishment_type.pk,
        establishment_type=establishment_type_entity,
        sector_id=establishment.sector.pk,
        sector=sector_entity,
        formations=formations_list,
        created_at=establishment.created_at,
        updated_at=establishment.updated_at,
        created_by=establishment.created_by.id if establishment.created_by else None,
        updated_by=establishment.updated_by.id if establishment.updated_by else None,
    )


def establishment_type_to_entity(
    establishment_type: EstablishmentType,
) -> EstablishmentTypeEntity:
    return EstablishmentTypeEntity(
        id=establishment_type.pk,
        name=establishment_type.name,
        description=establishment_type.description,
        created_at=establishment_type.created_at,
        updated_at=establishment_type.updated_at,
        created_by=(
            establishment_type.created_by.id if establishment_type.created_by else None
        ),
        updated_by=(
            establishment_type.updated_by.id if establishment_type.updated_by else None
        ),
    )


def rate_to_entity(rate: Rate) -> RateEntity:
    """Convertit un objet Rate Django en RateEntity"""
    return RateEntity(
        id=rate.pk,
        establishment_id=rate.establishment.pk,
        user_id=rate.user.pk,
        rating=rate.rating,
        created_at=rate.created_at,
        updated_at=rate.updated_at,
    )


def city_to_entity(db_obj: City) -> CityEntity:
    """
    Convert Django City model to CityEntity
    """
    return CityEntity(
        id=db_obj.pk,
        name=db_obj.name,
        region_id=db_obj.region.pk,
        created_at=db_obj.created_at,
        updated_at=db_obj.updated_at,
        created_by=db_obj.created_by.id if db_obj.created_by else None,
        updated_by=db_obj.updated_by.id if db_obj.updated_by else None,
    )
