import logging
from typing import List

from core.domain.entities.establishment_type_entity import EstablishmentTypeEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_establishment_type_repository import (
    DjangoEstablishmentTypeRepository,
)
from presentation.exceptions import ConflictError, NotFoundError, InternalServerError


class EstablishmentTypeUseCase:
    """Use case for CRUD operations on establishment types"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_establishment_type(
        self, establishment_type_data: EstablishmentTypeEntity
    ) -> EstablishmentTypeEntity:
        """Creates a new establishment type"""
        with self.unit_of_work:
            establishment_type_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentTypeRepository
            )

            # Check if an establishment type with the same name already exists
            existing_establishment_type = establishment_type_repository.get_by_name(
                establishment_type_data.name
            )
            if existing_establishment_type:
                self.logger.warning(
                    f"Establishment type with name '{establishment_type_data.name}' already exists"
                )
                raise ConflictError()

            # Create the establishment type
            created_establishment_type = establishment_type_repository.create(
                establishment_type_data
            )
            self.unit_of_work.commit()
            return created_establishment_type

    def get_establishment_type(
        self, establishment_type_id: int
    ) -> EstablishmentTypeEntity:
        """Retrieves an establishment type by its ID"""
        with self.unit_of_work:
            establishment_type_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentTypeRepository
            )
            establishment_type = establishment_type_repository.get(
                establishment_type_id
            )
            if not establishment_type:
                raise NotFoundError()
            return establishment_type

    def update_establishment_type(
        self,
        establishment_type_id: int,
        establishment_type_data: EstablishmentTypeEntity,
    ) -> EstablishmentTypeEntity:
        """Updates an existing establishment type"""
        with self.unit_of_work:
            establishment_type_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentTypeRepository
            )

            # Check if the establishment type exists
            existing_establishment_type = establishment_type_repository.get(
                establishment_type_id
            )
            if not existing_establishment_type:
                raise NotFoundError()

            # Check if the new name already exists for another establishment type
            if establishment_type_data.name != existing_establishment_type.name:
                name_exists = establishment_type_repository.get_by_name(
                    establishment_type_data.name
                )
                if name_exists and name_exists.id != establishment_type_id:
                    self.logger.warning(
                        f"Cannot update: Establishment type with name '{establishment_type_data.name}' already exists"
                    )
                    raise ConflictError()

            # Update the establishment type
            updated_establishment_type = establishment_type_repository.update(
                establishment_type_id, establishment_type_data
            )
            self.unit_of_work.commit()
            return updated_establishment_type

    def delete_establishment_type(self, establishment_type_id: int) -> bool:
        """Deletes an establishment type"""
        with self.unit_of_work:
            establishment_type_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentTypeRepository
            )

            # Check if the establishment type exists
            existing_establishment_type = establishment_type_repository.get(
                establishment_type_id
            )
            if not existing_establishment_type:
                raise NotFoundError()

            # Delete the establishment type
            result = establishment_type_repository.delete(establishment_type_id)
            self.unit_of_work.commit()
            return result

    def get_all_establishment_types(self) -> List[EstablishmentTypeEntity]:
        """Retrieves all establishment types"""
        with self.unit_of_work:
            establishment_type_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentTypeRepository
            )
            return establishment_type_repository.get_all()

    def filter_establishment_types(self, **kwargs) -> List[EstablishmentTypeEntity]:
        """Filters establishment types based on provided criteria"""
        with self.unit_of_work:
            establishment_type_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentTypeRepository
            )
            return establishment_type_repository.filter(**kwargs)
