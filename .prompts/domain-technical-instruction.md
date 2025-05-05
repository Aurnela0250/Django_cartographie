# Entities

## Instructions

- Les entites doivent être un model `pydantic` se référer au lien `https://docs.pydantic.dev/latest/migration/`
- Conventions des noms des fichiers doivient terminer par `_entity.py`

## Code example

```python
from typing import List, Dict, Optional, Union, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MyEntity(BaseModel):
    id: Optional[int]
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

# Repository Interfaces

## Instructions

- Convention name class `I`+`Name`+`Repository` => `INameRepository(ABC)`
- Conventions des noms des fichiers doivient terminer par `name`+`_repository.py` => `name_repository.py`

## Code example

```python
from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.user_entity import UserEntity


class INameRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        pass
```

# UseCases

## Instructions

- Le use doit être composé l'interface de `UnitOfWork` dans le constructeur
- Identifier et gérer tous les erreurs probable de se produire dans l'execution des use cases.
- Les fonctionnalité dans les use case n'ont pas les même types d'erreur. Adapter la gestion des erreurs pour chaque fonctionnalité.
- Convention des nom de class `Name`+`UseCase` => `NameUseCase`
- Conventions des noms des fichiers doivient terminer par `name`+`_use_case.py` => `name_use_case.py`

## Code example

- Ceci est uniquement à titre d'exemple

```python
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_user_repository import DjangoUserRepository
from presentation.exceptions import (
    ConflictError,
    DatabaseError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)

class MyUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work

    def create_user(
        self,
        user_data: CreateUserSchemaRequest,
        created_by: int,
    ) -> UserEntity:

        with self.unit_of_work:
            try:
                user_repository = self.unit_of_work.get_repository(
                    DjangoUserRepository
                )
                user = userEntity(**user_data.dict(), created_by=created_by)
                user_created = user_repository.create_user(user)
                return user_created
            except ConflictError as e:
                raise e
            except ValidationError as e:
                raise e
            except DjangoDataBaseError:
                raise DatabaseError()
            except Exception:
                raise InternalServerError()

    def update(
        self,
        id: int,
        user_data: UpdateUserSchemaRequest,
        updated_by: int,
    ) -> UserEntity:

        with self.unit_of_work:
            try:
                # Instructions
            except ConflictError as e:
                raise e
            except ValidationError as e:
                raise e
            except DjangoDataBaseError:
                raise DatabaseError()
            except Exception:
                raise InternalServerError()

    def delete(
        self,
        id: int
    ) -> bool:

        with self.unit_of_work:
            try:
                # Instructions
            except ConflictError as e:
                raise e
            except ValidationError as e:
                raise e
            except DjangoDataBaseError:
                raise DatabaseError()
            except Exception:
                raise InternalServerError()

    def get(
        self,
        id: int
    ) -> UserEntity:

        try:
            # Instructions
        except NotFoundError as e:
            raise e
        except ValidationError as e:
            raise e
        except DjangoDataBaseError:
            raise DatabaseError()
        except Exception:
            raise InternalServerError()

    def get_all(
        self,
    ) -> List[UserEntity]:

        try:
            # Instructions
        except ValidationError as e:
            raise e
        except DjangoDataBaseError:
            raise DatabaseError()
        except Exception:
            raise InternalServerError()
```
