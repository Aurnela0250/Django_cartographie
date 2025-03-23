from typing import List, Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from apps.school.models import School
from apps.users.models import User
from core.domain.entities.school import SchoolEntity
from core.interfaces.school_repository import SchoolRepository


class DjangoSchoolRepository(SchoolRepository):

    def _to_entity(self, db_school: School) -> SchoolEntity:
        school_dict = {
            "id": db_school.id,
            "name": db_school.name,
            "status": db_school.status,
            "description": db_school.description,
            "address": db_school.address,
            "parcours": db_school.parcours,
            "cycle": db_school.cycle,
            "image_url": db_school.image_url,
            "created_at": db_school.created_at,
            "updated_at": db_school.updated_at,
            "created_by": db_school.created_by.id if db_school.created_by else None,
            "updated_by": db_school.updated_by.id if db_school.updated_by else None,
        }
        return SchoolEntity(**school_dict)

    def _to_entity_list(self, db_objs: List[School]) -> List[SchoolEntity]:
        return [self._to_entity(obj) for obj in db_objs]

    def create(self, school: SchoolEntity) -> SchoolEntity:
        # Extraire created_by et updated_by
        created_by_id = school.created_by
        updated_by_id = school.updated_by

        # Créer un dictionnaire avec les données de l'école, en excluant id, created_by et updated_by
        school_dict = school.dict(exclude={"id", "created_by", "updated_by"})

        # Créer l'instance de School
        db_school = School(**school_dict)

        # Gérer created_by et updated_by
        if created_by_id:
            db_school.created_by = User.objects.get(id=created_by_id)
        if updated_by_id:
            db_school.updated_by = User.objects.get(id=updated_by_id)

        # Sauvegarder l'école
        db_school.save()
        return self._to_entity(db_school)

    def get(self, id: UUID) -> Optional[SchoolEntity]:
        try:
            school = School.objects.get(id=id)
            return self._to_entity(school)
        except ObjectDoesNotExist:
            return None

    def get_all(self) -> List[SchoolEntity]:
        schools = School.objects.all()
        return self._to_entity_list(list(schools))

    def update(self, id: UUID, school: SchoolEntity) -> Optional[SchoolEntity]:
        # Extraire created_by et updated_by
        created_by_id = school.created_by
        updated_by_id = school.updated_by
        try:
            db_school = School.objects.get(id=id)
            for key, value in school.dict(
                exclude={"id", "created_by", "updated_by"}
            ).items():
                setattr(db_school, key, value)

            # Gérer created_by et updated_by
            if created_by_id:
                db_school.created_by = User.objects.get(id=created_by_id)
            if updated_by_id:
                db_school.updated_by = User.objects.get(id=updated_by_id)

            db_school.save()
            return self._to_entity(db_school)
        except ObjectDoesNotExist:
            return None

    def delete(self, id: UUID) -> bool:
        try:
            school = School.objects.get(id=id)
            school.delete()
            return True
        except ObjectDoesNotExist:
            return False

    def filter(self, **kwargs) -> List[SchoolEntity]:
        query = Q()
        for key, value in kwargs.items():
            query &= Q(**{key: value})
        schools = School.objects.filter(query)
        return self._to_entity_list(list(schools))
