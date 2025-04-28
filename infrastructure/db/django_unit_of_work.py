from typing import Dict, Type, TypeVar

from django.db import transaction

from core.interfaces.base_repository import BaseRepository
from core.interfaces.unit_of_work import UnitOfWork

T = TypeVar("T")


class DjangoUnitOfWork(UnitOfWork):
    def __init__(self):
        self._repositories: Dict[Type[BaseRepository], BaseRepository] = {}

    def __enter__(self) -> "DjangoUnitOfWork":
        transaction.set_autocommit(False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            try:
                self.commit()
            except:
                self.rollback()
                raise
            finally:
                transaction.set_autocommit(True)
        self._repositories.clear()

    def commit(self):
        transaction.commit()

    def rollback(self):
        transaction.rollback()

    def get_repository(
        self, repository_class: Type[BaseRepository[T]]
    ) -> BaseRepository[T]:
        if repository_class not in self._repositories:
            self._repositories[repository_class] = repository_class()
        return self._repositories[repository_class]
