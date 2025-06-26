import pytest

from core.container.container import Container
from core.interfaces.domain_repository import IDomainRepository
from core.interfaces.user_repository import IUserRepository
from presentation.exceptions import DatabaseDoesNotExistException
from tests.factories import DomainEntityFactory, UserEntityFactory

pytestmark = pytest.mark.integration


async def test_delete_domain_successfully(container: Container) -> None:
    # Given
    domain_repository: IDomainRepository = container.domain_repository()
    user_repository: IUserRepository = container.user_repository()

    user_entity = UserEntityFactory.build()
    user = await user_repository.create(user_entity)

    domain_to_create = DomainEntityFactory.build(created_by=user.id)
    created_domain = await domain_repository.create(domain_to_create)
    assert created_domain is not None
    assert created_domain.id is not None

    # When
    result = await domain_repository.delete(created_domain.id)

    # Then
    assert result is True
    with pytest.raises(DatabaseDoesNotExistException):
        await domain_repository.get(created_domain.id)


async def test_delete_non_existent_domain_should_raise_exception(
    container: Container,
) -> None:
    # Given
    domain_repository: IDomainRepository = container.domain_repository()
    non_existent_id = 99999

    # When / Then
    with pytest.raises(DatabaseDoesNotExistException):
        await domain_repository.delete(non_existent_id)
