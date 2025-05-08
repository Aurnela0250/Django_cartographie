# Controller

## Instructions

- Implementation des enpoints pour les requetes http de l'api

## Code example

```python
from typing import List

from ninja_extra import api_controller, http_delete, http_get, http_post, http_put

from core.use_cases.user_use_case import UserUseCase
from infrastructure.db.django_user_repository import DjangoUserRepository
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.exceptions import (
    BadRequestError,
    ConflictError,
    DatabaseError,
    InternalServerError,
    NotFoundError,
    ValidationError,
)
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.user_schema import (
    CreateUserSchemaRequest,
    CreateUserSchemaResponse,
    UserSchema,
)
from presentation.schemas.user_schema import UpdateUserSchema as UserUpdate


@api_controller("/users", tags=["Users"], auth=jwt_auth)
class UserController:
    def __init__(self):
        self.user_repository = DjangoUserRepository()
        self.unit_of_work = DjangoUnitOfWork()
        self.user_use_case = UserUseCase(self.unit_of_work)

    @http_post("/", response={201: UserSchema})
    def create_user(self, request, user_data: CreateUserSchemaRequest):
        try:
            use_case = self.user_use_case

            user = use_case.create(
                user_data,
                created_by=request.user.id,
            )
            return 201, UserSchema.from_orm(user)
        except ConflictError as e:
            raise e
        except BadRequestError as e:
            raise e
        except ValidationError as e:
            return e
        except DatabaseError as e:
            raise e
        except InternalServerError as e:
            raise e
        except Exception:
            raise InternalServerError()

    @http_get(
        "/{user_id}",
        response={
            200: UserSchema,
            401: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def get_user(self, request, user_id: int):
        try:
            use_case = self.user_use_case
            user = use_case.get(user_id)
            return UserSchema.from_orm(user)
        except Exception as e:
            raise e

    @http_get("/", response=List[UserSchema])
    def get_all_users(self):
        try:
            use_case = self.user_use_case
            users = use_case.get_all()
            return [UserSchema.from_orm(user) for user in users]
        except Exception:
            raise InternalServerError()

    @http_put("/{user_id}", response=UserSchema)
    def update_user(self, request, user_id: int, user_data: UserUpdateSchema):
        try:
            use_case = self.user_use_case
            updated_user = use_case.update(
                user_id,
                user_data,
                updated_by=request.user.id,
            )
            return UserSchema.from_orm(updated_user)
        except ValidationError:
            raise BadRequestError()
        except NotFoundError:
            raise NotFoundError()
        except DatabaseError:
            raise DatabaseError()
        except Exception:
            raise InternalServerError()

    @http_delete("/{user_id}", response={204: None})
    def delete_user(self, user_id: int):
        try:
            use_case = self.user_use_case
            use_case.delete(user_id)
            return 204, None
        except NotFoundError as e:
            raise e
        except Exception as e:
            print(e)
            raise InternalServerError()
```

# Schema

## Instruction

- Le schema est la representation de données d'entrée et de sortie d'api lors des requêtes http (Request et Response)
- En fonction de la requête est le schema d'entrée et de sortie

## Code example

```python
from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict, EmailStr

from presentation.schemas.base_schema import BaseSchema


class UserBase(Schema):
    email: EmailStr
    username: str


class UserCreate(Schema):
    email: EmailStr
    password: str


class UserSignUp(Schema):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: UUID
    email_verified: bool


class Config:
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserInDB):
    model_config = ConfigDict(from_attributes=True)



class UserAuthSchema(BaseSchema):
    id: Optional[int] = None
    email: EmailStr
    username: str
    active: bool = True
    email_verified: bool = False
    is_two_factor_enabled: bool = False
    image: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
```
