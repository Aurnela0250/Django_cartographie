import logging
from typing import List

from core.domain.entities.pagination import PaginatedResult, PaginationParams
from core.domain.entities.sector_entity import SectorEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_sector_repository import DjangoSectorRepository
from presentation.exceptions import (
    ConflictError,
    NotFoundError,
)


class SectorUseCase:
    """Cas d'utilisation pour les opérations CRUD sur les secteurs"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_sector(self, sector_data: SectorEntity) -> SectorEntity:
        with self.unit_of_work:
            sector_repository = self.unit_of_work.get_repository(DjangoSectorRepository)
            existing_sector = sector_repository.get_by_name(sector_data.name)
            if existing_sector:
                self.logger.warning(
                    f"Sector with name '{sector_data.name}' already exists"
                )
                raise ConflictError()
            created_sector = sector_repository.create(sector_data)
            self.unit_of_work.commit()
            return created_sector

    def get_sector(self, sector_id: int) -> SectorEntity:
        with self.unit_of_work:
            sector_repository = self.unit_of_work.get_repository(DjangoSectorRepository)
            sector = sector_repository.get(sector_id)
            if not sector:
                raise NotFoundError()
            return sector

    def update_sector(self, sector_id: int, sector_data: SectorEntity) -> SectorEntity:
        with self.unit_of_work:
            sector_repository = self.unit_of_work.get_repository(DjangoSectorRepository)
            existing_sector = sector_repository.get(sector_id)
            if not existing_sector:
                raise NotFoundError()
            if sector_data.name and sector_data.name != existing_sector.name:
                name_exists = sector_repository.get_by_name(sector_data.name)
                if name_exists and name_exists.id != sector_id:
                    self.logger.warning(
                        f"Cannot update: Sector with name '{sector_data.name}' already exists"
                    )
                    raise ConflictError()
            updated_sector = sector_repository.update(sector_id, sector_data)
            self.unit_of_work.commit()
            return updated_sector

    def delete_sector(self, sector_id: int) -> bool:
        with self.unit_of_work:
            sector_repository = self.unit_of_work.get_repository(DjangoSectorRepository)
            existing_sector = sector_repository.get(sector_id)
            if not existing_sector:
                raise NotFoundError()
            result = sector_repository.delete(sector_id)
            self.unit_of_work.commit()
            return result

    def get_all_sectors(
        self, pagination_params: PaginationParams
    ) -> PaginatedResult[SectorEntity]:
        with self.unit_of_work:
            sector_repository = self.unit_of_work.get_repository(DjangoSectorRepository)
            return sector_repository.get_all(pagination_params)

    def get_sectors_by_region(self, region_id: int) -> List[SectorEntity]:
        with self.unit_of_work:
            sector_repository = self.unit_of_work.get_repository(DjangoSectorRepository)
            return sector_repository.get_by_region(region_id)
