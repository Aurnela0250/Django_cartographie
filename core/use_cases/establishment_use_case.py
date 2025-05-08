import logging

from core.domain.entities.establishment_entity import EstablishmentEntity
from core.domain.entities.pagination import PaginatedResult, PaginationParams
from core.domain.entities.rate_entity import RateEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_establishment_repository import (
    DjangoEstablishmentRepository,
)
from infrastructure.db.django_rate_repository import DjangoRateRepository
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    PydanticValidationError,
    UnprocessableEntityError,
    ValidationError,
)


class EstablishmentUseCase:
    """Use case for CRUD operations on establishments"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_establishment(
        self, establishment_data: EstablishmentEntity
    ) -> EstablishmentEntity:
        """Creates a new establishment"""
        with self.unit_of_work:
            establishment_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentRepository
            )

            # Check if an establishment with the same name already exists
            existing_establishment = establishment_repository.get_by_name(
                establishment_data.name
            )
            if existing_establishment:
                self.logger.warning(
                    f"Establishment with name '{establishment_data.name}' already exists"
                )
                raise ConflictError()

            # Check if the establishment type exists
            if not establishment_repository.check_establishment_type_exists(
                establishment_data.establishment_type_id
            ):
                self.logger.warning(
                    f"Establishment type with ID '{establishment_data.establishment_type_id}' not found"
                )
                raise UnprocessableEntityError()

            # Check if the sector exists
            if not establishment_repository.check_sector_exists(
                establishment_data.sector_id
            ):
                self.logger.warning(
                    f"Sector with ID '{establishment_data.sector_id}' not found"
                )
                raise UnprocessableEntityError()

            try:
                return establishment_repository.create(establishment_data)
            except Exception as e:
                self.logger.error(f"Failed to create establishment: {e}")
                raise InternalServerError()

    def get_establishment(self, establishment_id: int) -> EstablishmentEntity:
        """Retrieves an establishment by ID"""
        with self.unit_of_work:
            establishment_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentRepository
            )
            try:
                establishment = establishment_repository.get(establishment_id)
                if establishment is None:
                    raise NotFoundError()
                return establishment
            except NotFoundError:
                self.logger.warning(
                    f"Establishment with ID {establishment_id} not found"
                )
                raise
            except Exception as e:
                self.logger.error(f"Failed to get establishment: {e}")
                raise InternalServerError()

    def update_establishment(
        self, establishment_id: int, establishment_data: EstablishmentEntity
    ) -> EstablishmentEntity:
        """Updates an existing establishment"""
        with self.unit_of_work:
            establishment_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentRepository
            )

            # Check if the establishment exists
            try:
                establishment_repository.get(establishment_id)
            except NotFoundError:
                self.logger.warning(
                    f"Establishment with ID {establishment_id} not found"
                )
                raise

            # Check if the establishment type exists (if provided)
            if (
                establishment_data.establishment_type_id
                and not establishment_repository.check_establishment_type_exists(
                    establishment_data.establishment_type_id
                )
            ):
                self.logger.warning(
                    f"Establishment type with ID '{establishment_data.establishment_type_id}' not found"
                )
                raise NotFoundError()

            # Check if the sector exists (if provided)
            if (
                establishment_data.sector_id
                and not establishment_repository.check_sector_exists(
                    establishment_data.sector_id
                )
            ):
                self.logger.warning(
                    f"Sector with ID '{establishment_data.sector_id}' not found"
                )
                raise NotFoundError()

            try:
                return establishment_repository.update(
                    establishment_id, establishment_data
                )
            except NotFoundError:
                raise
            except ConflictError:
                raise
            except Exception as e:
                self.logger.error(f"Failed to update establishment: {e}")
                raise InternalServerError()

    def delete_establishment(self, establishment_id: int) -> bool:
        """Deletes an establishment"""
        with self.unit_of_work:
            establishment_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentRepository
            )
            try:
                return establishment_repository.delete(establishment_id)
            except NotFoundError:
                self.logger.warning(
                    f"Establishment with ID {establishment_id} not found"
                )
                raise
            except Exception as e:
                self.logger.error(f"Failed to delete establishment: {e}")
                raise InternalServerError()

    def get_all_establishments(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[EstablishmentEntity]:
        """Retrieves all establishments with pagination"""
        with self.unit_of_work:
            establishment_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentRepository
            )
            try:
                return establishment_repository.get_all(
                    pagination_params=pagination_params
                )

            except PydanticValidationError as e:
                self.logger.warning(f"Validation error occurred: {e}")
                raise ValidationError(e)
            except Exception as e:
                self.logger.error(f"Failed to get all establishments: {e}")
                raise InternalServerError()

    def rate_establishment(
        self,
        establishment_id: int,
        user_id: int,
        rating: float,
    ) -> bool:
        """
        Enregistre une notation d'un utilisateur pour un établissement.

        Args:
            establishment_id: L'identifiant de l'établissement
            user_id: L'identifiant de l'utilisateur qui note
            rating: La note à attribuer (généralement entre 0 et 5)

        Returns:
            bool: True si la notation a été créée avec succès, False sinon
        """
        with self.unit_of_work:
            establishment_repository = self.unit_of_work.get_repository(
                DjangoEstablishmentRepository
            )

            rate_repository = self.unit_of_work.get_repository(DjangoRateRepository)

            try:
                # Vérification que la valeur du rating est valide
                if rating < 0 or rating > 5:
                    self.logger.warning(
                        f"Rating invalide: {rating}. Doit être entre 0 et 5."
                    )
                    raise ValidationError()

                # Vérifier que l'établissement existe
                establishment = establishment_repository.get(establishment_id)
                if not establishment:
                    self.logger.warning(
                        f"Établissement avec ID {establishment_id} non trouvé"
                    )
                    raise UnprocessableEntityError()

                # Vérifier si l'utilisateur a déjà noté cet établissement
                if rate_repository.check_if_user_already_rate(
                    user_id,
                    establishment_id,
                ):
                    self.logger.warning(
                        f"L'utilisateur {user_id} a déjà noté l'établissement {establishment_id}"
                    )
                    return True

                # Créer une nouvelle notation
                rate_entity = RateEntity(
                    establishment_id=establishment_id,
                    user_id=user_id,
                    rating=rating,
                )

                # Enregistrer la notation
                rate_repository.create_rate(rate_entity)

                return True

            except UnprocessableEntityError:
                self.logger.warning(
                    f"Établissement avec ID {establishment_id} non trouvé"
                )
                raise
            except ValidationError:
                raise
            except Exception as e:
                self.logger.error(
                    f"Erreur lors de l'enregistrement de la notation: {e}"
                )
                raise InternalServerError()
