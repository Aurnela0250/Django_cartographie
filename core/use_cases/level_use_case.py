import logging
from typing import List

from core.domain.entities.level_entity import LevelEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_level_repository import DjangoLevelRepository
from presentation.exceptions import ConflictError, NotFoundError


class LevelUseCase:
    """Use case for CRUD operations on levels"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_level(self, level_data: LevelEntity) -> LevelEntity:
        """Creates a new level"""
        with self.unit_of_work:
            level_repository = self.unit_of_work.get_repository(DjangoLevelRepository)

            # Check if a level with the same name already exists
            existing_level = level_repository.get_by_name(level_data.name)
            if existing_level:
                self.logger.warning(
                    f"Level with name '{level_data.name}' already exists"
                )
                raise ConflictError()

            # Check if a level with the same acronym already exists
            if level_data.acronyme is not None:
                existing_level = level_repository.get_by_acronyme(level_data.acronyme)
                if existing_level:
                    self.logger.warning(
                        f"Level with acronym '{level_data.acronyme}' already exists"
                    )
                    raise ConflictError()

            # Create the level
            created_level = level_repository.create(level_data)
            self.unit_of_work.commit()
            return created_level

    def get_level(self, level_id: int) -> LevelEntity:
        """Retrieves a level by its ID"""
        with self.unit_of_work:
            level_repository = self.unit_of_work.get_repository(DjangoLevelRepository)
            level = level_repository.get(level_id)
            if not level:
                raise NotFoundError()
            return level

    def update_level(self, level_id: int, level_data: LevelEntity) -> LevelEntity:
        """Updates an existing level"""
        with self.unit_of_work:
            level_repository = self.unit_of_work.get_repository(DjangoLevelRepository)

            # Check if the level exists
            existing_level = level_repository.get(level_id)
            if not existing_level:
                raise NotFoundError()

            # Check if the new name already exists for another level
            if level_data.name != existing_level.name:
                name_exists = level_repository.get_by_name(level_data.name)
                if name_exists and name_exists.id != level_id:
                    self.logger.warning(
                        f"Cannot update: Level with name '{level_data.name}' already exists"
                    )
                    raise ConflictError()

            # Check if the new acronym already exists for another level
            if (
                level_data.acronyme is not None
                and level_data.acronyme != existing_level.acronyme
            ):
                acronyme_exists = level_repository.get_by_acronyme(level_data.acronyme)
                if acronyme_exists and acronyme_exists.id != level_id:
                    self.logger.warning(
                        f"Cannot update: Level with acronym '{level_data.acronyme}' already exists"
                    )
                    raise ConflictError()

            # Update the level
            updated_level = level_repository.update(level_id, level_data)
            self.unit_of_work.commit()
            return updated_level

    def delete_level(self, level_id: int) -> bool:
        """Deletes a level"""
        with self.unit_of_work:
            level_repository = self.unit_of_work.get_repository(DjangoLevelRepository)

            # Check if the level exists
            existing_level = level_repository.get(level_id)
            if not existing_level:
                raise NotFoundError()

            # Delete the level
            result = level_repository.delete(level_id)
            self.unit_of_work.commit()
            return result

    def get_all_levels(self) -> List[LevelEntity]:
        """Retrieves all levels"""
        with self.unit_of_work:
            level_repository = self.unit_of_work.get_repository(DjangoLevelRepository)
            return level_repository.get_all()

    def filter_levels(self, **kwargs) -> List[LevelEntity]:
        """Filters levels based on provided criteria"""
        with self.unit_of_work:
            level_repository = self.unit_of_work.get_repository(DjangoLevelRepository)
            return level_repository.filter(**kwargs)
