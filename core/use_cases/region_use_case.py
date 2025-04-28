import logging
from typing import List, Optional

from core.domain.entities.region_entity import RegionEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_region_repository import DjangoRegionRepository
from presentation.exceptions import ConflictError, NotFoundError, EntityError


class RegionUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les régions"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_region(self, region_data: RegionEntity) -> RegionEntity:
        """Crée une nouvelle région"""
        with self.unit_of_work:
            region_repository = self.unit_of_work.get_repository(DjangoRegionRepository)

            # Vérifier si une région avec le même nom existe déjà
            existing_region = region_repository.get_by_name(region_data.name)
            if existing_region:
                self.logger.warning(
                    f"Region with name '{region_data.name}' already exists"
                )
                raise EntityError.already_exists(RegionEntity, region_data.name)

            # Vérifier si une région avec le même code existe déjà (si un code est fourni)
            if region_data.code:
                existing_region = region_repository.get_by_code(region_data.code)
                if existing_region:
                    self.logger.warning(
                        f"Region with code '{region_data.code}' already exists"
                    )
                    raise EntityError.already_exists(RegionEntity, region_data.code)

            # Créer la région
            created_region = region_repository.create(region_data)
            self.unit_of_work.commit()
            return created_region

    def get_region(self, region_id: int) -> RegionEntity:
        """Récupère une région par son ID"""
        with self.unit_of_work:
            region_repository = self.unit_of_work.get_repository(DjangoRegionRepository)
            region = region_repository.get(region_id)
            if not region:
                raise EntityError.not_found(RegionEntity, region_id)
            return region

    def update_region(self, region_id: int, region_data: RegionEntity) -> RegionEntity:
        """Met à jour une région existante"""
        with self.unit_of_work:
            region_repository = self.unit_of_work.get_repository(DjangoRegionRepository)

            # Vérifier si la région existe
            existing_region = region_repository.get(region_id)
            if not existing_region:
                raise EntityError.not_found(RegionEntity, region_id)

            # Vérifier si le nouveau nom existe déjà pour une autre région
            if region_data.name != existing_region.name:
                name_exists = region_repository.get_by_name(region_data.name)
                if name_exists and name_exists.id != region_id:
                    self.logger.warning(
                        f"Cannot update: Region with name '{region_data.name}' already exists"
                    )
                    raise EntityError.already_exists(RegionEntity, region_data.name)

            # Vérifier si le nouveau code existe déjà pour une autre région
            if region_data.code and region_data.code != existing_region.code:
                code_exists = region_repository.get_by_code(region_data.code)
                if code_exists and code_exists.id != region_id:
                    self.logger.warning(
                        f"Cannot update: Region with code '{region_data.code}' already exists"
                    )
                    raise EntityError.already_exists(RegionEntity, region_data.code)

            # Mettre à jour la région
            updated_region = region_repository.update(region_id, region_data)
            self.unit_of_work.commit()
            return updated_region

    def delete_region(self, region_id: int) -> bool:
        """Supprime une région"""
        with self.unit_of_work:
            region_repository = self.unit_of_work.get_repository(DjangoRegionRepository)

            # Vérifier si la région existe
            existing_region = region_repository.get(region_id)
            if not existing_region:
                raise EntityError.not_found(RegionEntity, region_id)

            # Supprimer la région
            result = region_repository.delete(region_id)
            self.unit_of_work.commit()
            return result

    def get_all_regions(self) -> List[RegionEntity]:
        """Récupère toutes les régions"""
        with self.unit_of_work:
            region_repository = self.unit_of_work.get_repository(DjangoRegionRepository)
            return region_repository.get_all()

    def filter_regions(self, **kwargs) -> List[RegionEntity]:
        """Filtre les régions selon les critères fournis"""
        with self.unit_of_work:
            region_repository = self.unit_of_work.get_repository(DjangoRegionRepository)
            return region_repository.filter(**kwargs)
