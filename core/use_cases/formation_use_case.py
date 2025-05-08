import logging

from core.domain.entities.formation_authorization_entity import (
    FormationAuthorizationEntity,
)
from core.domain.entities.formation_entity import FormationEntity
from core.domain.entities.pagination import PaginatedResult, PaginationParams
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_formation_repository import DjangoFormationRepository
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnprocessableEntityError,
)


class FormationUseCase:
    """Use case for CRUD operations on formations"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_formation(self, formation_data: FormationEntity) -> FormationEntity:
        """Creates a new formation"""
        with self.unit_of_work:
            formation_repository = self.unit_of_work.get_repository(
                DjangoFormationRepository
            )

            # Check if a formation with the same intitule already exists
            existing_formation = formation_repository.get_by_intitule(
                formation_data.intitule
            )
            if existing_formation:
                self.logger.warning(
                    f"Formation with intitule '{formation_data.intitule}' already exists"
                )
                raise ConflictError()

            # Check if the level exists
            if not formation_repository.check_level_exists(formation_data.level_id):
                self.logger.warning(
                    f"Level with ID '{formation_data.level_id}' not found"
                )
                raise UnprocessableEntityError()

            # Check if the mention exists
            if not formation_repository.check_mention_exists(formation_data.mention_id):
                self.logger.warning(
                    f"Mention with ID '{formation_data.mention_id}' not found"
                )
                raise UnprocessableEntityError()

            # Check if the establishment exists
            if not formation_repository.check_establishment_exists(
                formation_data.establishment_id
            ):
                self.logger.warning(
                    f"Establishment with ID '{formation_data.establishment_id}' not found"
                )
                raise UnprocessableEntityError()

            # Check if the authorization exists (if provided)
            if (
                formation_data.authorization_id
                and not formation_repository.check_formation_authorization_exists(
                    formation_data.authorization_id
                )
            ):
                self.logger.warning(
                    f"FormationAuthorization with ID '{formation_data.authorization_id}' not found"
                )
                raise UnprocessableEntityError()

            try:
                return formation_repository.create(formation_data)
            except Exception as e:
                self.logger.error(f"Failed to create formation: {e}")
                raise InternalServerError()

    def get_formation(self, formation_id: int) -> FormationEntity:
        """Retrieves a formation by ID"""
        with self.unit_of_work:
            formation_repository = self.unit_of_work.get_repository(
                DjangoFormationRepository
            )
            try:
                formation = formation_repository.get(formation_id)
                if formation is None:
                    raise NotFoundError()
                return formation
            except NotFoundError:
                self.logger.warning(f"Formation with ID {formation_id} not found")
                raise
            except Exception as e:
                self.logger.error(f"Failed to get formation: {e}")
                raise InternalServerError()

    def update_formation(
        self,
        formation_id: int,
        formation_data: FormationEntity,
    ) -> FormationEntity:
        """Updates an existing formation"""
        with self.unit_of_work:
            formation_repository = self.unit_of_work.get_repository(
                DjangoFormationRepository
            )

            # Check if the formation exists
            try:
                formation_repository.get(formation_id)
            except NotFoundError:
                self.logger.warning(f"Formation with ID {formation_id} not found")
                raise

            # Check if the level exists
            if not formation_repository.check_level_exists(formation_data.level_id):
                self.logger.warning(
                    f"Level with ID '{formation_data.level_id}' not found"
                )
                raise UnprocessableEntityError()

            # Check if the mention exists
            if not formation_repository.check_mention_exists(formation_data.mention_id):
                self.logger.warning(
                    f"Mention with ID '{formation_data.mention_id}' not found"
                )
                raise UnprocessableEntityError()

            # Check if the establishment exists
            if not formation_repository.check_establishment_exists(
                formation_data.establishment_id
            ):
                self.logger.warning(
                    f"Establishment with ID '{formation_data.establishment_id}' not found"
                )
                raise UnprocessableEntityError()

            # Check if the authorization exists (if provided)
            if (
                formation_data.authorization_id
                and not formation_repository.check_formation_authorization_exists(
                    formation_data.authorization_id
                )
            ):
                self.logger.warning(
                    f"FormationAuthorization with ID '{formation_data.authorization_id}' not found"
                )
                raise UnprocessableEntityError()

            try:
                return formation_repository.update(formation_id, formation_data)
            except Exception as e:
                self.logger.error(f"Failed to update formation: {e}")
                raise InternalServerError()

    def delete_formation(self, formation_id: int) -> None:
        """Deletes a formation"""
        with self.unit_of_work:
            formation_repository = self.unit_of_work.get_repository(
                DjangoFormationRepository
            )
            try:
                # Check if the formation exists
                if formation_repository.get(formation_id) is None:
                    raise NotFoundError()
                formation_repository.delete(formation_id)
            except NotFoundError:
                self.logger.warning(f"Formation with ID {formation_id} not found")
                raise
            except Exception as e:
                self.logger.error(f"Failed to delete formation: {e}")
                raise InternalServerError()

    def get_all_formations(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[FormationEntity]:
        """Retrieves all formations with pagination"""
        with self.unit_of_work:
            formation_repository = self.unit_of_work.get_repository(
                DjangoFormationRepository
            )
            try:
                return formation_repository.get_all(pagination_params)
            except Exception as e:
                self.logger.error(f"Failed to get formations: {e}")
                raise InternalServerError()

    def create_authorization(
        self,
        formation_id: int,
        authorization_data: FormationAuthorizationEntity,
    ) -> FormationEntity:
        """Creates a new authorization for a formation"""
        with self.unit_of_work:
            formation_repository = self.unit_of_work.get_repository(
                DjangoFormationRepository
            )
            try:
                # Check if the formation exists
                if formation_repository.get(formation_id) is None:
                    raise NotFoundError()
                return formation_repository.create_formation_authorization(
                    formation_id, authorization_data
                )
            except NotFoundError:
                self.logger.warning(f"Formation with ID {formation_id} not found")
                raise
            except Exception as e:
                self.logger.error(f"Failed to create authorization: {e}")
                raise InternalServerError()

    def update_authorization(
        self,
        formation_id: int,
        authorization_data: FormationAuthorizationEntity,
    ) -> FormationEntity:
        """Updates the authorization for a formation"""
        with self.unit_of_work:
            formation_repository = self.unit_of_work.get_repository(
                DjangoFormationRepository
            )
            try:
                # Check if the formation exists
                formation = formation_repository.get(formation_id)
                if formation is None:
                    raise NotFoundError()
                # Check if the formation has an authorization
                if not formation.authorization_id:
                    raise UnprocessableEntityError()
                return formation_repository.update_formation_authorization(
                    formation_id,
                    authorization_data,
                )
            except NotFoundError:
                self.logger.warning(f"Formation with ID {formation_id} not found")
                raise
            except UnprocessableEntityError:
                self.logger.warning(
                    f"Formation with ID {formation_id} has no authorization to update"
                )
                raise
            except Exception as e:
                self.logger.error(f"Failed to update authorization: {e}")
                raise InternalServerError()
