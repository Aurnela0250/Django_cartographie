import pytest
from tortoise import exceptions

from core.container.container import Container
from core.entities.domain import DomainEntity
from core.interfaces.domain_repository import IDomainRepository
from core.interfaces.user_repository import IUserRepository
from tests.factories import DomainFactory, UserFactory

pytestmark = pytest.mark.integration


async def test_update_domain_should_succeed(
    container: Container,
) -> None:
    """
    Given: An existing domain created by a first user.
    When: The domain is updated with a new name by a second user.
    Then: The update method should return the updated domain,
          and the changes should be persisted in the database.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()
    user_repository: IUserRepository = container.user_repository()

    # Create the creator and the initial domain
    creator_entity = UserFactory.build()
    creator = await user_repository.create(creator_entity)
    initial_domain_entity = DomainFactory.build(created_by=creator.id)
    created_domain = await domain_repository.create(initial_domain_entity)
    assert created_domain.id is not None

    # Create the user who will perform the update
    updater_entity = UserFactory.build()
    updater = await user_repository.create(updater_entity)
    new_name = "Updated Domain Name"

    # The entity with the updated data
    domain_to_update = DomainEntity(
        id=created_domain.id,
        name=new_name,
        updated_by=updater.id,
        created_by=created_domain.created_by,
    )

    # Act
    updated_domain = await domain_repository.update(created_domain.id, domain_to_update)

    # Assert
    # Check the returned entity
    assert updated_domain is not None
    assert updated_domain.id == created_domain.id
    assert updated_domain.name == new_name
    assert updated_domain.updated_by == updater.id
    assert updated_domain.created_by == creator.id

    # Check for persistence
    persisted_domain = await domain_repository.get(created_domain.id)
    assert persisted_domain is not None
    assert persisted_domain.name == new_name
    assert persisted_domain.updated_by == updater.id
    assert persisted_domain.created_by == creator.id


async def test_update_domain_with_non_existent_id_should_raise_exception(
    container: Container,
) -> None:
    """
    Given: A non-existent domain ID.
    When: The update method is called with this ID.
    Then: A DoesNotExist exception should be raised.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()
    non_existent_domain_id = 999999
    domain_to_update = DomainFactory.build()

    # Act & Assert
    with pytest.raises(exceptions.DoesNotExist):
        await domain_repository.update(non_existent_domain_id, domain_to_update)


async def test_update_domain_with_existing_name_should_raise_integrity_error(
    container: Container,
) -> None:
    """
    Given: Two domains created by a user.
    When: An attempt is made to update the second domain with the name of the first.
    Then: An IntegrityError should be raised due to the unique constraint on the name.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()
    user_repository: IUserRepository = container.user_repository()

    # Create a user
    user_entity = UserFactory.build()
    user = await user_repository.create(user_entity)

    # Create the first domain with a specific name
    existing_domain_entity = DomainFactory.build(
        name="Domaine Existant", created_by=user.id
    )
    await domain_repository.create(existing_domain_entity)

    # Create the second domain to be updated
    domain_to_update_entity = DomainFactory.build(
        name="Domaine à Mettre à Jour", created_by=user.id
    )
    domain_to_update = await domain_repository.create(domain_to_update_entity)
    assert domain_to_update.id is not None

    # Prepare the update with the name of the first domain
    update_data = DomainEntity(
        id=domain_to_update.id,
        name=existing_domain_entity.name,  # Duplicate name
        updated_by=user.id,
        created_by=user.id,
    )

    # Act & Assert
    with pytest.raises(exceptions.IntegrityError):
        await domain_repository.update(domain_to_update.id, update_data)


async def test_update_domain_with_non_existent_user_should_raise_integrity_error(
    container: Container,
) -> None:
    """
    Given: An existing domain.
    When: An attempt is made to update the domain with a non-existent user ID for updated_by.
    Then: An IntegrityError should be raised.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()
    user_repository: IUserRepository = container.user_repository()

    # Create a user and a domain
    user_entity = UserFactory.build()
    user = await user_repository.create(user_entity)
    domain_entity = DomainFactory.build(created_by=user.id)
    domain = await domain_repository.create(domain_entity)
    assert domain.id is not None

    # Prepare the update with a non-existent user ID
    update_data = DomainEntity(
        id=domain.id,
        name="Nouveau nom de domaine",
        updated_by=999999,  # Non-existent user ID
        created_by=user.id,
    )

    # Act & Assert
    with pytest.raises(exceptions.IntegrityError):
        await domain_repository.update(domain.id, update_data)
