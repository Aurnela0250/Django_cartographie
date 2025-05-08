from typing import Optional

from pydantic import BaseModel

from apps.establishment.models import Establishment, EstablishmentType
from apps.formation.models import Formation
from apps.formation_authorization.models import FormationAuthorization
from apps.levels.models import Level
from apps.mentions.models import Mention
from apps.sector.models import Sector
from core.domain.entities.establishment_entity import EstablishmentEntity
from core.domain.entities.formation_authorization_entity import (
    FormationAuthorizationEntity,
)
from core.domain.entities.formation_entity import FormationEntity
from core.domain.entities.level_entity import LevelEntity
from core.domain.entities.mention_entity import MentionEntity
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
        created_at=formation.created_at,
        updated_at=formation.updated_at,
        created_by=formation.created_by.id if formation.created_by else None,
        updated_by=formation.updated_by.id if formation.updated_by else None,
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
        # Charger les formations associées à cet établissement
        # On utilise Formation.objects.filter pour être plus explicite
        for formation_model in Formation.objects.filter(establishment=establishment):
            # Pour l'instant, on ne charge pas les détails des formations (level, mention, etc.)
            # pour éviter les dépendances circulaires ou une charge de données trop importante.
            # Ceci peut être contrôlé via FormationToEntityMetadata si nécessaire.
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
