import logging

from core.domain.entities.annual_headcount_entity import AnnualHeadCountEntity
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

    def add_annual_headcount(
        self,
        formation_id: int,
        annual_headcount_data: AnnualHeadCountEntity,
    ) -> FormationEntity:
        with self.unit_of_work:
            try:
                formation_repository = self.unit_of_work.get_repository(
                    DjangoFormationRepository
                )

                # Vérifier que la formation existe
                formation = formation_repository.get(formation_id)
                if not formation:
                    self.logger.warning(f"Formation avec ID {formation_id} non trouvée")
                    raise UnprocessableEntityError()

                # Vérifier qu'il n'y a pas déjà un effectif pour cette année
                existing_headcount = (
                    formation_repository.get_annual_headcount_by_formation_and_year(
                        formation_id=formation_id,
                        academic_year=annual_headcount_data.academic_year,
                    )
                )

                if existing_headcount:
                    self.logger.warning(
                        f"Un effectif annuel existe déjà pour la formation {formation_id} "
                        f"et l'année universitaire {annual_headcount_data.academic_year}"
                    )
                    raise ConflictError()

                # Assurer que l'ID de formation est correctement défini
                annual_headcount_data.formation_id = formation_id

                # Créer l'effectif annuel et récupérer la formation mise à jour
                return formation_repository.create_annual_headcount(
                    annual_headcount_data
                )

                # Retourner la formation mise à jour
                return formation_repository.get(formation_id)

            except UnprocessableEntityError:
                raise
            except ConflictError:
                raise
            except Exception as e:
                self.logger.error(f"Erreur lors de l'ajout d'un effectif annuel: {e}")
                raise InternalServerError()

    def update_annual_headcount(
        self,
        annual_headcount_id: int,
        annual_headcount_data: AnnualHeadCountEntity,
    ) -> FormationEntity:
        with self.unit_of_work:
            try:
                formation_repository = self.unit_of_work.get_repository(
                    DjangoFormationRepository
                )

                # Récupérer l'effectif annuel existant
                existing_headcount = formation_repository.get_annual_headcount(
                    annual_headcount_id
                )
                if not existing_headcount:
                    self.logger.warning(
                        f"Effectif annuel avec ID {annual_headcount_id} non trouvé"
                    )
                    raise NotFoundError()

                # Si l'année académique est modifiée, vérifier qu'il n'y a pas déjà un effectif pour cette nouvelle année
                if (
                    annual_headcount_data.academic_year
                    != existing_headcount.academic_year
                ):
                    duplicate_check = (
                        formation_repository.get_annual_headcount_by_formation_and_year(
                            existing_headcount.formation_id,
                            annual_headcount_data.academic_year,
                        )
                    )
                    if duplicate_check:
                        self.logger.warning(
                            f"Un effectif annuel existe déjà pour la formation {existing_headcount.formation_id} "
                            f"et l'année universitaire {annual_headcount_data.academic_year}"
                        )
                        raise ConflictError()

                # Conserver la formation_id d'origine
                annual_headcount_data.formation_id = existing_headcount.formation_id

                # Mettre à jour l'effectif annuel et récupérer la formation mise à jour
                return formation_repository.update_annual_headcount(
                    annual_headcount_id, annual_headcount_data
                )

            except NotFoundError:
                raise
            except ConflictError:
                raise
            except Exception as e:
                self.logger.error(
                    f"Erreur lors de la mise à jour d'un effectif annuel: {e}"
                )
                raise InternalServerError()

    def delete_annual_headcount(
        self,
        annual_headcount_id: int,
    ) -> None:
        with self.unit_of_work:
            try:
                formation_repository = self.unit_of_work.get_repository(
                    DjangoFormationRepository
                )

                # Récupérer l'effectif annuel pour vérifier son existence et obtenir l'ID de formation
                annual_headcount = formation_repository.get_annual_headcount(
                    annual_headcount_id
                )
                if not annual_headcount:
                    self.logger.warning(
                        f"Effectif annuel avec ID {annual_headcount_id} non trouvé"
                    )
                    raise UnprocessableEntityError()

                # Supprimer l'effectif annuel
                formation_repository.delete_annual_headcount(annual_headcount_id)

                # Retourner la formation mise à jour
                return None

            except UnprocessableEntityError:
                raise
            except Exception as e:
                self.logger.error(
                    f"Erreur lors de la suppression d'un effectif annuel: {e}"
                )
                raise InternalServerError()
