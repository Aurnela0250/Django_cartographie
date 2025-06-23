from polyfactory.factories.pydantic_factory import ModelFactory

from core.entities.domain import DomainEntity
from core.entities.user import UserEntity


class DomainFactory(ModelFactory[DomainEntity]):
    __model__ = DomainEntity


class UserFactory(ModelFactory[UserEntity]):
    __model__ = UserEntity
