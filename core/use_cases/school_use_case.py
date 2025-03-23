from typing import List
from uuid import UUID

from django.db import transaction

from core.domain.entities.school import SchoolEntity
from core.interfaces.school_repository import SchoolRepository
from presentation.exceptions import (
    ConflictError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)


class CreateSchoolUseCase:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    @transaction.atomic
    def execute(self, school_data: dict, created_by: UUID) -> SchoolEntity:
        try:
            # Vérifier si l'école existe déjà
            if self.school_repository.filter(name=school_data.get("name")):
                raise ConflictError(
                    f"Une école avec le nom '{school_data.get('name')}' existe déjà"
                )

            school = SchoolEntity(**school_data, created_by=created_by)

            return self.school_repository.create(school)
        except ConflictError as e:
            raise e
        except ValidationError as e:
            raise (e)
        except Exception as e:
            raise (e)


class UpdateSchoolUseCase:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    @transaction.atomic
    def execute(self, id: UUID, school_data: dict, updated_by: UUID) -> SchoolEntity:
        try:
            existing_school = self.school_repository.get(id)
            if not existing_school:
                raise NotFoundError(f"Aucune école trouvée avec l'ID : {id}")
            updated_school = SchoolEntity(
                **{**existing_school.dict(), **school_data},
            )
            updated_school.updated_by = updated_by
            updated_school = self.school_repository.update(id, updated_school)
            if not updated_school:
                raise InternalServerError(
                    f"Erreur lors de la mise à jour de l'école avec l'ID : {id}"
                )
            return updated_school
        except NotFoundError as e:
            raise e
        except ValidationError as e:
            raise ValidationError(
                f"Erreur de validation lors de la mise à jour de l'école : {str(e)}"
            )
        except Exception as e:
            raise InternalServerError(
                f"Erreur inattendue lors de la mise à jour de l'école : {str(e)}"
            )


class DeleteSchoolUseCase:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    @transaction.atomic
    def execute(self, id: UUID) -> bool:
        try:
            if not self.school_repository.get(id):
                raise NotFoundError(f"Aucune école trouvée avec l'ID : {id}")
            return self.school_repository.delete(id)
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise InternalServerError(
                f"Erreur inattendue lors de la suppression de l'école : {str(e)}"
            )


class GetSchoolUseCase:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    def execute(self, id: UUID) -> SchoolEntity:
        school = self.school_repository.get(id)
        if not school:
            raise NotFoundError(f"Aucune école trouvée avec l'ID : {id}")
        return school


class GetAllSchoolsUseCase:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    def execute(self) -> List[SchoolEntity]:
        try:
            return self.school_repository.get_all()
        except Exception as e:
            raise InternalServerError(
                f"Erreur lors de la récupération de toutes les écoles : {str(e)}"
            )


class FilterSchoolsUseCase:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repository = school_repository

    def execute(self, **kwargs) -> List[SchoolEntity]:
        try:
            return self.school_repository.filter(**kwargs)
        except Exception as e:
            raise InternalServerError(f"Erreur lors du filtrage des écoles : {str(e)}")
