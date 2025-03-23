from typing import List
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from core.domain.entities.school_year import SchoolYearEntity
from core.interfaces.school_year_repository import SchoolYearRepository
from presentation.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ValidationError,
)


class SchoolYearUseCase:
    def __init__(self, school_year_repository: SchoolYearRepository):
        self.school_year_repository = school_year_repository

    @transaction.atomic
    def create(
        self,
        school_year_data: dict,
        created_by: UUID,
    ) -> SchoolYearEntity:
        try:
            start_year = school_year_data.get("start_year")
            end_year = school_year_data.get("end_year")

            if self.school_year_repository.filter(
                start_year=start_year,
                end_year=end_year,
            ):
                raise ConflictError(
                    f"Une année scolaire pour {school_year_data.get('start_year')}-{school_year_data.get('end_year')} existe déjà"
                )
            if end_year and end_year <= start_year:
                raise BadRequestError(
                    "L'année de fin doit être supérieure à l'année de début"
                )

            if end_year and start_year and end_year != start_year + 1:
                raise BadRequestError(
                    "L'année de début doit être exactement une année avant l'année de fin"
                )

            school_year = SchoolYearEntity(
                **school_year_data,
                created_by=created_by,
            )
            return self.school_year_repository.create(school_year)
        except ConflictError as e:
            raise e
        except BadRequestError as e:
            raise e
        except ValidationError as e:
            raise e
        except Exception as e:
            raise e

    def get(self, school_year_id: int) -> SchoolYearEntity:
        try:
            school_year = self.school_year_repository.get(school_year_id)
            if not school_year:
                raise NotFoundError(
                    f"Année scolaire avec l'ID {school_year_id} non trouvée"
                )
            return school_year
        except ObjectDoesNotExist:
            raise NotFoundError(
                f"Année scolaire avec l'ID {school_year_id} non trouvée"
            )
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise e

    @transaction.atomic
    def update(
        self,
        school_year_id: int,
        school_year_data: dict,
        updated_by: UUID,
    ) -> SchoolYearEntity:
        try:
            existing_school_year = self.school_year_repository.get(school_year_id)
            if not existing_school_year:
                raise NotFoundError(
                    f"Année scolaire avec l'ID {school_year_id} non trouvée"
                )

            start_year = school_year_data.get("start_year")
            end_year = school_year_data.get("end_year")

            if end_year and end_year <= start_year:
                raise BadRequestError(
                    "L'année de fin doit être supérieure à l'année de début"
                )

            if end_year and start_year and end_year != start_year + 1:
                raise BadRequestError(
                    "L'année de début doit être exactement une année avant l'année de fin"
                )

            updated_school_year = SchoolYearEntity(
                **{
                    **existing_school_year.model_dump(),
                    **school_year_data,
                    "updated_by": updated_by,
                }
            )
            return self.school_year_repository.update(
                school_year_id,
                updated_school_year,
            )
        except ObjectDoesNotExist:
            raise NotFoundError(
                f"Année scolaire avec l'ID {school_year_id} non trouvée"
            )
        except NotFoundError as e:
            raise e
        except BadRequestError as e:
            raise e
        except ValidationError as e:
            raise e
        except Exception as e:
            raise e

    @transaction.atomic
    def delete(self, school_year_id: int) -> bool:
        try:
            if not self.school_year_repository.get(school_year_id):
                raise NotFoundError(
                    f"Année scolaire avec l'ID {school_year_id} non trouvée"
                )
            return self.school_year_repository.delete(school_year_id)
        except ObjectDoesNotExist:
            raise NotFoundError(
                f"Année scolaire avec l'ID {school_year_id} non trouvée"
            )
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise e

    def get_all(self) -> List[SchoolYearEntity]:
        try:
            return self.school_year_repository.get_all()
        except Exception as e:
            raise e

    def filter(self, **kwargs) -> List[SchoolYearEntity]:
        try:
            return self.school_year_repository.filter(**kwargs)
        except Exception as e:
            raise e
