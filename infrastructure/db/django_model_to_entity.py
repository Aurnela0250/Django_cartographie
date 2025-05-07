from typing import Optional

from pydantic import BaseModel

from apps.establishment.models import Establishment, EstablishmentType
from apps.sector.models import Sector
from core.domain.entities.sector_entity import SectorEntity
from core.interfaces.establishment_repository import EstablishmentEntity
from core.interfaces.establishment_type_repository import EstablishmentTypeEntity


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


def establishment_to_entity(
    establishment: Establishment,
    metadata: Optional[
        EstablishmentToEntityMetadata
    ] = None,  # Ajout de la valeur par défaut
) -> EstablishmentEntity:
    # Utiliser les valeurs par défaut de metadata si non fourni
    effective_metadata = (
        metadata if metadata is not None else EstablishmentToEntityMetadata()
    )

    establishment_type_entity = None
    if effective_metadata.establishment_type and establishment.establishment_type:
        establishment_type_entity = establishment_type_to_entity(
            establishment.establishment_type
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
