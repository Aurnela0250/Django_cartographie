from typing import Generic, List, Optional, Type, TypeVar

from django.db import models
from django.db.models import Q
from pydantic import BaseModel

from apps.users.models import User

T = TypeVar("T", bound=BaseModel)
M = TypeVar("M", bound=models.Model)
ID = TypeVar("ID", int, str)


class DjangoBaseRepository(Generic[T, M, ID]):
    def __init__(self, model: Type[M], entity: Type[T]):
        self.model = model
        self.entity = entity

    def _to_entity(self, db_obj: M) -> T:
        obj_dict = {
            "id": db_obj.id,  # type: ignore
            "created_at": db_obj.created_at,  # type: ignore
            "updated_at": db_obj.updated_at,  # type: ignore
            "created_by": db_obj.created_by.id if db_obj.created_by else None,  # type: ignore
            "updated_by": db_obj.updated_by.id if db_obj.updated_by else None,  # type: ignore
        }

        # Traiter tous les autres champs sauf ceux déjà définis
        exclude_fields = {"id", "created_at", "updated_at", "created_by", "updated_by"}

        for field in self.entity.__annotations__:
            if hasattr(db_obj, field) and field not in exclude_fields:
                obj_dict[field] = getattr(db_obj, field)

        return self.entity(**obj_dict)

    def _to_entity_list(self, db_objs: List[M]) -> List[T]:
        return [self._to_entity(obj) for obj in db_objs]

    def create(self, obj: T) -> T:
        created_by_id = obj.created_by  # type: ignore
        updated_by_id = obj.updated_by  # type: ignore

        obj_dict = obj.model_dump(
            exclude={"id", "created_by", "updated_by", "created_at", "updated_at"}
        )

        db_obj = self.model(**obj_dict)

        if created_by_id:
            db_obj.created_by = User.objects.get(id=created_by_id)  # type: ignore
        if updated_by_id:
            db_obj.updated_by = User.objects.get(id=updated_by_id)  # type: ignore

        db_obj.save()
        return self._to_entity(db_obj)

    def get(self, id: ID) -> Optional[T]:
        obj = self.model.objects.get(id=id)
        return self._to_entity(obj)

    def get_all(self) -> List[T]:
        objs = self.model.objects.all()
        return self._to_entity_list(list(objs))

    def update(self, id: ID, obj: T) -> T:
        created_by_id = obj.created_by  # type: ignore
        updated_by_id = obj.updated_by  # type: ignore

        db_obj = self.model.objects.get(id=id)
        for key, value in obj.model_dump(
            exclude={"id", "created_by", "updated_by"}
        ).items():
            setattr(db_obj, key, value)

        if created_by_id:
            db_obj.created_by = User.objects.get(id=created_by_id)  # type: ignore
        if updated_by_id:
            db_obj.updated_by = User.objects.get(id=updated_by_id)  # type: ignore

        db_obj.save()
        return self._to_entity(db_obj)

    def delete(self, id: ID) -> bool:
        obj = self.model.objects.get(id=id)
        obj.delete()
        return True

    def filter(self, **kwargs) -> List[T]:
        query = Q()
        for key, value in kwargs.items():
            query &= Q(**{key: value})
        objs = self.model.objects.filter(query)
        return self._to_entity_list(list(objs))
