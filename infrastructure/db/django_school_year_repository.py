from typing import Optional

from apps.school.models import SchoolYear
from core.domain.entities.school_year import SchoolYearEntity
from core.interfaces.school_year_repository import SchoolYearRepository
from infrastructure.db.django_base_repository import DjangoBaseRepository


class DjangoSchoolYearRepository(
    DjangoBaseRepository[
        SchoolYearEntity,
        SchoolYear,
        int,
    ],
    SchoolYearRepository,
):
    def __init__(self):
        super().__init__(SchoolYear, SchoolYearEntity)

    def create(self, school_year: SchoolYearEntity) -> SchoolYearEntity:
        return super().create(school_year)

    def get(self, id: int) -> Optional[SchoolYearEntity]:
        return super().get(id)

    def get_all(self) -> list[SchoolYearEntity]:
        return super().get_all()

    def update(self, id: int, school_year: SchoolYearEntity) -> SchoolYearEntity:
        return super().update(id, school_year)

    def delete(self, id: int) -> bool:
        return super().delete(id)

    def filter(self, **kwargs) -> list[SchoolYearEntity]:
        return super().filter(**kwargs)

    # def _to_entity(self, db_school_year: SchoolYear) -> SchoolYearEntity:
    #     school_year_dict = {
    #         "id": db_school_year.id,
    #         "start_year": db_school_year.start_year,
    #         "end_year": db_school_year.end_year,
    #         "created_at": db_school_year.created_at,
    #         "updated_at": db_school_year.updated_at,
    #         "created_by": (
    #             db_school_year.created_by.id if db_school_year.created_by else None
    #         ),
    #         "updated_by": (
    #             db_school_year.updated_by.id if db_school_year.updated_by else None
    #         ),
    #     }
    #     return SchoolYearEntity(**school_year_dict)

    # def _to_entity_list(self, db_objs: List[SchoolYear]) -> List[SchoolYearEntity]:
    #     return [self._to_entity(obj) for obj in db_objs]

    # def create(self, school_year: SchoolYearEntity) -> SchoolYearEntity:
    #     created_by_id = school_year.created_by
    #     updated_by_id = school_year.updated_by

    #     school_year_dict = school_year.dict(exclude={"id", "created_by", "updated_by"})

    #     db_school_year = SchoolYear(**school_year_dict)

    #     if created_by_id:
    #         db_school_year.created_by = User.objects.get(id=created_by_id)
    #     if updated_by_id:
    #         db_school_year.updated_by = User.objects.get(id=updated_by_id)

    #     db_school_year.save()
    #     return self._to_entity(db_school_year)

    # def get(self, id: UUID) -> Optional[SchoolYearEntity]:
    #     try:
    #         school_year = SchoolYear.objects.get(id=id)
    #         return self._to_entity(school_year)
    #     except ObjectDoesNotExist:
    #         return None

    # def get_all(self) -> List[SchoolYearEntity]:
    #     school_years = SchoolYear.objects.all()
    #     return self._to_entity_list(list(school_years))

    # def update(
    #     self, id: UUID, school_year: SchoolYearEntity
    # ) -> Optional[SchoolYearEntity]:
    #     created_by_id = school_year.created_by
    #     updated_by_id = school_year.updated_by
    #     try:
    #         db_school_year = SchoolYear.objects.get(id=id)
    #         for key, value in school_year.dict(
    #             exclude={"id", "created_by", "updated_by"}
    #         ).items():
    #             setattr(db_school_year, key, value)

    #         if created_by_id:
    #             db_school_year.created_by = User.objects.get(id=created_by_id)
    #         if updated_by_id:
    #             db_school_year.updated_by = User.objects.get(id=updated_by_id)

    #         db_school_year.save()
    #         return self._to_entity(db_school_year)
    #     except ObjectDoesNotExist:
    #         return None

    # def delete(self, id: UUID) -> bool:
    #     try:
    #         school_year = SchoolYear.objects.get(id=id)
    #         school_year.delete()
    #         return True
    #     except ObjectDoesNotExist:
    #         return False

    # def filter(self, **kwargs) -> List[SchoolYearEntity]:
    #     query = Q()
    #     for key, value in kwargs.items():
    #         query &= Q(**{key: value})
    #     school_years = SchoolYear.objects.filter(query)
    #     return self._to_entity_list(list(school_years))
