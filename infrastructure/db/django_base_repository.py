import logging  # Added import for logging
from typing import Generic, List, Optional, Type, TypeVar

from django.db import IntegrityError, models
from django.db.models import Q
from pydantic import BaseModel

from apps.users.models import User
from core.domain.entities.pagination import (
    PaginatedResult,
    PaginationParams,
)
from presentation.exceptions import (
    ConflictError,
    DatabaseError,
    NotFoundError,
)

logger = logging.getLogger(__name__)  # Added logger instance

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
        exclude_fields = {
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        }

        for field in self.entity.__annotations__:
            if hasattr(db_obj, field) and field not in exclude_fields:
                obj_dict[field] = getattr(db_obj, field)

        return self.entity(**obj_dict)

    def _to_entity_list(self, db_objs: List[M]) -> List[T]:
        return [self._to_entity(obj) for obj in db_objs]

    def _to_pagination_result(
        self, queryset: models.QuerySet, pagination_params: PaginationParams
    ) -> PaginatedResult[T]:
        """Crée un résultat paginé à partir d'un queryset"""
        # Calculer le nombre total d'éléments
        total_items = queryset.count()

        # Paginer les résultats
        paginated_queryset = queryset[
            pagination_params.offset : pagination_params.offset
            + pagination_params.limit
        ]

        # Calculer le nombre total de pages
        total_pages = (
            total_items + pagination_params.per_page - 1
        ) // pagination_params.per_page

        # Calculer la page suivante et précédente
        next_page = (
            pagination_params.page + 1 if pagination_params.page < total_pages else None
        )
        previous_page = (
            pagination_params.page - 1 if pagination_params.page > 1 else None
        )

        # Retourner un résultat paginé
        return PaginatedResult(
            items=self._to_entity_list(list(paginated_queryset)),
            total_items=total_items,
            page=pagination_params.page,
            per_page=pagination_params.per_page,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

    def create(self, obj: T) -> T:
        created_by_id = obj.created_by  # type: ignore
        updated_by_id = obj.updated_by  # type: ignore

        obj_dict = obj.model_dump(
            exclude={
                "id",
                "created_by",
                "updated_by",
                "created_at",
                "updated_at",
            }
        )

        db_obj = self.model(**obj_dict)

        if created_by_id:
            db_obj.created_by = User.objects.get(id=created_by_id)  # type: ignore
        if updated_by_id:
            db_obj.updated_by = User.objects.get(id=updated_by_id)  # type: ignore

        db_obj.save()
        return self._to_entity(db_obj)

    def get(self, id: ID) -> Optional[T]:
        try:
            obj = self.model.objects.get(id=id)
            return self._to_entity(obj)
        except self.model.DoesNotExist:
            logger.warning(f"{self.model.__name__} with id {id} not found.")
            raise NotFoundError()
        except Exception as e:
            logger.error(
                f"Database error retrieving {self.model.__name__} with id {id}: {e}",
                exc_info=True,
            )
            raise DatabaseError()

    def get_all(
        self,
        pagination_params: PaginationParams,
    ) -> PaginatedResult[T]:
        """Récupère tous les objets avec pagination"""
        queryset = self.model.objects.all()
        return self._to_pagination_result(queryset, pagination_params)

    def update(self, id: ID, obj: T) -> T:
        try:
            updated_by_id = obj.updated_by  # type: ignore

            db_obj = self.model.objects.get(id=id)
            for key, value in obj.model_dump(
                exclude={"id", "created_by", "updated_by", "created_at", "updated_at"}
            ).items():
                setattr(db_obj, key, value)

            if updated_by_id:
                db_obj.updated_by = User.objects.get(id=updated_by_id)  # type: ignore

            db_obj.save()
            return self._to_entity(db_obj)
        except self.model.DoesNotExist:
            logger.warning(f"{self.model.__name__} with id {id} not found for update.")
            raise NotFoundError()  # Call exception without arguments
        except IntegrityError as e:
            logger.error(
                f"Database integrity error updating {self.model.__name__} with id {id}: {e}",
                exc_info=True,
            )
            # Using ConflictError for unique constraints, adjust if needed for other IntegrityErrors
            raise ConflictError()  # Call exception without arguments
        except Exception as e:
            logger.error(
                f"Database error updating {self.model.__name__} with id {id}: {e}",
                exc_info=True,
            )
            raise DatabaseError()  # Call exception without arguments

    def delete(self, id: ID) -> bool:
        try:
            obj = self.model.objects.get(id=id)
            obj.delete()
            return True
        except self.model.DoesNotExist:
            logger.warning(
                f"{self.model.__name__} with id {id} not found for deletion."
            )
            raise NotFoundError()  # Call exception without arguments
        except Exception as e:
            logger.error(
                f"Database error deleting {self.model.__name__} with id {id}: {e}",
                exc_info=True,
            )
            raise DatabaseError()  # Call exception without arguments

    def filter(
        self,
        pagination_params: PaginationParams,
        **kwargs,
    ) -> PaginatedResult[T]:
        """Filtre les objets avec pagination"""
        query = Q()
        for key, value in kwargs.items():
            query &= Q(**{key: value})
        queryset = self.model.objects.filter(query)
        return self._to_pagination_result(queryset, pagination_params)
