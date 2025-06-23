import pytest

from core.container.container import Container
from core.interfaces.domain_repository import IDomainRepository
from presentation.exceptions import DatabaseDoesNotExistException

pytestmark = pytest.mark.integration


async def test_get_by_name_returns_domain_when_name_exists(
    container: Container,
) -> None:
    """
    Given: Un domaine créé avec un nom spécifique.
    When: La méthode get_by_name est appelée avec ce nom.
    Then: Elle doit retourner l'entité Domain avec le nom correct.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure isolation
    from apps.tortoise.domain.models import Domain as TortoiseDomain
    from apps.tortoise.user.models import User as TortoiseUser

    await TortoiseDomain.all().delete()
    await TortoiseUser.all().delete()

    # Create a user first
    user = await TortoiseUser.create(
        email="test@example.com",
        password="password123",
        active=True,
        email_verified=True,
    )

    # Create a domain with a specific name
    test_domain_name = "Informatique de Gestion"
    await TortoiseDomain.create(name=test_domain_name, created_by_id=user.id)

    # Act
    result = await domain_repository.get_by_name(test_domain_name)

    # Assert
    assert result is not None
    assert result.name == test_domain_name


async def test_get_by_name_raises_does_not_exist_when_name_not_found(
    container: Container,
) -> None:
    """
    Given: Une base de données sans domaine avec le nom recherché.
    When: La méthode get_by_name est appelée avec un nom qui n'existe pas.
    Then: Elle doit lever une exception DoesNotExist.
    """
    # Arrange
    domain_repository: IDomainRepository = container.domain_repository()

    # Clean the database to ensure isolation
    from apps.tortoise.domain.models import Domain as TortoiseDomain
    from apps.tortoise.user.models import User as TortoiseUser

    await TortoiseDomain.all().delete()
    await TortoiseUser.all().delete()

    # Act & Assert
    with pytest.raises(DatabaseDoesNotExistException):
        await domain_repository.get_by_name("Nom Inexistant")
