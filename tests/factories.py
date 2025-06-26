from polyfactory.factories.pydantic_factory import ModelFactory

from core.entities.domain import DomainEntity
from core.entities.user import UserEntity
from presentation.schemas.domain import (
    CreateDomainSchema,
    DomainSchema,
    UpdateDomainSchema,
)


# ================= Entity Factories =================
class DomainEntityFactory(ModelFactory[DomainEntity]):
    __model__ = DomainEntity


class UserEntityFactory(ModelFactory[UserEntity]):
    __model__ = UserEntity


# ================= Schema Factories =================
class CreateDomainSchemaFactory(ModelFactory[CreateDomainSchema]):
    __model__ = CreateDomainSchema


class UpdateDomainSchemaFactory(ModelFactory[UpdateDomainSchema]):
    __model__ = UpdateDomainSchema


class DomainSchemaFactory(ModelFactory[DomainSchema]):
    __model__ = DomainSchema
