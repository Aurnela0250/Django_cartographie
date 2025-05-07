from typing import Optional

from apps.establishment.models import Establishment
from apps.establishment_type.models import EstablishmentType
from apps.users.models import User
from core.domain.entities.establishment_entity import EstablishmentEntity
from core.interfaces.establishment_repository import IEstablishmentRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository
from presentation.exceptions import UnprocessableEntityError


class DjangoEstablishmentRepository(
    DjangoBaseRepository[EstablishmentEntity, Establishment, int],
    IEstablishmentRepository,
):
    """Django implementation of the repository for establishments"""

    def __init__(self):
        super().__init__(Establishment, EstablishmentEntity)

    def _to_entity(self, db_obj: Establishment) -> EstablishmentEntity:
        """Converts a database object to an entity"""
        # Get base entity data (id, created_at, etc.)
        obj_dict = super()._to_entity(db_obj).model_dump()

        # Add establishment type ID
        if db_obj.establishment_type:
            obj_dict["establishment_type_id"] = db_obj.establishment_type.id  # type: ignore

        return EstablishmentEntity(**obj_dict)

    def get_by_name(self, name: str) -> Optional[EstablishmentEntity]:
        """Retrieves an establishment by its name"""
        try:
            establishment = self.model.objects.get(name=name)
            return self._to_entity(establishment)
        except self.model.DoesNotExist:
            return None

    def check_establishment_type_exists(self, establishment_type_id: int) -> bool:
        """Checks if the establishment type with the given ID exists"""
        return EstablishmentType.objects.filter(id=establishment_type_id).exists()

    def create(self, obj: EstablishmentEntity) -> EstablishmentEntity:
        """Creates a new establishment"""
        if not self.check_establishment_type_exists(obj.establishment_type_id):
            raise UnprocessableEntityError()

        created_by_id = obj.created_by
        updated_by_id = obj.updated_by

        obj_dict = obj.model_dump(
            exclude={
                "id",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
                "establishment_type_id",
            }
        )

        db_obj = self.model(**obj_dict)

        # Set the establishment_type
        db_obj.establishment_type = EstablishmentType.objects.get(
            id=obj.establishment_type_id
        )

        # Set tracking fields
        if created_by_id:
            db_obj.created_by = User.objects.get(id=created_by_id)

        if updated_by_id:
            db_obj.updated_by = User.objects.get(id=updated_by_id)

        db_obj.save()
        return self._to_entity(db_obj)
